import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "anomaly_model.pkl"

# Load model
model = joblib.load(MODEL_PATH)

def predict_file_risk(file_size, hash_length, entropy, verified):
    features = np.array([[file_size, hash_length, entropy, verified]])
    prediction = model.predict(features)

    return "SAFE" if prediction[0] == 1 else "SUSPICIOUS"


if __name__ == "__main__":
    result = predict_file_risk(
        file_size=2048,
        hash_length=64,
        entropy=7.9,
        verified=1
    )

    print("🔍 AI Risk Prediction:", result)