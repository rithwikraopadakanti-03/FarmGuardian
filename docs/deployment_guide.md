# FarmGuardian AI — Deployment Guide

This guide explains how to deploy the FarmGuardian AI platform for production or hackathon judging.

## Frontend Deployment (Vercel)

Vercel is recommended for the React + Vite frontend.

1.  **Configure API URL:** Ensure the frontend points to your deployed backend URL. In `frontend/src/services/api.js`, set the base URL dynamically:
    ```javascript
    const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    ```
2.  **Vercel Setup:**
    *   Connect your GitHub repository to Vercel.
    *   Set the Root Directory to `frontend`.
    *   Framework Preset: `Vite`.
    *   Build Command: `npm run build`.
    *   Output Directory: `dist`.
    *   Environment Variables: Add `VITE_API_URL` pointing to your Render backend URL.

## Backend Deployment (Render)

Render is recommended for hosting the FastAPI backend.

1.  **Prepare for Render:**
    Ensure `requirements.txt` is complete.
2.  **Create Web Service:**
    *   Connect your GitHub repository to Render.
    *   Set the Root Directory to `backend`.
    *   Environment: `Python 3`.
    *   Build Command: `pip install -r requirements.txt`.
    *   Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
3.  **Environment Variables:**
    *   `SECRET_KEY`: Generate a secure random string.
    *   `MODEL_PATH`: If you uploaded your trained model, specify its path (e.g., `./models/farmguardian_model.h5`). Note: Render's free tier has strict memory limits (512MB), which might struggle to load a full TensorFlow model. If it crashes, the app will automatically fall back to the built-in simulation mode.

## Local Docker Deployment (Optional)

For a self-contained local setup:

**Backend Dockerfile (`backend/Dockerfile`):**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
