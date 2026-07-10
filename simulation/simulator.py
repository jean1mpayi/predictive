import random
import time
from .models import SimulationConfig


def generate_normal():
    return {
        "vibration": round(random.uniform(0.2, 0.5), 2),
        "temperature": round(random.uniform(30, 40), 1),
        "pressure": round(random.uniform(5.8, 6.2), 2),
        "torque": round(random.uniform(10, 12), 2),
    }


def generate_bearing_wear(t):
    return {
        "vibration": round(0.3 + 0.05 * t, 2),
        "temperature": round(35 + 0.2 * t, 1),
        "pressure": round(random.uniform(5.5, 6.2), 2),
        "torque": round(random.uniform(10, 13), 2),
    }


def generate_data(config, t=1):
    if config.fault_mode == "normal":
        return generate_normal()

    elif config.fault_mode == "bearing_wear":
        return generate_bearing_wear(t)

    else:
        return generate_normal()