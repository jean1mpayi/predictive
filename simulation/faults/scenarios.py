"""
Fault scenario knowledge base.

Les valeurs représentent la dégradation appliquée
à CHAQUE cycle de simulation.

Modifier uniquement les valeurs ci-dessous pour
accélérer ou ralentir une panne.
"""

from __future__ import annotations

# ==========================================================
# VITESSE DE DEGRADATION
#
# DEMO      -> 1 à 5 secondes
# REALISTIC -> 30 à 120 secondes
# INDUSTRY  -> plusieurs minutes
#
# Il suffit de modifier DEMO_FACTOR.
# ==========================================================

DEMO_FACTOR = 10

FAULT_SCENARIOS = {

    "NORMAL": {},

    # --------------------------------------------
    # Roulements
    # --------------------------------------------
    "BEARING_WEAR": {

        # augmente l'usure
        "wear": 2.0 * DEMO_FACTOR,

        # augmente progressivement les vibrations
        "misalignment": 0.30 * DEMO_FACTOR,
    },

    # --------------------------------------------
    # Refroidissement
    # --------------------------------------------
    "COOLING_FAILURE": {

        # fait chuter très vite le refroidissement
        "cooling_efficiency": -4.0 * DEMO_FACTOR,
    },

    # --------------------------------------------
    # Surcharge
    # --------------------------------------------
    "MOTOR_OVERLOAD": {

        # augmente rapidement la charge
        "load": 3.5 * DEMO_FACTOR,
    },

    # --------------------------------------------
    # Désalignement rotor
    # --------------------------------------------
    "ROTOR_MISALIGNMENT": {

        "misalignment": 0.70 * DEMO_FACTOR,
    },

    # --------------------------------------------
    # Défaut électrique
    # --------------------------------------------
    "ELECTRICAL_FAULT": {

        "load": 2.0 * DEMO_FACTOR,
        "misalignment": 0.35 * DEMO_FACTOR,
    },

    # --------------------------------------------
    # Coupure alimentation
    # --------------------------------------------
    "POWER_LOSS": {

        "load": -6.0 * DEMO_FACTOR,
    },
}