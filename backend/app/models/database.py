import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(DB_DIR, "farmguardian.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FarmProfile(Base):
    __tablename__ = "farm_profiles"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, default="Rithwik Rao")
    location_name = Column(String, default="Guntur, Andhra Pradesh")
    latitude = Column(Float, default=16.3067)
    longitude = Column(Float, default=80.4365)
    primary_crop = Column(String, default="Tomato & Potato")
    farm_size_acres = Column(Float, default=4.5)
    phone_number = Column(String, default="+91 8121985059")

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String, default="Tomato")
    disease_predicted = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    severity_level = Column(String, default="Medium")
    affected_area_pct = Column(Float, default=25.0)
    image_filename = Column(String, nullable=True)
    scanned_at = Column(DateTime, default=datetime.utcnow)
    
    # Weather context at scan time
    temperature_c = Column(Float, default=29.5)
    humidity_pct = Column(Float, default=78.0)
    rainfall_mm = Column(Float, default=12.4)
    spraying_risk = Column(String, default="Medium Risk")

    # Financial & Yield predictions
    yield_loss_pct = Column(Float, default=30.0)
    recovery_probability_pct = Column(Float, default=85.0)
    estimated_cost_inr = Column(Float, default=1850.0)
    estimated_savings_inr = Column(Float, default=14500.0)

    # Treatment Timeline & Details (JSON strings)
    day_1_plan = Column(Text, default="Remove severely infected lower leaves & isolate healthy rows.")
    day_2_plan = Column(Text, default="Apply Copper Oxychloride 50% WP spray (2.5g/L water) in late evening.")
    day_3_plan = Column(Text, default="Inspect leaf undersides for fungal sporulation & ensure field drainage.")
    day_4_plan = Column(Text, default="Foliar application of Neem oil extract (3ml/L) to boost immunity.")
    day_5_plan = Column(Text, default="Final recovery evaluation & schedule bi-weekly preventive spray.")

    voice_called = Column(Boolean, default=False)
    call_summary = Column(Text, nullable=True)

class VoiceCallLog(Base):
    __tablename__ = "voice_call_logs"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scan_records.id"), nullable=True)
    farmer_phone = Column(String, default="+91 8121985059")
    call_status = Column(String, default="Completed")
    duration_seconds = Column(Integer, default=94)
    called_at = Column(DateTime, default=datetime.utcnow)
    transcript = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=False)
    reminder_scheduled = Column(String, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
