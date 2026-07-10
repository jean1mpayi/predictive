"""Fault injection helper for the motor digital twin."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .scenarios import FAULT_SCENARIOS


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


@dataclass
class FaultInjector:
    """Apply controlled fault drift to the motor internal state.

    The injector only modifies the allowed internal state variables. It never
    touches derived physical values such as temperature, current, speed,
    torque, or vibration. Those are recomputed later by the physics layer.
    """

    current_fault: str = "NORMAL"
    active: bool = False
    cycles: int = 0

    def activate(self, name: str) -> None:
        """Enable a named fault scenario.

        Parameters
        ----------
        name:
            Scenario name as defined in ``FAULT_SCENARIOS``.
        """

        normalized_name = name.upper()
        if normalized_name not in FAULT_SCENARIOS:
            raise ValueError(f"Unknown fault scenario: {name}")

        self.current_fault = normalized_name
        self.active = normalized_name != "NORMAL"
        self.cycles = 0

    def deactivate(self) -> None:
        """Disable fault injection and return to normal mode."""

        self.reset()

    def update(self, motor: Any) -> Any:
        """Apply the active scenario drift to the provided motor.

        The motor instance is mutated in place, but only through the allowed
        internal state variables.
        """

        if not self.active or self.current_fault == "NORMAL":
            return motor

        scenario = FAULT_SCENARIOS[self.current_fault]
        multiplier = 3.0 if self.cycles == 0 else 1.0

        self._apply_delta(
            motor,
            "load",
            scenario.get("load", 0.0) * multiplier,
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "wear",
            scenario.get("wear", 0.0) * multiplier,
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "misalignment",
            scenario.get("misalignment", 0.0) * multiplier,
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "cooling_efficiency",
            scenario.get("cooling_efficiency", 0.0) * multiplier,
            0.0,
            100.0,
        )
        self.cycles += 1

        return motor

    def kick(self, motor: Any) -> Any:
        """Apply an immediate visible impact when the operator selects a fault."""

        if not self.active or self.current_fault == "NORMAL":
            return motor

        scenario = FAULT_SCENARIOS[self.current_fault]
        shock_map = {
            "BEARING_WEAR": {"wear": 8.0, "misalignment": 4.0},
            "COOLING_FAILURE": {"cooling_efficiency": 15.0},
            "MOTOR_OVERLOAD": {"load": 15.0},
            "ROTOR_MISALIGNMENT": {"misalignment": 10.0},
            "ELECTRICAL_FAULT": {"load": 8.0, "misalignment": 4.0},
            "POWER_LOSS": {"load": 20.0},
        }
        shock = shock_map.get(self.current_fault, {})

        self._apply_delta(
            motor,
            "load",
            scenario.get("load", 0.0) * shock.get("load", 5.0),
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "wear",
            scenario.get("wear", 0.0) * shock.get("wear", 5.0),
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "misalignment",
            scenario.get("misalignment", 0.0) * shock.get("misalignment", 5.0),
            0.0,
            100.0,
        )
        self._apply_delta(
            motor,
            "cooling_efficiency",
            scenario.get("cooling_efficiency", 0.0) * shock.get("cooling_efficiency", 10.0),
            0.0,
            100.0,
        )

        if self.current_fault == "POWER_LOSS":
            setattr(motor, "running", False)

        return motor

    def reset(self) -> None:
        """Clear the active fault and restore normal operation."""

        self.current_fault = "NORMAL"
        self.active = False
        self.cycles = 0

    @staticmethod
    def _apply_delta(
        motor: Any,
        attribute: str,
        delta: float,
        minimum: float,
        maximum: float,
    ) -> None:
        if delta == 0:
            return

        current_value = float(getattr(motor, attribute, 0.0))
        updated_value = _clamp(current_value + delta, minimum, maximum)
        setattr(motor, attribute, updated_value)
