import random
from dataclasses import dataclass
from .physics import Physics


# =========================================================
# CAPTEUR DE BASE
# =========================================================
@dataclass
class Sensor:
    noise_level: float = 0.02  # bruit de mesure (2%)

    def add_noise(self, value: float) -> float:
        noise = random.uniform(-self.noise_level, self.noise_level)
        return value * (1 + noise)


# =========================================================
# CAPTEUR TEMPERATURE
# =========================================================
class TemperatureSensor(Sensor):

    def read(self, motor):
        value = motor.internal_temperature
        return round(self.add_noise(value), 2)


# =========================================================
# CAPTEUR VIBRATION
# =========================================================
class VibrationSensor(Sensor):

    def read(self, motor):
        value = Physics.compute_vibration(
            wear=motor.wear,
            misalignment=motor.misalignment
        )
        return round(self.add_noise(value), 3)


# =========================================================
# CAPTEUR COURANT
# =========================================================
class CurrentSensor(Sensor):

    def read(self, motor):
        value = Physics.compute_current(
            load=motor.load,
            wear=motor.wear
        )
        return round(self.add_noise(value), 2)


# =========================================================
# CAPTEUR COUPLE
# =========================================================
class TorqueSensor(Sensor):

    def read(self, motor):
        value = Physics.compute_torque(
            load=motor.load
        )
        return round(self.add_noise(value), 2)


# =========================================================
# CAPTEUR VITESSE
# =========================================================
class SpeedSensor(Sensor):

    def read(self, motor):
        value = motor.speed
        return round(self.add_noise(value), 1)