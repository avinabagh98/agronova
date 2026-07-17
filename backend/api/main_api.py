import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from sklearn.base import BaseEstimator, TransformerMixin
from fastapi.middleware.cors import CORSMiddleware
from custom_transformers import SkipTransformer, Passthrough
from typing import Optional
import datetime

# --- Scoring Logic ---
def calculate_irrigation_score(prediction, humidity, rainfall):
    """
    Calculate irrigation score based on ML prediction and environmental factors.

    Args:
        prediction (int): Binary prediction from ML model (0=irrigation needed, 1=not needed)
        humidity (float): Humidity percentage
        rainfall (float): Rainfall in mm

    Returns:
        tuple: (score: int, description: str)
    """
    if prediction == 0:
        if humidity < 65:
            return 0, "Irrigation needed urgently"
        else:
            return 1, "Irrigation needed"
    else:
        if rainfall > 200 and humidity > 90:
            return 5, "Water logged"
        elif rainfall > 170 or humidity > 88:
            return 4, "High water level, no irrigation required"
        elif rainfall > 120 or humidity > 80:
            return 3, "Sufficient water, no irrigation required"
        else:
            return 2, "Optimal moisture, no irrigation required"

def calculate_fertility_score(n, p, k, ph):
    """
    Calculate soil fertility based on NPK values and pH.

    Optimal ranges:
    - pH: 6.0-7.5
    - N: 60-120
    - P: 40-80
    - K: 40-80

    Args:
        n (int): Nitrogen content
        p (int): Phosphorus content
        k (int): Potassium content
        ph (float): pH value

    Returns:
        dict: Fertility assessment report
    """
    report = {}
    score = 0

    # pH Assessment
    if 6.0 <= ph <= 7.5:
        report['ph'] = "Optimal"
        score += 25
    elif ph < 6.0:
        report['ph'] = "Acidic - Low"
    else:
        report['ph'] = "Alkaline - High"

    # Nitrogen Assessment
    if 60 <= n <= 120:
        report['nitrogen'] = "Optimal"
        score += 25
    elif n < 60:
        report['nitrogen'] = "Low"
    else:
        report['nitrogen'] = "High"

    # Phosphorus Assessment
    if 40 <= p <= 80:
        report['phosphorus'] = "Optimal"
        score += 25
    elif p < 40:
        report['phosphorus'] = "Low"
    else:
        report['phosphorus'] = "High"

    # Potassium Assessment
    if 40 <= k <= 80:
        report['potassium'] = "Optimal"
        score += 25
    else:
        report['potassium'] = "Low"

    # Overall Fertility
    if score >= 75:
        report['overall_fertility'] = f"Good ({score}%)"
    elif score >= 50:
        report['overall_fertility'] = f"Moderate ({score}%)"
    else:
        report['overall_fertility'] = f"Poor ({score}%)"

    return report

# --- Sensor Data Models ---
class SensorData(BaseModel):
    """Input data model for sensor readings from ESP8266"""
    device_id: str
    temp: Optional[float] = None
    hum: Optional[int] = None
    soilPct: Optional[int] = None
    rain: Optional[str] = None  # "Yes" or "No"
    light: Optional[str] = None  # "Bright" or "Dark"
    pump: Optional[str] = None  # "ON" or "OFF"
    mode: Optional[str] = None  # "AUTO" or "MANUAL"

    class Config:
        schema_extra = {
            "example": {
                "device_id": "agronova-1",
                "temp": 24.0,
                "hum": 55,
                "soilPct": 42,
                "rain": "No",
                "light": "Bright",
                "pump": "OFF",
                "mode": "AUTO"
            }
        }

# --- In-Memory Storage for Sensor Data ---
# In a production environment, this would be replaced with a database
latest_sensor_data = {
    "device_id": None,
    "temp": None,
    "hum": None,
    "soilPct": None,
    "rain": None,
    "light": None,
    "pump": None,
    "mode": None,
    "timestamp": None
}

# --- API Setup ---
app = FastAPI(
    title="Soil and Irrigation Analysis API",
    description="Provides irrigation scores and soil fertility analysis using ML.",
    version="2.0.0"
)

import os

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:9002")
allowed_origins = [
    frontend_url,
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:9002",
    "http://localhost:9002"
]
# If there are multiple frontend URLs (e.g., Vercel previews), they can be passed as a comma-separated string
if "ALLOWED_ORIGINS" in os.environ:
    allowed_origins.extend([origin.strip() for origin in os.environ["ALLOWED_ORIGINS"].split(",")])

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load the ML Pipeline ---
try:
    pipeline = joblib.load('best_pipeline.pkl')
    print("[SUCCESS] ML model loaded successfully!")
except Exception as e:
    pipeline = None
    print(f"[ERROR] FATAL: Could not load model pipeline. Error: {e}")

# --- API Data Models ---
class SoilData(BaseModel):
    """Input data model for soil analysis"""
    N: int
    P: int
    K: int
    temperature: float
    humidity: float
    ph: float
    rainfall: float

    class Config:
        schema_extra = {
            "example": {
                "N": 90,
                "P": 60,
                "K": 70,
                "temperature": 28.5,
                "humidity": 75.0,
                "ph": 6.8,
                "rainfall": 120.0
            }
        }

# --- API Endpoints ---
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "API is online",
        "version": "2.0.0",
        "model_loaded": pipeline is not None
    }

@app.post("/analyze")
def analyze_soil(data: SoilData):
    """
    Analyze soil data and provide irrigation and fertility recommendations.

    Args:
        data (SoilData): Soil parameters and environmental conditions

    Returns:
        dict: Analysis results with irrigation score and fertility report
    """
    if not pipeline:
        return {"error": "Model is not loaded on the server."}

    # Convert input to DataFrame
    input_df = pd.DataFrame([data.dict()])

    # 1. Get binary prediction from ML model
    prediction = pipeline.predict(input_df)[0]

    # 2. Calculate irrigation score (0-5)
    irrigation_score, irrigation_label = calculate_irrigation_score(
        prediction, data.humidity, data.rainfall
    )

    # 3. Calculate fertility report
    fertility_report = calculate_fertility_score(
        data.N, data.P, data.K, data.ph
    )

    return {
        "irrigation_analysis": {
            "score": irrigation_score,
            "description": irrigation_label
        },
        "fertility_analysis": fertility_report
    }

# --- Sensor Data Endpoints ---
@app.post("/api/sensors")
async def receive_sensor_data(sensor_data: SensorData):
    """
    Receive sensor data from ESP8266 device

    Args:
        sensor_data (SensorData): Sensor readings from ESP8266

    Returns:
        dict: Confirmation message
    """
    # Update the global storage with new sensor data
    global latest_sensor_data
    latest_sensor_data = {
        "device_id": sensor_data.device_id,
        "temp": sensor_data.temp,
        "hum": sensor_data.hum,
        "soilPct": sensor_data.soilPct,
        "rain": sensor_data.rain,
        "light": sensor_data.light,
        "pump": sensor_data.pump,
        "mode": sensor_data.mode,
        "timestamp": datetime.datetime.now().isoformat()
    }

    return {
        "status": "success",
        "message": "Sensor data received successfully",
        "timestamp": latest_sensor_data["timestamp"]
    }

@app.get("/api/sensors/latest")
async def get_latest_sensor_data():
    """
    Get the latest sensor data received from ESP8266

    Returns:
        dict: Latest sensor readings or empty dict if no data available
    """
    global latest_sensor_data

    # Check if we have any data
    if latest_sensor_data["device_id"] is None:
        raise HTTPException(status_code=404, detail="No sensor data available")

    return latest_sensor_data

# --- Run the API ---
if __name__ == '__main__':
    print("Starting Soil Analysis API...")
    print("API will be available at: http://127.0.0.1:8000")
    print("API documentation at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)