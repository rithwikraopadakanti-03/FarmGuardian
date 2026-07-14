# FarmGuardian API Documentation

## Authentication Endpoints

### 1. Register User
`POST /api/auth/register`
**Body:**
```json
{
  "username": "farmer_john",
  "email": "john@example.com",
  "password": "securepassword123"
}
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Login User
`POST /api/auth/login`
**Body:**
```json
{
  "username": "farmer_john",
  "password": "securepassword123"
}
```
**Response (200 OK):** (Same as register)

### 3. Guest Login
`POST /api/auth/guest`
Creates an anonymous session.
**Response (200 OK):** (Same as register)

---

## Core Endpoints

### 4. Predict Disease
`POST /api/predict`
Analyzes a leaf image for disease, severity, and provides recommendations.

**Request:** `multipart/form-data`
*   `file`: The image file (jpeg, png).
*   `language`: (Optional) "en", "te", or "hi". Default is "en".

**Response (200 OK):**
```json
{
  "disease": "Tomato___Early_blight",
  "confidence": 0.98,
  "severity_level": "Moderate",
  "severity_score": 45.2,
  "risk_level": "Medium",
  "yield_loss_range": "15-25%",
  "revenue_impact": "₹4,500 - ₹7,500 per acre",
  "recommendations": {
    "immediate_actions": ["Remove infected leaves immediately."],
    "organic_treatments": ["Apply copper-based fungicides."],
    "chemical_treatments": ["Apply Chlorothalonil."],
    "preventive_measures": ["Practice 3-year crop rotation."]
  }
}
```

### 5. Generate Field Report
`POST /api/field-report`
Analyzes multiple images and generates a comprehensive PDF report.

**Request:** `multipart/form-data`
*   `files`: Multiple image files.
*   `language`: (Optional) "en", "te", or "hi".

**Response (200 OK):**
```json
{
  "health_score": 75.5,
  "disease_distribution": {
    "Tomato___Early_blight": 2,
    "Tomato___healthy": 1
  },
  "risk_distribution": {
    "Medium": 2,
    "None": 1
  },
  "recommendations": { ... },
  "pdf_url": "/reports/report_abc123.pdf"
}
```

### 6. Health Check
`GET /api/health`
**Response (200 OK):**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": "0:15:30.123456",
  "model_loaded": true
}
```
