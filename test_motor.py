from simulation.core.motor import SynchronousMotor
import time

motor = SynchronousMotor()

motor.start()

print("=== TEST MOTEUR ===")

for i in range(10):
    motor.update(dt=1)

    print(f"""
    t={motor.runtime}
    load={motor.load}
    wear={motor.wear:.2f}
    temp={motor.internal_temperature:.2f}
    speed={motor.speed:.2f}
    health={motor.health_index:.2f}
    """)

    time.sleep(0.5)

motor.stop()