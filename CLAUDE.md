# CLAUDE.md — AgroNova Project Context

This file gives Claude Code context on the AgroNova project: an IoT soil-monitoring
device (ESP8266) feeding data into the AgroNova AI platform (Next.js + FastAPI).

## Project Overview

AgroNova AI is an agricultural intelligence platform with two parts:

1. **AgroNova AI platform** (this repo, hosted on Render: `agro-nova-2.onrender.com`)
   - `frontend/` — Next.js 15.3 + TypeScript + Tailwind, App Router
   - `backend/api/main_api.py` — FastAPI backend serving ML predictions
     (yield prediction, pest/disease detection from images, soil NPK analysis),
     weather integration, and market price data. Uses Google Gemini + a trained
     ML pipeline (`best_pipeline.pkl`).
2. **AgroNova hardware unit** (ESP8266 NodeMCU, separate `.ino` firmware, not in
   this repo yet) — a physical device with soil moisture, DHT11 temp/humidity,
   rain, and light sensors, plus a relay-driven water pump. It has its own local
   web dashboard and OLED display.

## Current Integration Goal

Wire the ESP8266 hardware unit into this platform so live sensor readings show
up in the Next.js dashboard, instead of the dashboard only using
demo/manual-entry data.

**Data flow (target):**
```
ESP8266 sensors → HTTPS POST → backend/api/main_api.py (new /api/sensors route)
                                        ↓
                              storage (TBD — see Open Questions)
                                        ↓
                         Next.js frontend reads via GET /api/sensors/latest (or similar)
```

## What's Already Done (firmware side)

The ESP8266 firmware (`AgroNova_v8.ino`, delivered separately, not yet in this
repo) has been updated to:

- Run `WiFi.mode(WIFI_AP_STA)` — keeps its local dashboard alive at `192.168.4.1`
  **and** connects to the home router for internet access, concurrently.
- POST a JSON payload to `https://agro-nova-2.onrender.com/api/sensors` every
  45 seconds (separate timer from the 2-second local sensor-read loop), via
  `ESP8266HTTPClient` + `WiFiClientSecure` (currently using `client.setInsecure()`
  — no cert pinning yet, flagged as a known simplification).
- Only sends when Wi-Fi station mode is actually connected (skips + logs
  otherwise; local dashboard still works either way).

**Payload shape POSTed by the device:**
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
`temp`/`hum` can be `null` if the DHT11 read failed.

## What's NOT Done Yet (backend side — the actual next step)

- `backend/api/main_api.py` does **not yet have** a `/api/sensors` ingestion
  route. A generic standalone FastAPI stub was drafted earlier in conversation
  but should **not** be used as-is — it doesn't match this repo's existing
  FastAPI app instance, CORS setup, or storage conventions.
- The right move: read `main_api.py`, then add a `/api/sensors` (POST) route
  and a corresponding read route (e.g. `/api/sensors/latest`,
  `/api/sensors/history`) using whatever conventions the existing endpoints
  already follow (route prefix style, response models, error handling).
- Frontend: no dashboard component yet consumes live sensor data — will need
  a fetch/hook added once the backend route exists.

## Open Questions To Resolve

- **Storage**: does `main_api.py` already use any persistence (DB, in-memory,
  file)? Sensor readings should follow the same pattern rather than
  introducing a second storage mechanism.
- **Route prefix convention**: confirm whether existing endpoints live under
  `/api/...`, `/predict`, etc., so the new route matches.
- **Auth**: current `/pump` and `/mode` endpoints on the ESP8266 itself have no
  auth. Same question applies to whether `/api/sensors` on the backend should
  require an API key/device token — worth deciding before exposing it publicly
  on Render.

## Known Issues / Things to Flag If Touched

- ESP8266 firmware has **WiFi credentials hardcoded in plaintext** in the
  `.ino` file (`STA_SSID`, `STA_PASS`). Fine for a hobby build, but don't copy
  this pattern into anything shared publicly — consider `WiFiManager` or a
  gitignored `secrets.h` if the firmware gets added to this repo.
- Render free tier sleeps on inactivity — first request after idle can take
  20–30s. The firmware doesn't currently retry on a failed/slow POST.
- `client.setInsecure()` in the firmware skips TLS certificate validation —
  acceptable for now, not hardened.

## Useful Commands (per README)

```bash
# Backend
cd backend/api
python -m uvicorn main_api:app --reload

# Frontend
cd frontend
npm run dev
```
