from sqlalchemy import Column, Integer, String, Date, Float
from database import Base

class BloodDonation(Base):
    __tablename__ = "blood_donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    donation_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    shelf_life_days = Column(Integer, nullable=True)
    volume = Column(Float, nullable=True)
