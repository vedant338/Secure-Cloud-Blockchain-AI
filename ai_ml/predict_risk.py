import joblib
import numpy as np

model = joblib.load("file_risk_model.pkl")

# Example file metadata
new_file = np.array([[5000, 8, 4, 25, 0]])

prediction = model.predict(new_file)

if prediction[0] == -1:
    print("HIGH RISK file detected")
else:
    print("LOW RISK file")