from dataclasses import dataclass, field
from typing import Optional

from .physics import Physics


@dataclass
class SynchronousMotor:
    """
    Jumeau numérique simplifié d'un moteur synchrone.

    Cette classe représente uniquement l'état interne du moteur.
    Toute la logique physique est déléguée à la classe Physics.
    """

    # -----------------------------
    # Etat général
    # -----------------------------
    running: bool = False

    # -----------------------------
    # Etats internes (%)
    # -----------------------------
    load: float = 40.0                   # Charge mécanique
    wear: float = 5.0                    # Usure des roulements
    misalignment: float = 0.0            # Désalignement
    cooling_efficiency: float = 100.0    # Rendement du refroidissement

    # -----------------------------
    # Grandeurs physiques
    # -----------------------------
    internal_temperature: float = 35.0
    speed: float = Physics.params.nominal_speed

    # Ces valeurs seront calculées automatiquement
    current: float = 0.0
    torque: float = 0.0
    vibration: float = 0.0

    # -----------------------------
    # Contrôle manuel / overrides
    # -----------------------------
    manual_mode: str = "AUTO"
    manual_override: dict[str, Optional[float]] = field(
        default_factory=lambda: {
            "temperature": None,
            "vibration": None,
            "current": None,
            "speed": None,
            "torque": None,
        }
    )

    # -----------------------------
    # Temps de fonctionnement
    # -----------------------------
    runtime: float = 0.0

    # =============================
    # Commandes
    # =============================

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False

        self.load = 40.0
        self.wear = 5.0
        self.misalignment = 0.0
        self.cooling_efficiency = 100.0

        self.internal_temperature = 35.0

        self.speed = Physics.params.nominal_speed

        self.current = 0.0
        self.torque = 0.0
        self.vibration = 0.0

        self.manual_mode = "AUTO"
        self.manual_override = {
            "temperature": None,
            "vibration": None,
            "current": None,
            "speed": None,
            "torque": None,
        }

        self.runtime = 0.0

    # =============================
    # Evolution du moteur
    # =============================

    def update(self, dt=1):

        if not self.running:
            return

        # Limitation de la charge
        self.load = max(
            0,
            min(self.load, Physics.params.max_load)
        )

        # Température
        self.internal_temperature = Physics.compute_temperature(
            current_temp=self.internal_temperature,
            load=self.load,
            wear=self.wear,
            cooling_efficiency=self.cooling_efficiency,
            dt=dt,
            motor=self,
        )

        # Usure
        self.wear = Physics.compute_wear(
            wear=self.wear,
            load=self.load,
            dt=dt
        )

        # Vitesse
        self.speed = Physics.compute_speed(
            self.load,
            motor=self,
        )

        # Courant
        self.current = Physics.compute_current(
            self.load,
            self.wear,
            motor=self,
        )

        # Couple
        self.torque = Physics.compute_torque(
            self.load,
            motor=self,
        )

        # Vibrations
        self.vibration = Physics.compute_vibration(
            self.wear,
            self.misalignment,
            motor=self,
        )

        # Temps de fonctionnement
        self.runtime += dt

    # =============================
    # Etat de santé
    # =============================

    @property
    def health_index(self):
        """
        Retourne un indice de santé compris entre 0 et 100.
        """

        return Physics.compute_health_index(
            wear=self.wear,
            load=self.load,
            misalignment=self.misalignment,
            cooling_efficiency=self.cooling_efficiency
        )