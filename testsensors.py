from simulation.core.motor import SynchronousMotor
from simulation.core.sensors import (
    TemperatureSensor,
    VibrationSensor,
    CurrentSensor,
    TorqueSensor,
    SpeedSensor
)

motor = SynchronousMotor()
motor.start()

temp = TemperatureSensor()
vib = VibrationSensor()
curr = CurrentSensor()
torque = TorqueSensor()
speed = SpeedSensor()

print("=== TEST CAPTEURS ===")

for i in range(10):
    motor.update()

    data = {
        "temperature": temp.read(motor),
        "vibration": vib.read(motor),
        "current": curr.read(motor),
        "torque": torque.read(motor),
        "speed": speed.read(motor)
    }

    print(data)