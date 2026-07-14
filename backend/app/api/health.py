from fastapi import APIRouter
from datetime import datetime
from app.models.schemas import HealthResponse
from app.services.ml_service import ml_service

router = APIRouter()
START_TIME = datetime.utcnow()

@router.get("/", response_model=HealthResponse)
def health_check():
    uptime = str(datetime.utcnow() - START_TIME)
    return HealthResponse(
        status="ok",
        version="1.0.0",
        uptime=uptime,
        model_loaded=ml_service.is_loaded()
    )
