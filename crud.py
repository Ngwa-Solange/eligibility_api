from sqlalchemy.orm import Session
from models import BloodDonation
from datetime import datetime
import pandas as pd

def create_blood_donation(db: Session, donation):
    db_donation = BloodDonation(**donation.dict())
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation

def bulk_insert_donations(db: Session, df: pd.DataFrame):
    # Assuming df columns match BloodDonation fields
    for _, row in df.iterrows():
        donation_data = {
            "donor_name": row.get("donor_name", "Unknown"),
            "blood_type": row["blood_type"],
            "donation_date": pd.to_datetime(row["donation_date"]).date(),
            "expiry_date": pd.to_datetime(row["expiry_date"]).date() if pd.notnull(row.get("expiry_date")) else None,
            "shelf_life_days": int(row["shelf_life_days"]) if pd.notnull(row.get("shelf_life_days")) else None,
            "volume": float(row["volume"]) if pd.notnull(row.get("volume")) else None,
        }
        create_blood_donation(db, donation=donation_data)
