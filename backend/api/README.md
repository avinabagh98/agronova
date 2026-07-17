# 🧪 Soil and Irrigation Analysis API (FastAPI)

This directory contains the machine learning backend for AgriVision AI, providing intelligent soil health assessments and irrigation scheduling.

## 📦 File Structure

- **`main_api.py`** - Primary FastAPI entry point with intelligent scoring logic.
- **`train_model.py`** - Machine learning script to train the Random Forest pipeline.
- **`custom_transformers.py`** - Custom scikit-learn transformers (`SkipTransformer`, `Passthrough`).
- **`best_pipeline.pkl`** - The exported ML model (generated after training).
- **`1_install_packages.bat`**, **`2_train_model.bat`**, **`3_start_api.bat`** - Automation scripts for Windows.

---

## 🚀 Setup & Execution

### 1. Install Dependencies

Ensure you have Python 3.11+ installed. Run the following in your terminal:

```bash
pip install -r ../requirements.txt
```

*Or use the Windows shortcut:*
Double-click `1_install_packages.bat`

### 2. Train the Machine Learning Model

The backend requires a trained pipeline to function. Generate it by running:

```bash
python train_model.py
```

*Or use the Windows shortcut:*
Double-click `2_train_model.bat`

**Expected Output:**
- `✓ Generated synthetic training data (2,000 samples)`
- `✓ Model performance: ~100.00%`
- `✓ Saved: best_pipeline.pkl`

### 3. Launch the API Server

Start the FastAPI application:

```bash
python main_api.py
```

*Or use the Windows shortcut:*
Double-click `3_start_api.bat`

---

## 🎯 API Endpoints

### Health Check
**GET** `http://127.0.0.1:8000/`
Returns current API status and model state.

### Soil & Irrigation Analysis
**POST** `http://127.0.0.1:8000/analyze`
**Payload:**
```json
{
    "N": 90,
    "P": 60,
    "K": 70,
    "temperature": 28.5,
    "humidity": 75.0,
    "ph": 6.8,
    "rainfall": 120.0
}
```

**Response includes:**
- `prediction`: Binary suitability.
- `irrigation_score`: 0-5 scale (Calculated using ML + real-time conditions).
- `fertility_report`: Detailed NPK and pH assessment.

---

## 🛠️ Testing

Open the interactive Swagger documentation:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


### Option 3: Python
```python
import requests

data = {
    "N": 90,
    "P": 60,
    "K": 70,
    "temperature": 28.5,
    "humidity": 75.0,
    "ph": 6.8,
    "rainfall": 120.0
}

response = requests.post("http://127.0.0.1:8000/analyze", json=data)
print(response.json())
```

---

## ❓ Troubleshooting

### "pip is not recognized"
Try these alternatives:
```powershell
python -m pip install ...
# OR
py -m pip install ...
# OR
pip3 install ...
```

### "python is not recognized"
Try:
```powershell
py train_model.py
# OR
python3 train_model.py
```

### Check Python installation
```powershell
python --version
# OR
py --version
```

### Model file not created
- Make sure all packages are installed
- Check for error messages in the training output
- Ensure you have write permissions in this folder

### API won't start
- Check if port 8000 is already in use
- Make sure `best_pipeline.pkl` exists
- Verify all packages are installed

---

## 📊 What the Model Does

The trained model predicts whether irrigation is needed based on:
- **N, P, K** (soil nutrients)
- **Temperature** (°C)
- **Humidity** (%)
- **pH** (soil acidity)
- **Rainfall** (mm)

**Output:**
- **0** = Irrigation needed
- **1** = No irrigation needed

The API then converts this to a 0-5 score with recommendations!

---

## 🔄 Retrain the Model

If you want to retrain with different data:

1. Edit `train_model.py` (modify the `generate_synthetic_data` function)
2. Run: `python train_model.py`
3. Restart the API server

---

## 📁 File Structure

```
src/api/
├── train_model.py          ← Run this first to create the model
├── main_api.py             ← Run this to start the API server
├── best_pipeline.pkl       ← Created by train_model.py
└── README.md               ← This file
```

---

## ✅ Checklist

- [ ] Python installed
- [ ] Packages installed (`pip install ...`)
- [ ] Model trained (`python train_model.py`)
- [ ] `best_pipeline.pkl` file exists
- [ ] API server running (`python main_api.py`)
- [ ] Web app can connect to API

---

