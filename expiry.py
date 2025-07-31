from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import ExpiryPredictionRequest, ExpiryPredictionResponse
from database import get_db
import joblib
from datetime import datetime

router = APIRouter()

# Load the model once when the router is imported
model = joblib.load("expiry_predictor.pkl")

def preprocess_input(data: ExpiryPredictionRequest):
    # Example feature engineering (you may need to adjust based on your training)
    # Convert donation_date to numeric day of year, encode blood type as categorical int
    blood_type_map = {'A+': 0, 'A-': 1, 'B+': 2, 'B-': 3, 'AB+': 4, 'AB-': 5, 'O+': 6, 'O-': 7}
    day_of_year = data.donation_date.timetuple().tm_yday
    blood_type_encoded = blood_type_map.get(data.blood_type.upper(), -1)
    volume = data.volume if data.volume is not None else 0
    if blood_type_encoded == -1:
        raise HTTPException(status_code=400, detail="Invalid blood type")
    return [[blood_type_encoded, day_of_year, volume]]

@router.post("/predict_expiry", response_model=ExpiryPredictionResponse)
def predict_expiry(data: ExpiryPredictionRequest, db: Session = Depends(get_db)):
    features = preprocess_input(data)
    pred = model.predict(features)[0]
    # Optional: save prediction as new donation record? (not required here)
    return ExpiryPredictionResponse(predicted_shelf_life_days=pred)
