def _clamp(value, minimum=0, maximum=100000):
    return max(minimum, min(maximum, value))


def calculate_rul(health_value, fault_name):
    nominal_hours = 10000
    coefficients = {
        "Bearing Wear": 0.6,
        "Cooling Failure": 0.5,
        "Motor Overload": 0.7,
        "Electrical Fault": 0.5,
    }

    coefficient = coefficients.get(fault_name, 1.0)
    hours = _clamp(round(nominal_hours * (health_value / 100.0) * coefficient), 0, nominal_hours)
    days = round(hours / 24.0, 1)

    if health_value >= 80 and coefficient >= 1.0:
        condition = "GOOD"
    elif health_value >= 50:
        condition = "WARNING"
    else:
        condition = "CRITICAL"

    return {
        "hours": hours,
        "days": days,
        "condition": condition,
    }

