import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load dataset
data = pd.read_csv("dataset/file_activity.csv")

# Train model
model = IsolationForest(
    n_estimators=100,
    contamination=0.2,
    random_state=42
)

model.fit(data)

# Save model
joblib.dump(model, "file_risk_model.pkl")

print("AI model trained successfully")