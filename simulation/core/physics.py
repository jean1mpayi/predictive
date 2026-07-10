from dataclasses import dataclass


@dataclass
class MotorParameters:
    """
    Paramètres physiques du moteur synchrone simulé.
    Tous les coefficients peuvent être ajustés afin de
    représenter différents moteurs.
    """

    # Température
    ambient_temperature: float = 25.0       # °C
    max_temperature: float = 120.0          # °C

    # Vitesse nominale
    nominal_speed: float = 1500.0           # tr/min

    # Charge maximale
    max_load: float = 100.0                 # %

    # Coefficients thermiques
    thermal_load_gain: float = 0.02
    thermal_wear_gain: float = 0.03
    thermal_cooling_gain: float = 0.04

    # Evolution de l'usure
    wear_rate: float = 0.001

    # Influence de la charge sur la vitesse
    speed_drop_gain: float = 0.5

    # Courant nominal
    nominal_current: float = 5.0            # A
    current_load_gain: float = 0.06
    current_wear_gain: float = 0.02

    # Couple nominal
    nominal_torque: float = 10.0            # N.m
    torque_load_gain: float = 0.10

    # Vibrations nominales
    nominal_vibration: float = 0.20         # g
    vibration_wear_gain: float = 0.015
    vibration_misalignment_gain: float = 0.020


class Physics:
    """
    Ensemble des lois physiques simplifiées utilisées
    par le jumeau numérique du moteur synchrone.
    """

    params = MotorParameters()

    # ------------------------------------------------------------------
    # Température
    # ------------------------------------------------------------------

    @staticmethod
    def compute_temperature(
        current_temp,
        load,
        wear,
        cooling_efficiency,
        dt
    ):
        p = Physics.params

        delta = (
            p.thermal_load_gain * load
            + p.thermal_wear_gain * wear
            - p.thermal_cooling_gain * cooling_efficiency
        )

        new_temp = current_temp + delta * dt

        return max(
            p.ambient_temperature,
            min(new_temp, p.max_temperature)
        )

    # ------------------------------------------------------------------
    # Usure
    # ------------------------------------------------------------------

    @staticmethod
    def compute_wear(
        wear,
        load,
        dt
    ):
        p = Physics.params

        wear += p.wear_rate * load * dt

        return min(wear, 100.0)

    # ------------------------------------------------------------------
    # Vitesse
    # ------------------------------------------------------------------

    @staticmethod
    def compute_speed(load):
        p = Physics.params

        speed = (
            p.nominal_speed
            - p.speed_drop_gain * load
        )

        return max(speed, 0)

    # ------------------------------------------------------------------
    # Courant
    # ------------------------------------------------------------------

    @staticmethod
    def compute_current(
        load,
        wear
    ):
        p = Physics.params

        return (
            p.nominal_current
            + p.current_load_gain * load
            + p.current_wear_gain * wear
        )

    # ------------------------------------------------------------------
    # Couple
    # ------------------------------------------------------------------

    @staticmethod
    def compute_torque(load):
        p = Physics.params

        return (
            p.nominal_torque
            + p.torque_load_gain * load
        )

    # ------------------------------------------------------------------
    # Vibrations
    # ------------------------------------------------------------------

    @staticmethod
    def compute_vibration(
        wear,
        misalignment
    ):
        p = Physics.params

        return (
            p.nominal_vibration
            + p.vibration_wear_gain * wear
            + p.vibration_misalignment_gain * misalignment
        )

    # ------------------------------------------------------------------
    # Indice de santé (Health Index)
    # ------------------------------------------------------------------

    @staticmethod
    def compute_health_index(
        wear,
        load,
        misalignment,
        cooling_efficiency
    ):
        """
        Retourne un indice de santé compris entre 0 et 100.
        100 = moteur neuf
        0 = moteur très dégradé
        """

        health = (
            100
            - (
                0.35 * wear
                + 0.30 * misalignment
                + 0.20 * load
                + 0.15 * (100 - cooling_efficiency)
            )
        )

        return max(0, min(100, health))