from pydantic import BaseModel
from datetime import date
from typing import Optional

class BloodDonationBase(BaseModel):
    donor_name: str
    blood_type: str
    donation_date: date
    volume: Optional[float] = None

class BloodDonationCreate(BloodDonationBase):
    expiry_date: Optional[date] = None
    shelf_life_days: Optional[int] = None

class BloodDonation(BloodDonationBase):
    id: int
    expiry_date: Optional[date]
    shelf_life_days: Optional[int]

    class Config:
        orm_mode = True

class ExpiryPredictionRequest(BaseModel):
    blood_type: str
    donation_date: date
    volume: Optional[float] = None

class ExpiryPredictionResponse(BaseModel):
    predicted_shelf_life_days: float
