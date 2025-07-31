from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
from database import engine, Base, get_db
import models, crud
from routers import expiry
from io import StringIO

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expiry.router, prefix="/api")

@app.post("/api/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    try:
        df = pd.read_csv(StringIO(contents.decode()))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    crud.bulk_insert_donations(db, df)
    return {"message": f"Inserted {len(df)} records"}

@app.get("/")
def root():
    return {"message": "Blood Bank API with expiry prediction"}
