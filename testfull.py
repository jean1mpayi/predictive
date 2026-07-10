from simulation.engine.simulator import SimulationEngine
import time

engine = SimulationEngine(interval=1)

print("=== TEST SIMULATION ENGINE ===")

engine.start()

try:
    time.sleep(100)  # laisser tourner 100 secondes
finally:
    engine.stop()