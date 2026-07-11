"""
Fault injector.

Ne modifie JAMAIS :

- température
- courant
- vitesse
- couple
- vibration

Ces valeurs sont recalculées uniquement
par Physics.
"""

from dataclasses import dataclass
from typing import Any

from .scenarios import FAULT_SCENARIOS


def clamp(value, mini, maxi):
    return max(mini, min(value, maxi))


@dataclass
class FaultInjector:

    current_fault: str = "NORMAL"

    active: bool = False

    cycles: int = 0

    # ====================================================
    # Activer une panne
    # ====================================================

    def activate(self, fault):

        fault = fault.upper()

        if fault not in FAULT_SCENARIOS:
            raise ValueError(f"Unknown fault {fault}")

        self.current_fault = fault

        self.active = fault != "NORMAL"

        self.cycles = 0

    # ====================================================
    # Désactiver
    # ====================================================

    def deactivate(self):

        self.reset()

    # ====================================================
    # Mise à jour
    # ====================================================

    def update(self, motor):

        if not self.active:
            return motor

        scenario = FAULT_SCENARIOS[self.current_fault]

        # ------------------------------------------------
        # IMPORTANT
        #
        # Plus cette valeur est grande,
        # plus la panne devient exponentielle.
        #
        # 0.02 = lent
        # 0.05 = normal
        # 0.10 = rapide
        # 0.15 = démonstration
        # ------------------------------------------------

        acceleration = 1 + (self.cycles * 0.12)

        self.apply(
            motor,
            "load",
            scenario.get("load", 0) * acceleration,
            0,
            100,
        )

        self.apply(
            motor,
            "wear",
            scenario.get("wear", 0) * acceleration,
            0,
            100,
        )

        self.apply(
            motor,
            "misalignment",
            scenario.get("misalignment", 0) * acceleration,
            0,
            100,
        )

        self.apply(
            motor,
            "cooling_efficiency",
            scenario.get("cooling_efficiency", 0) * acceleration,
            0,
            100,
        )

        self.cycles += 1

        return motor

    # ====================================================
    # Impact immédiat
    # ====================================================

    def kick(self, motor):

        if not self.active:
            return motor

        # ------------------------------------------------
        # Le kick rend la panne visible
        # immédiatement après son activation.
        #
        # Modifier uniquement ces valeurs
        # si l'on veut une apparition plus ou moins brutale.
        # ------------------------------------------------

        shock = {

            "BEARING_WEAR": {

                "wear": 35,

                "misalignment": 10,
            },

            "COOLING_FAILURE": {

                "cooling_efficiency": -55,
            },

            "MOTOR_OVERLOAD": {

                "load": 40,
            },

            "ROTOR_MISALIGNMENT": {

                "misalignment": 30,
            },

            "ELECTRICAL_FAULT": {

                "load": 25,

                "misalignment": 15,
            },

            "POWER_LOSS": {

                "load": -45,
            },
        }

        config = shock.get(self.current_fault, {})

        self.apply(
            motor,
            "load",
            config.get("load", 0),
            0,
            100,
        )

        self.apply(
            motor,
            "wear",
            config.get("wear", 0),
            0,
            100,
        )

        self.apply(
            motor,
            "misalignment",
            config.get("misalignment", 0),
            0,
            100,
        )

        self.apply(
            motor,
            "cooling_efficiency",
            config.get("cooling_efficiency", 0),
            0,
            100,
        )

        if self.current_fault == "POWER_LOSS":
            motor.running = False

        return motor

    # ====================================================

    def reset(self):

        self.current_fault = "NORMAL"

        self.active = False

        self.cycles = 0

    # ====================================================

    @staticmethod
    def apply(motor, field, delta, mini, maxi):

        if delta == 0:
            return

        value = getattr(motor, field)

        setattr(
            motor,
            field,
            clamp(value + delta, mini, maxi)
        )