from fastapi import APIRouter, UploadFile, File, Form
from app.models.schemas import SeverityResponse
from app.services.severity_engine import severity_engine

router = APIRouter()

@router.post("/", response_model=SeverityResponse)
async def analyze_severity(
    file: UploadFile = File(...),
    disease: str = Form(...),
    confidence: float = Form(...)
):
    image_bytes = await file.read()
    
    severity_level, severity_score = severity_engine.analyze_severity(image_bytes, disease, confidence)
    
    # Estimate affected area based on severity score
    affected_area = severity_score * 0.8
    
    return SeverityResponse(
        disease=disease,
        severity_level=severity_level,
        severity_score=severity_score,
        affected_area_percentage=round(affected_area, 2)
    )
