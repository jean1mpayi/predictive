import pandas as pd
import random

def generate_dataset(n=1000):
    data = []

    for i in range(n):
        vibration = random.uniform(0.2, 2.5)
        temperature = random.uniform(30, 80)
        pressure = random.uniform(4, 7)
        torque = random.uniform(10, 20)

        # LABEL (logique simple pour entraîner)
        if vibration > 1.5 or temperature > 65:
            label = 1  # panne
        else:
            label = 0  # normal

        data.append([vibration, temperature, pressure, torque, label])

    return pd.DataFrame(data, columns=[
        "vibration", "temperature", "pressure", "torque", "label"
    ])