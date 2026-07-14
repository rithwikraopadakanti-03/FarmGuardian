from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session
from app.models.database import get_db, Scan
from app.models.schemas import PredictionResponse
from app.services.ml_service import ml_service
from app.services.severity_engine import severity_engine
from app.services.yield_predictor import yield_predictor
from app.services.recommendation import recommendation_engine
from app.core.security import get_current_user
import uuid
import os

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    language: str = Form("en"),
    db: Session = Depends(get_db),
    # user = Depends(get_current_user) # Optional for now, to allow guest access without strict tokens if needed
):
    image_bytes = await file.read()
    
    # 1. Prediction
    disease, confidence = ml_service.predict(image_bytes)
    
    # 2. Severity
    severity_level, severity_score = severity_engine.analyze_severity(image_bytes, disease, confidence)
    
    # 3. Risk Level (Derived from severity)
    if severity_level == "Mild":
        risk_level = "Low"
    elif severity_level == "Moderate":
        risk_level = "Medium"
    else:
        risk_level = "High"
        
    if 'healthy' in disease.lower():
        risk_level = "None"
        
    # 4. Yield Loss
    yield_loss_range, revenue_impact = yield_predictor.predict_yield_loss(disease, severity_score)
    
    # 5. Recommendations
    recommendations = recommendation_engine.get_recommendations(disease, severity_level, language)
    
    # 6. Save to DB
    # Save image temporarily
    filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
        
    new_scan = Scan(
        # user_id=user.id,
        image_path=filepath,
        disease=disease,
        confidence=confidence,
        severity=severity_level,
        severity_score=severity_score,
        yield_loss=yield_loss_range
    )
    db.add(new_scan)
    db.commit()
    
    return PredictionResponse(
        disease=disease,
        confidence=confidence,
        severity_level=severity_level,
        severity_score=severity_score,
        risk_level=risk_level,
        yield_loss_range=yield_loss_range,
        revenue_impact=revenue_impact,
        recommendations=recommendations
    )
