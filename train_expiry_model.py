import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load your dataset
df = pd.read_csv("9364ab63-5f53-4af1-b3c8-6b002ee5947f.csv")

# Clean and prepare data
df = df.dropna(subset=["blood_type", "donation_date", "shelf_life_days", "volume"])
df["donation_date"] = pd.to_datetime(df["donation_date"], errors="coerce")
df = df.dropna(subset=["donation_date"])

# Feature engineering
df["day_of_year"] = df["donation_date"].dt.dayofyear
blood_type_map = {'A+': 0, 'A-': 1, 'B+': 2, 'B-': 3, 'AB+': 4, 'AB-': 5, 'O+': 6, 'O-': 7}
df["blood_type_encoded"] = df["blood_type"].map(blood_type_map)
df = df.dropna(subset=["blood_type_encoded"])

# Train model
X = df[["blood_type_encoded", "day_of_year", "volume"]]
y = df["shelf_life_days"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "expiry_predictor.pkl")
print("✅ Model saved as expiry_predictor.pkl")
