from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Load trained model
with open("donor_eligibility_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def home():
    return "Donor Eligibility Model API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]
    return jsonify({"eligible": int(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)