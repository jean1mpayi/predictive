import joblib
import numpy as np

model = joblib.load("ml/model.pkl")

def predict(vibration, temperature, pressure, torque):

    stress_index = vibration * temperature
    pressure_ratio = pressure / (torque + 1)

    features = np.array([[vibration, temperature, pressure, torque,
                          stress_index, pressure_ratio]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }