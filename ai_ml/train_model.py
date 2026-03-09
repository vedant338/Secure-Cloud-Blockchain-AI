import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest
import joblib

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "file_features.csv"
MODEL_PATH = BASE_DIR / "model" / "anomaly_model.pkl"

data = pd.read_csv(DATA_PATH)

X = data[["file_size", "hash_length", "entropy", "verified"]]

model = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

model.fit(X)

joblib.dump(model, MODEL_PATH)

print("✅ AI model trained & saved successfully")