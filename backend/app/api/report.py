from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import List
from sqlalchemy.orm import Session
from app.models.database import get_db, Report
from app.models.schemas import FieldReportResponse
from app.services.ml_service import ml_service
from app.services.severity_engine import severity_engine
from app.services.report_generator import report_generator
from app.services.recommendation import recommendation_engine
import json

router = APIRouter()

@router.post("/", response_model=FieldReportResponse)
async def generate_field_report(
    files: List[UploadFile] = File(...),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    scan_results = []
    total_severity = 0
    disease_counts = {}
    risk_counts = {"Low": 0, "Medium": 0, "High": 0, "None": 0}
    
    for file in files:
        image_bytes = await file.read()
        disease, confidence = ml_service.predict(image_bytes)
        severity_level, severity_score = severity_engine.analyze_severity(image_bytes, disease, confidence)
        
        if severity_level == "Mild": risk = "Low"
        elif severity_level == "Moderate": risk = "Medium"
        else: risk = "High"
        
        if 'healthy' in disease.lower(): risk = "None"
            
        recs = recommendation_engine.get_recommendations(disease, severity_level, language)
        
        scan_data = {
            "disease": disease,
            "confidence": confidence,
            "severity_level": severity_level,
            "severity_score": severity_score,
            "risk_level": risk,
            "recommendations": recs
        }
        scan_results.append(scan_data)
        
        total_severity += severity_score
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
        risk_counts[risk] += 1
        
    # Overall health score (100 - average severity)
    avg_severity = total_severity / len(files) if files else 0
    health_score = 100 - avg_severity
    
    # Generate PDF
    pdf_url = report_generator.generate_pdf(scan_results, health_score)
    
    # Get top recommendations (from the most severe disease found)
    top_recs = {"immediate_actions": [], "preventive_measures": []}
    if scan_results:
        worst = max(scan_results, key=lambda x: x['severity_score'])
        top_recs = worst['recommendations']
        
    # Save Report to DB
    new_report = Report(
        health_score=health_score,
        total_images=len(files),
        diseases_found=json.dumps(disease_counts),
        pdf_path=pdf_url
    )
    db.add(new_report)
    db.commit()
    
    return FieldReportResponse(
        health_score=round(health_score, 2),
        disease_distribution=disease_counts,
        risk_distribution={k: v for k, v in risk_counts.items() if v > 0},
        recommendations=top_recs,
        pdf_url=pdf_url
    )
