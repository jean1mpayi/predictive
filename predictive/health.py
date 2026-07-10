from dataclasses import dataclass


@dataclass
class HealthResult:
    value: int
    penalties: list

    def to_dict(self):
        return {
            "value": self.value,
            "penalties": self.penalties,
        }


def _clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


def _add_penalty(penalties, metric, severity, penalty, reason, measured_value):
    if penalty <= 0:
        return 0

    penalties.append(
        {
            "metric": metric,
            "severity": severity,
            "penalty": penalty,
            "reason": reason,
            "value": measured_value,
        }
    )

    return penalty


def calculate_health(sensor_data):
    penalties = []
    total_penalty = 0

    temperature = float(sensor_data.get("temperature", 0) or 0)
    vibration = float(sensor_data.get("vibration", 0) or 0)
    current = float(sensor_data.get("current", 0) or 0)
    wear = float(sensor_data.get("wear", 0) or 0)
    load = float(sensor_data.get("load", 0) or 0)

    if 25 <= temperature <= 60:
        pass
    elif temperature <= 75:
        total_penalty += _add_penalty(
            penalties,
            "temperature",
            "degraded",
            6,
            "Temperature above nominal range",
            temperature,
        )
    elif temperature <= 90:
        total_penalty += _add_penalty(
            penalties,
            "temperature",
            "degraded",
            14,
            "Temperature indicates progressive overheating",
            temperature,
        )
    else:
        total_penalty += _add_penalty(
            penalties,
            "temperature",
            "critical",
            30,
            "Critical overheating detected",
            temperature,
        )

    if vibration < 0.5:
        pass
    elif vibration <= 0.8:
        total_penalty += _add_penalty(
            penalties,
            "vibration",
            "degraded",
            8,
            "Vibration above nominal range",
            vibration,
        )
    elif vibration <= 1:
        total_penalty += _add_penalty(
            penalties,
            "vibration",
            "degraded",
            15,
            "High vibration suggests mechanical wear",
            vibration,
        )
    else:
        total_penalty += _add_penalty(
            penalties,
            "vibration",
            "critical",
            28,
            "Critical vibration level",
            vibration,
        )

    if 5 <= current <= 10:
        pass
    elif current > 12:
        total_penalty += _add_penalty(
            penalties,
            "current",
            "critical",
            20,
            "Current overload detected",
            current,
        )
    elif current > 10:
        total_penalty += _add_penalty(
            penalties,
            "current",
            "degraded",
            7,
            "Current above nominal range",
            current,
        )
    else:
        total_penalty += _add_penalty(
            penalties,
            "current",
            "degraded",
            15,
            "Current below normal operating range",
            current,
        )

    if wear < 30:
        pass
    elif wear <= 70:
        total_penalty += _add_penalty(
            penalties,
            "wear",
            "degraded",
            16,
            "Component wear detected",
            wear,
        )
    else:
        total_penalty += _add_penalty(
            penalties,
            "wear",
            "critical",
            35,
            "Critical wear detected",
            wear,
        )

    if load < 70:
        pass
    elif load <= 85:
        total_penalty += _add_penalty(
            penalties,
            "load",
            "degraded",
            8,
            "Load above nominal range",
            load,
        )
    else:
        total_penalty += _add_penalty(
            penalties,
            "load",
            "critical",
            18,
            "Motor overload detected",
            load,
        )

    value = _clamp(round(100 - total_penalty))
    return HealthResult(value=value, penalties=penalties)

