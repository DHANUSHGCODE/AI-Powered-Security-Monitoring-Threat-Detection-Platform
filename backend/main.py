from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import joblib
import pandas as pd
import os
import sys

# Add current directory to path so we can import from backend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SecurityLog, SessionLocal, engine, init_db
import schemas

app = FastAPI(title="AI Security Monitor", description="Real-time Thread Detection API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
init_db()

# Load Model (Global)
model = None
encoders = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../ai-model/isolation_forest_model.pkl")
ENCODERS_PATH = os.path.join(BASE_DIR, "../ai-model/encoders.pkl")

def load_model():
    global model, encoders
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            encoders = joblib.load(ENCODERS_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
    else:
        print("Model file not found. Predictions will not work.")

@app.on_event("startup")
async def startup_event():
    load_model()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "AI Security Monitor API is running"}

@app.post("/logs/", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    db_log = SecurityLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/", response_model=List[schemas.LogResponse])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(SecurityLog).order_by(SecurityLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@app.post("/predict/", response_model=schemas.PredictionResponse)
def predict_anomaly(request: schemas.PredictionRequest):
    global model, encoders
    if not model or not encoders:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Preprocess
        protocol_encoded = encoders['protocol'].transform([request.protocol])[0]
        # Note: We need to handle unknown labels in production, but for now assuming known
        
        # Create DataFrame for prediction
        # The model was trained on ['bytes', 'protocol_encoded']
        features = pd.DataFrame([[request.bytes_transferred, protocol_encoded]], columns=['bytes', 'protocol_encoded'])
        
        prediction = model.predict(features)[0] # -1 for anomaly, 1 for normal
        score = model.decision_function(features)[0]
        
        is_anomaly = True if prediction == -1 else False
        
        return {"is_anomaly": is_anomaly, "anomaly_score": score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
