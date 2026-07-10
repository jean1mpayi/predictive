"""Fault diagnostics using weighted expert-style scoring."""

from __future__ import annotations

from typing import Any, Callable


def _clamp(value: float, minimum: int = 0, maximum: int = 100) -> int:
    return int(max(minimum, min(maximum, round(value))))


def _scale(value: float, lower: float, upper: float) -> float:
    """Normalize a metric on a 0-100 scale."""

    if upper <= lower:
        return 0.0
    if value <= lower:
        return 0.0
    if value >= upper:
        return 100.0
    return ((value - lower) / (upper - lower)) * 100.0


def _get(data: dict[str, Any], key: str) -> float:
    return float(data.get(key, 0) or 0)


def _score_bearing_wear(data: dict[str, Any]) -> int:
    vibration = _get(data, "vibration")
    wear = _get(data, "wear")
    temperature = _get(data, "temperature")
    current = _get(data, "current")

    vibration_component = _scale(vibration, 0.35, 1.35)
    wear_component = _scale(wear, 20, 75)
    temperature_component = _scale(temperature, 50, 95)
    current_component = _scale(current, 6, 14)

    score = (
        0.40 * vibration_component
        + 0.35 * wear_component
        + 0.15 * temperature_component
        + 0.10 * current_component
    )

    if wear >= 50 and vibration >= 0.8:
        score += 8

    if wear >= 65 and vibration >= 1.0:
        score += 5

    return _clamp(score)


def _score_cooling_failure(data: dict[str, Any]) -> int:
    temperature = _get(data, "temperature")
    current = _get(data, "current")
    cooling_efficiency = _get(data, "cooling_efficiency")
    load = _get(data, "load")

    temperature_component = _scale(temperature, 70, 100)
    cooling_component = _scale(100 - cooling_efficiency, 20, 95)
    current_component = _scale(current, 8, 16)

    score = (
        0.50 * temperature_component
        + 0.30 * cooling_component
        + 0.20 * current_component
    )

    if temperature >= 95 and cooling_efficiency <= 20:
        score += 20

    if temperature >= 90 and cooling_efficiency <= 30:
        score += 10

    if load >= 85:
        score += 4

    return _clamp(score)


def _score_motor_overload(data: dict[str, Any]) -> int:
    load = _get(data, "load")
    current = _get(data, "current")
    torque = _get(data, "torque")

    load_component = _scale(load, 70, 100)
    current_component = _scale(current, 8, 16)
    torque_component = _scale(torque, 12, 24)

    score = (
        0.50 * load_component
        + 0.30 * current_component
        + 0.20 * torque_component
    )

    if load >= 90:
        score += 20

    if load >= 95 and current >= 11:
        score += 10

    if load >= 95 and torque >= 18:
        score += 5

    return _clamp(score)


def _score_rotor_misalignment(data: dict[str, Any]) -> int:
    vibration = _get(data, "vibration")
    misalignment = _get(data, "misalignment")
    current = _get(data, "current")

    vibration_component = _scale(vibration, 0.35, 1.30)
    misalignment_component = _scale(misalignment, 1, 20)
    current_component = _scale(current, 6, 14)

    score = (
        0.45 * vibration_component
        + 0.40 * misalignment_component
        + 0.15 * current_component
    )

    if misalignment >= 5:
        score += 8

    if misalignment >= 10 and vibration >= 0.9:
        score += 5

    return _clamp(score)


def _score_electrical_fault(data: dict[str, Any]) -> int:
    current = _get(data, "current")
    load = _get(data, "load")
    misalignment = _get(data, "misalignment")

    current_component = _scale(current, 4, 16)
    load_component = _scale(load, 50, 100)
    misalignment_component = _scale(misalignment, 0, 15)

    score = (
        0.55 * current_component
        + 0.25 * load_component
        + 0.20 * misalignment_component
    )

    if current <= 4 or current >= 14:
        score += 10

    if current >= 12 and load >= 80:
        score += 6

    return _clamp(score)


def _score_power_loss(data: dict[str, Any]) -> int:
    current = _get(data, "current")
    speed = _get(data, "speed")
    load = _get(data, "load")

    current_component = _scale(5 - current, 0, 5)
    speed_component = _scale(1500 - speed, 0, 1500)
    load_component = _scale(40 - load, 0, 40)

    score = (
        0.45 * current_component
        + 0.35 * speed_component
        + 0.20 * load_component
    )

    if current <= 2:
        score += 20

    if speed <= 900:
        score += 10

    return _clamp(score)


FAULT_SCORERS: dict[str, Callable[[dict[str, Any]], int]] = {
    "Cooling Failure": _score_cooling_failure,
    "Power Loss": _score_power_loss,
    "Electrical Fault": _score_electrical_fault,
    "Motor Overload": _score_motor_overload,
    "Rotor Misalignment": _score_rotor_misalignment,
    "Bearing Wear": _score_bearing_wear,
}

FAULT_PRIORITY = [
    "Cooling Failure",
    "Power Loss",
    "Electrical Fault",
    "Motor Overload",
    "Rotor Misalignment",
    "Bearing Wear",
]


def detect_fault(sensor_data: dict[str, Any]) -> dict[str, int | str]:
    """Detect the most likely fault using weighted scores and priority order."""

    scores = {name: scorer(sensor_data) for name, scorer in FAULT_SCORERS.items()}
    best_score = max(scores.values())

    if best_score < 35:
        return {
            "fault": "Normal",
            "probability": 0,
        }

    ranked_faults = [
        fault_name
        for fault_name in FAULT_PRIORITY
        if scores[fault_name] == best_score
    ]
    chosen_fault = ranked_faults[0] if ranked_faults else max(
        scores,
        key=scores.get,
    )

    return {
        "fault": chosen_fault,
        "probability": best_score,
    }

