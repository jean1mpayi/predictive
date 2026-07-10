"""Empirical confidence scoring for maintenance diagnostics."""

from __future__ import annotations


def _clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, value))


def calculate_confidence(health_value: int, fault_name: str, probability: int) -> int:
    """Estimate diagnostic confidence on a 0-100 scale.

    The score is intentionally empirical. It favors well-identified faults
    with high probability while keeping normal operation at 100.
    """

    if fault_name == "Normal" or probability <= 0:
        return 100

    bonuses = {
        "Bearing Wear": 16,
        "Cooling Failure": 8,
        "Motor Overload": 12,
        "Electrical Fault": 10,
        "Rotor Misalignment": 10,
        "Power Loss": 6,
    }

    confidence = probability + bonuses.get(fault_name, 5)

    if health_value < 50:
        confidence -= 2

    if probability < 50:
        confidence -= 10

    return _clamp(round(confidence))

