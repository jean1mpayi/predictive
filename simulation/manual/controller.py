"""
simulation/manual/controller.py

ManualController : interface de contrôle manuel du moteur synchrone.

Ce contrôleur permet à un opérateur d'injecter des valeurs directement
dans le Digital Twin depuis le Dashboard ou l'API.

Fonctionnement :
- Chaque set_*() valide la valeur puis l'écrit sur motor.*
- Les champs "override" ont priorité sur le calcul physique au cycle suivant
- reset_parameter() restaure la valeur nominale du moteur
- reset_all() rétablit les defaults du moteur (motor.reset() partiel)
- Aucune logique de maintenance dans ce fichier (respecte l'architecture)

Architecture :
    ManualController
         ↓ (agit sur)
    SynchronousMotor
         ↓ (lu par)
    Sensors → MaintenanceEngine → API → Dashboard
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any

from .validators import ManualValidator

if TYPE_CHECKING:
    from simulation.core.motor import SynchronousMotor

logger = logging.getLogger(__name__)


class ControlMode(str, Enum):
    AUTO = "AUTO"
    MANUAL = "MANUAL"


# Valeurs nominales par défaut — synchronisées avec motor.py
_MOTOR_DEFAULTS: dict[str, float] = {
    "load":               40.0,
    "wear":               5.0,
    "misalignment":       0.0,
    "cooling_efficiency": 100.0,
    "internal_temperature": 35.0,
    "speed":              1500.0,   # Physics.params.nominal_speed
    "current":            0.0,      # recalculé automatiquement
    "torque":             0.0,      # recalculé automatiquement
    "vibration":          0.0,      # recalculé automatiquement
}


class ManualController:
    """
    Contrôleur de réglage manuel du moteur synchrone.

    Possède une référence directe à l'instance SynchronousMotor
    du SimulationEngine courant.

    Compatible avec :
    - Plusieurs moteurs (multi-instance) : instancier un controller par moteur
    - FaultInjector : les overrides peuvent coexister avec les pannes
    - Machine Learning futur : les valeurs appliquées sont loguées

    Attributes:
        motor: Référence au moteur synchrone cible.
    """

    def __init__(self, motor: "SynchronousMotor") -> None:
        """
        Initialise le contrôleur avec la référence au moteur.

        Args:
            motor: Instance de SynchronousMotor à piloter.
        """
        self.motor = motor
        self.mode = ControlMode.AUTO
        logger.info("[ManualController] Initialisé sur moteur %s", motor)

    # ==================================================================
    # MODE
    # ==================================================================

    def set_mode(self, mode: str) -> None:
        """Passe le contrôleur en mode AUTO ou MANUAL."""
        mode_name = mode.value if isinstance(mode, ControlMode) else str(mode)
        self.mode = ControlMode(mode_name.upper())
        self.motor.manual_mode = self.mode.value
        if self.mode == ControlMode.AUTO:
            self.clear_overrides()
        logger.info("[ManualController] mode → %s", self.mode.value)

    def is_manual(self) -> bool:
        return self.mode == ControlMode.MANUAL

    def is_auto(self) -> bool:
        return self.mode == ControlMode.AUTO

    def clear_overrides(self) -> None:
        """Supprime tous les overrides manuels afin de reprendre le calcul physique."""
        for key in self.motor.manual_override:
            self.motor.manual_override[key] = None

    # ==================================================================
    # SET — modifications directes
    # ==================================================================

    def set_temperature(self, value: float) -> None:
        """
        Force la température interne du moteur.

        Args:
            value: Température en °C [0, 130].
        """
        ManualValidator.validate("temperature", value)
        if self.is_manual():
            self.motor.manual_override["temperature"] = float(value)
        else:
            self.motor.internal_temperature = float(value)
        logger.debug("[ManualController] temperature → %.2f °C", value)

    def set_load(self, value: float) -> None:
        """
        Force la charge mécanique du moteur.

        Args:
            value: Charge en % [0, 100].
        """
        ManualValidator.validate("load", value)
        self.motor.load = float(value)
        logger.debug("[ManualController] load → %.2f %%", value)

    def set_vibration(self, value: float) -> None:
        """
        Force le niveau de vibration.

        Note : Bypass le calcul Physics.compute_vibration() au cycle courant.
               Le moteur recalculera automatiquement si wear/misalignment changent.

        Args:
            value: Vibration en g [0, 5].
        """
        ManualValidator.validate("vibration", value)
        if self.is_manual():
            self.motor.manual_override["vibration"] = float(value)
        else:
            self.motor.vibration = float(value)
        logger.debug("[ManualController] vibration → %.3f g", value)

    def set_current(self, value: float) -> None:
        """
        Force le courant électrique absorbé.

        Args:
            value: Courant en A [0, 30].
        """
        ManualValidator.validate("current", value)
        if self.is_manual():
            self.motor.manual_override["current"] = float(value)
        else:
            self.motor.current = float(value)
        logger.debug("[ManualController] current → %.2f A", value)

    def set_speed(self, value: float) -> None:
        """
        Force la vitesse de rotation.

        Args:
            value: Vitesse en rpm [0, 3000].
        """
        ManualValidator.validate("speed", value)
        if self.is_manual():
            self.motor.manual_override["speed"] = float(value)
        else:
            self.motor.speed = float(value)
        logger.debug("[ManualController] speed → %.1f rpm", value)

    def set_torque(self, value: float) -> None:
        """
        Force le couple moteur.

        Args:
            value: Couple en N.m [0, 200].
        """
        ManualValidator.validate("torque", value)
        if self.is_manual():
            self.motor.manual_override["torque"] = float(value)
        else:
            self.motor.torque = float(value)
        logger.debug("[ManualController] torque → %.2f N.m", value)

    def set_wear(self, value: float) -> None:
        """
        Force l'usure des roulements.

        Impacte directement : vibration, courant, health_index au cycle suivant.

        Args:
            value: Usure en % [0, 100].
        """
        ManualValidator.validate("wear", value)
        self.motor.wear = float(value)
        logger.debug("[ManualController] wear → %.2f %%", value)

    def set_misalignment(self, value: float) -> None:
        """
        Force le désalignement du rotor.

        Impacte directement : vibration, health_index au cycle suivant.

        Args:
            value: Désalignement en % [0, 100].
        """
        ManualValidator.validate("misalignment", value)
        self.motor.misalignment = float(value)
        logger.debug("[ManualController] misalignment → %.2f %%", value)

    def set_cooling_efficiency(self, value: float) -> None:
        """
        Force le rendement du système de refroidissement.

        Impacte directement : température, health_index au cycle suivant.

        Args:
            value: Rendement en % [0, 100].
        """
        ManualValidator.validate("cooling_efficiency", value)
        self.motor.cooling_efficiency = float(value)
        logger.debug("[ManualController] cooling_efficiency → %.2f %%", value)

    # ==================================================================
    # SET — dispatch générique
    # ==================================================================

    # Table de dispatch : paramètre → méthode setter
    _SETTERS: dict[str, str] = {
        "temperature":        "set_temperature",
        "load":               "set_load",
        "vibration":          "set_vibration",
        "current":            "set_current",
        "speed":              "set_speed",
        "torque":             "set_torque",
        "wear":               "set_wear",
        "misalignment":       "set_misalignment",
        "cooling_efficiency": "set_cooling_efficiency",
    }

    def set_parameter(self, parameter: str, value: float) -> None:
        """
        Point d'entrée générique pour modifier n'importe quel paramètre.

        Utilisé par l'API pour éviter un switch/case côté Vue.

        Args:
            parameter: Nom du paramètre (insensible à la casse).
            value: Nouvelle valeur.

        Raises:
            ValueError: Si le paramètre est inconnu.
            ValidationError: Si la valeur est hors plage.
        """
        param = parameter.lower().strip()

        setter_name = self._SETTERS.get(param)
        if setter_name is None:
            raise ValueError(
                f"[ManualController] Paramètre inconnu : '{parameter}'. "
                f"Paramètres supportés : {list(self._SETTERS.keys())}"
            )

        method = getattr(self, setter_name)
        method(value)

    # ==================================================================
    # RESET — réinitialisation
    # ==================================================================

    def reset_parameter(self, parameter: str) -> None:
        """
        Remet un paramètre à sa valeur nominale par défaut.

        Args:
            parameter: Nom du paramètre à réinitialiser.

        Raises:
            ValueError: Si le paramètre est inconnu.
        """
        param = parameter.lower().strip()

        if param not in _MOTOR_DEFAULTS:
            raise ValueError(
                f"[ManualController] Impossible de reset '{parameter}' : "
                f"paramètre inconnu."
            )

        default_value = _MOTOR_DEFAULTS[param]

        # Correspondance champ moteur
        _motor_attr = {
            "temperature": "internal_temperature",
        }
        attr = _motor_attr.get(param, param)

        setattr(self.motor, attr, default_value)
        logger.info(
            "[ManualController] reset '%s' → %.2f", parameter, default_value
        )

    def reset_all(self) -> None:
        """
        Réinitialise tous les paramètres manuels aux valeurs nominales.

        N'arrête PAS le moteur (contrairement à motor.reset()).
        Conserve motor.running, motor.runtime.
        """
        was_running = self.motor.running
        runtime = self.motor.runtime

        self.motor.load               = _MOTOR_DEFAULTS["load"]
        self.motor.wear               = _MOTOR_DEFAULTS["wear"]
        self.motor.misalignment       = _MOTOR_DEFAULTS["misalignment"]
        self.motor.cooling_efficiency = _MOTOR_DEFAULTS["cooling_efficiency"]
        self.motor.internal_temperature = _MOTOR_DEFAULTS["internal_temperature"]
        self.motor.current            = _MOTOR_DEFAULTS["current"]
        self.motor.torque             = _MOTOR_DEFAULTS["torque"]
        self.motor.vibration          = _MOTOR_DEFAULTS["vibration"]
        self.clear_overrides()

        # Restaurer l'état de marche et le runtime
        self.motor.running = was_running
        self.motor.runtime = runtime

        logger.info("[ManualController] reset_all effectué (running=%s)", was_running)

    # ==================================================================
    # Snapshot — état actuel (utile pour debug / ML futur)
    # ==================================================================

    def snapshot(self) -> dict[str, Any]:
        """
        Retourne un dictionnaire de l'état manuel actuel du moteur.

        Utile pour les logs, les tests, et la future intégration ML.
        """
        return {
            "temperature":        self.motor.internal_temperature,
            "load":               self.motor.load,
            "wear":               self.motor.wear,
            "misalignment":       self.motor.misalignment,
            "cooling_efficiency": self.motor.cooling_efficiency,
            "vibration":          self.motor.vibration,
            "current":            self.motor.current,
            "speed":              self.motor.speed,
            "torque":             self.motor.torque,
            "running":            self.motor.running,
        }
