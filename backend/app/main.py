from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import predict, severity, report, auth, health
from app.models.database import engine, Base
from app.core.config import settings

# Create DB tables
Base.metadata.create_all(bind=engine)

# Ensure upload directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "reports"), exist_ok=True)

app = FastAPI(
    title="FarmGuardian AI API",
    description="Early Crop Disease Detection & Yield Loss Prevention System",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
app.mount("/reports", StaticFiles(directory=os.path.join(settings.UPLOAD_DIR, "reports")), name="reports")

# Include routers
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(severity.router, prefix="/api/severity", tags=["Severity"])
app.include_router(report.router, prefix="/api/field-report", tags=["Reports"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FarmGuardian AI API"}
