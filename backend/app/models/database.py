from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True) # Optional, can be null for guests if needed, or we link to guest id
    image_path = Column(String)
    disease = Column(String)
    confidence = Column(Float)
    severity = Column(String)
    severity_score = Column(Float)
    yield_loss = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    health_score = Column(Float)
    total_images = Column(Integer)
    diseases_found = Column(String) # JSON string
    pdf_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
