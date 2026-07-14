from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    severity_level: str
    severity_score: float
    risk_level: str
    yield_loss_range: str
    revenue_impact: str
    recommendations: Dict[str, Any]

class SeverityResponse(BaseModel):
    disease: str
    severity_level: str
    severity_score: float
    affected_area_percentage: float

class FieldReportResponse(BaseModel):
    health_score: float
    disease_distribution: Dict[str, int]
    risk_distribution: Dict[str, int]
    recommendations: Dict[str, List[str]]
    pdf_url: str

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: str
    model_loaded: bool
