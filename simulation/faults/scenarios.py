"""Fault scenario knowledge base.

This module intentionally contains only declarative data. It does not
implement any behavior or decision logic.
"""

from __future__ import annotations


FAULT_SCENARIOS: dict[str, dict[str, float]] = {
    "NORMAL": {},
    "BEARING_WEAR": {
        "wear": 0.20,
        "misalignment": 0.01,
    },
    "COOLING_FAILURE": {
        "cooling_efficiency": -0.50,
    },
    "MOTOR_OVERLOAD": {
        "load": 0.50,
    },
    "ROTOR_MISALIGNMENT": {
        "misalignment": 0.05,
    },
    "ELECTRICAL_FAULT": {
        "load": 0.20,
        "misalignment": 0.02,
    },
    "POWER_LOSS": {
        "load": -1.00,
    },
}

