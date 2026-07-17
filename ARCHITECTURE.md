# AgroNova Architecture Documentation

## Overview

AgroNova is an agricultural intelligence platform consisting of:
1. **Frontend**: Next.js 15.3 application (React + TypeScript + Tailwind CSS)
2. **Backend**: FastAPI application serving ML predictions and analysis
3. **Hardware**: ESP8266-based soil monitoring device (separate firmware, not in this repo)

This document explains how these components work together, their data flow, and deployment configuration.

## Project Structure

```
agrivision-ai/
├── backend/
│   └── api/
│       ├── main_api.py        # FastAPI application
│       ├── requirements.txt   # Python dependencies
│       └── Procfile           # Deployment configuration
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js app router (pages)
│   │   ├── components/        # Reusable UI components
│   │   ├── lib/               # Utility functions
│   │   ├── hooks/             # Custom React hooks
│   │   └── contexts/          # React context providers
│   ├── package.json           # Frontend dependencies
│   ├── next.config.ts         # Next.js configuration
│   └── tailwind.config.ts     # Tailwind CSS configuration
├── Dockerfile                 # Multi-stage Docker build
├── start.sh                   # Application startup script
├── CLAUDE.md                  # Project context for AI assistants
└── readme.md                  # General project documentation
```

## Component Details

### Backend (`backend/api/main_api.py`)

**Purpose**: Provides soil analysis API endpoints using machine learning models.

**Key Features**:
- Loads trained ML pipeline (`best_pipeline.pkl`) at startup
- Exposes `/analyze` endpoint for soil parameter analysis
- Calculates irrigation score (0-5) based on ML prediction + environmental factors
- Generates fertility report based on NPK values and pH
- Implements CORS middleware for frontend communication
- Health check endpoint at `/`

**Data Models**:
- `SoilData`: Input model (N, P, K, temperature, humidity, pH, rainfall)
- Response includes:
  - `irrigation_analysis`: Score (0-5) and description
  - `fertility_analysis`: Detailed NPK/pH assessment

**Dependencies**:
- FastAPI, Uvicorn, Scikit-learn, Pandas, Joblib
- See `backend/requirements.txt` for full list

### Frontend (`frontend/`)

**Purpose**: Provides user interface for interacting with the AgroNova platform.

**Key Pages** (in `frontend/src/app/`):
- `/` - Home/Landing page
- `/soil-analysis` - Soil analysis form and results
- `/analysis` - Detailed analysis view
- `/weather` - Weather data integration
- `/market` - Market price data
- `/pest-disease` - Plant disease detection
- `/map` - Field mapping functionality

**Key Components** (in `frontend/src/components/agrivision/`):
- `SoilAnalysisPage.tsx`: Main soil analysis component
  - Input form for soil parameters
  - Calls backend `/analyze` endpoint
  - Displays irrigation score, fertility report
  - Provides crop recommendations and improvement suggestions
  - Includes export functionality (JSON report)
- Reusable UI components (buttons, cards, inputs, etc.) from `frontend/src/components/ui/`

**State Management**:
- React hooks (`useState`, `useEffect`) for form handling
- Context API for language/i18n support (`LanguageContext`)
- Custom hooks in `frontend/src/hooks/` for specialized logic

## Data Flow

### Current Flow (Manual Input)
```
User Input → Frontend Form → POST /analyze → Backend Processing → ML Model → Response → Frontend Display
```

**Step-by-Step**:
1. User enters soil parameters (N, P, K, temperature, humidity, pH, rainfall) in the soil analysis form
2. On form submission, frontend sends POST request to `/analyze` endpoint
3. Backend receives request, validates input data using Pydantic model
4. ML pipeline (`best_pipeline.pkl`) makes binary prediction (0=irrigation needed, 1=not needed)
5. System calculates irrigation score (0-5) based on prediction + humidity + rainfall
6. System calculates fertility report based on NPK values and pH ranges
7. Backend returns JSON response with both analyses
8. Frontend enhances response with crop recommendations and improvement suggestions
9. Results displayed in UI with visual indicators, scores, and actionable insights

### Planned Flow (ESP8266 Integration)
```
ESP8266 Sensors → HTTPS POST /api/sensors → Backend Storage → GET /api/sensors/latest → Frontend Display
```

**Planned Implementation**:
1. ESP8266 device sends JSON payload every 45 seconds:
   ```json
   {
     "device_id": "agronova-1",
     "temp": 24.0,
     "hum": 55,
     "soilPct": 42,
     "rain": "Yes" | "No",
     "light": "Bright" | "Dark",
     "pump": "ON" | "OFF",
     "mode": "AUTO" | "MANUAL"
   }
   ```
2. New `/api/sensors` POST endpoint in backend to ingest this data
3. Data stored in database (TBD - see Open Questions)
4. New `/api/sensors/latest` GET endpoint to retrieve most recent readings
5. Frontend component to display live sensor data on dashboard

## Deployment on Render

### Docker Configuration

**Multi-stage Dockerfile**:
1. **Builder Stage** (`node:18-alpine`):
   - Installs frontend dependencies
   - Builds Next.js application (`npm run build`)
   - Output: `.next/standalone` and `.next` directory

2. **Final Stage** (`python:3.11-slim`):
   - Installs Node.js 18
   - Installs Python dependencies from `backend/requirements.txt`
   - Copies built frontend and backend code
   - Sets up environment variables
   - Uses `start.sh` as entrypoint

**start.sh Script**:
```bash
#!/bin/bash
set -e

echo "Starting FastAPI backend..."
cd /app/backend/api
uvicorn main_api:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "Starting Next.js frontend..."
cd /app/frontend
export PORT=${PORT:-3000}
export HOSTNAME="0.0.0.0"
node server.js &
FRONTEND_PID=$!

wait -n
exit $?
```

**Key Deployment Details**:
- Backend binds to `127.0.0.1:8000` (internal only, not exposed externally)
- Frontend runs on port specified by `PORT` environment variable (provided by Render)
- Frontend accesses backend via internal localhost communication
- External users only access the frontend port (Render handles SSL termination and routing)
- `NEXT_PUBLIC_API_URL` is set to `/api/py` in Dockerfile (gets proxied to backend)

### Environment Variables
- `PORT`: Set by Render (frontend port)
- `FRONTEND_URL`: Used for CORS configuration in backend
- `ALLOWED_ORIGINS`: Configurable CORS origins
- Other variables as needed for ML model paths, etc.

## Data Storage & Persistence

### Current State (No Persistent Database)
- **No database dependencies** in `requirements.txt`
- **All processing is in-memory** per request
- **ML model loaded at startup** (`joblib.load('best_pipeline.pkl')`)
- **No historical data storage** for sensor readings or user analyses

### Open Questions for Storage
As noted in CLAUDE.md:
> **Storage**: does `main_api.py` already use any persistence (DB, in-memory, file)? Sensor readings should follow the same pattern rather than introducing a second storage mechanism.

**Recommended Approach**:
1. **For MVP**: Use SQLite (file-based, zero-config) for simplicity
2. **For Scaling**: Use PostgreSQL (managed service on Render)
3. **Tables needed**:
   - `sensor_readings`: Store ESP8266 data with timestamps
   - `analysis_history`: Store user soil analysis results
   - `devices`: Register ESP8266 hardware units

## API Endpoints

### Current Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/analyze` | Soil analysis (requires SoilData body) |

### Planned Endpoints (for ESP8266 Integration)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/sensors` | Receive sensor data from ESP8266 |
| GET | `/api/sensors/latest` | Get most recent sensor reading |
| GET | `/api/sensors/history` | Get historical sensor data (with filtering) |
| GET | `/api/sensors/stats` | Get aggregated statistics |

## Security Considerations

### Current State
- No authentication on API endpoints (intended for trusted network/local use)
- ESP8266 firmware uses `client.setInsecure()` (no TLS validation - temporary simplification)
- WiFi credentials hardcoded in ESP8266 firmware (not suitable for production)

### Recommended Improvements
1. **Add API Key Authentication**:
   - Require `X-API-Key` header for `/api/sensors` endpoints
   - Store API keys securely (environment variables or secrets manager)
2. **Improve ESP8266 Security**:
   - Use `WiFiManager` for credential configuration
   - Implement proper TLS certificate validation
   - Consider using MQTT instead of HTTP for better efficiency
3. **Backend Security**:
   - Add rate limiting to prevent abuse
   - Implement input validation and sanitization
   - Add logging and monitoring

## Development Setup

### Backend
```bash
cd backend/api
pip install -r requirements.txt
uvicorn main_api:app --reload  # Development mode
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # Development mode at http://localhost:3000
```

### Full Stack (Docker)
```bash
docker build -t agro-nova .
docker run -p 3000:3000 agro-nova
```

## Future Enhancements

1. **ESP8266 Integration**:
   - Implement `/api/sensors` endpoints
   - Add database storage for sensor data
   - Create live dashboard component
   - Add alerting based on sensor thresholds

2. **User Features**:
   - User authentication and profiles
   - Field management (save multiple field configurations)
   - Analysis history and trends
   - Export options (PDF, CSV)

3. **ML Improvements**:
   - Model retraining pipeline
   - Uncertainty quantification in predictions
   - Ensemble methods for better accuracy

4. **Platform Expansion**:
   - Mobile application (React Native)
   - Multi-language support expansion
   - Integration with agricultural APIs (weather, market data)

## Troubleshooting

### Common Issues
1. **Model Loading Failure**:
   - Ensure `best_pipeline.pkl` exists in `backend/api/`
   - Check file permissions and path correctness

2. **CORS Errors**:
   - Verify `FRONTEND_URL` environment variable matches deployed frontend URL
   - Check `allowed_origins` configuration in `main_api.py`

3. **Port Conflicts**:
   - Ensure backend uses `127.0.0.1:8000` internally
   - Frontend should use Render-provided `PORT` variable

4. **Build Failures**:
   - Clear npm/yarn cache if experiencing frontend build issues
   - Ensure Python version matches Dockerfile specification (3.11-slim)

## Conclusion

This architecture provides a solid foundation for the AgroNova platform, combining AI-powered soil analysis with a modern web interface. The modular design allows for straightforward extension with real-time sensor data from the ESP8266 hardware unit, while the containerized deployment ensures consistency across environments.

The current implementation focuses on manual soil analysis, with clear pathways for integrating live sensor data, enhancing security, and expanding functionality based on user needs.