from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import json
import requests
from datetime import datetime

# Import local backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.database import engine, Base, SessionLocal, ScanRecord, VoiceCallLog, FarmProfile
from app.core.config import settings
from app.services.weather_service import get_weather_data
from app.services.gemini_service import generate_treatment_and_reasoning, ask_farm_advisor
from app.services.voice_service import initiate_omnidimension_voice_call
from app.api import predict, severity, report, auth, health

# Create DB tables
Base.metadata.create_all(bind=engine)

# Ensure upload directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "reports"), exist_ok=True)

app = FastAPI(
    title="FarmGuardian AI Platform",
    description="Commercial AI Farm Intelligence Platform",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
app.mount("/reports", StaticFiles(directory=os.path.join(settings.UPLOAD_DIR, "reports")), name="reports")

# Include original routers
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(severity.router, prefix="/api/severity", tags=["Severity"])
app.include_router(report.router, prefix="/api/field-report", tags=["Reports"])

# --- Platform FastAPI Endpoints ---

@app.get("/api/weather")
def api_weather(lat: float = 16.3067, lon: float = 80.4365):
    return get_weather_data(lat, lon)

@app.post("/api/advisor")
async def api_advisor(request: Request):
    body = await request.json()
    q = body.get("question", "")
    lang = body.get("language", "en")
    ctx = body.get("context", {})
    answer = ask_farm_advisor(q, lang, ctx)
    return {"question": q, "answer": answer, "language": lang}

@app.post("/api/voice/call")
async def api_voice_call(request: Request):
    body = await request.json()
    scan_data = body.get("scan_data", {})
    farmer_phone = body.get("farmer_phone", "+91 8121985059")

    # Initiate OmniDimension Voice Call
    res = initiate_omnidimension_voice_call(scan_data, farmer_phone)

    # Log into database
    db = SessionLocal()
    try:
        call_log = VoiceCallLog(
            farmer_phone=res.get("farmer_phone", farmer_phone),
            call_status="Completed",
            duration_seconds=res.get("duration_seconds", 78),
            transcript=res.get("transcript", ""),
            ai_summary=res.get("ai_summary", ""),
            reminder_scheduled=res.get("reminder_scheduled", "")
        )
        db.add(call_log)
        db.commit()
    except Exception as e:
        print(f"Database call log warning: {e}")
        db.rollback()
    finally:
        db.close()

    return res

@app.get("/api/history")
def api_history():
    db = SessionLocal()
    scans_data = []
    calls_data = []
    try:
        scans = db.query(ScanRecord).order_by(ScanRecord.scanned_at.desc()).limit(20).all()
        for s in scans:
            scans_data.append({
                "id": s.id,
                "crop": s.crop_type,
                "disease": s.disease_predicted,
                "confidence": s.confidence,
                "severity": s.severity_level,
                "date": s.scanned_at.strftime("%Y-%m-%d %H:%M"),
                "savings": s.expected_savings_inr
            })

        calls = db.query(VoiceCallLog).order_by(VoiceCallLog.called_at.desc()).limit(10).all()
        for c in calls:
            calls_data.append({
                "id": c.id,
                "farmer_phone": c.farmer_phone,
                "status": c.call_status,
                "duration_seconds": c.duration_seconds,
                "date": c.called_at.strftime("%Y-%m-%d %H:%M"),
                "summary": c.ai_summary,
                "reminder": c.reminder_scheduled
            })
    except Exception as e:
        print(f"History query warning: {e}")
    finally:
        db.close()

    return {"scans": scans_data, "calls": calls_data}

@app.get("/")
def read_root():
    return {"message": "Welcome to FarmGuardian AI Commercial Platform"}
