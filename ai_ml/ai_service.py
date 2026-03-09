import joblib
import numpy as np
from pathlib import Path

# 📁 Resolve model path correctly
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "anomaly_model.pkl"

# 🧠 Load model ONCE (GLOBAL)
model = joblib.load(MODEL_PATH)

def analyze_file_risk(file_size: int, entropy: float, hash_length: int, verified: int):
    """
    Predicts risk score using trained Isolation Forest
    """

    # Feature order MUST match training
    features = np.array([[file_size, entropy, hash_length, verified]])

    prediction = model.predict(features)

    return {
        "risk": "HIGH" if prediction[0] == -1 else "LOW",
        "model_output": int(prediction[0])
    }