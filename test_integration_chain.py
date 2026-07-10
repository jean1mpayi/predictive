"""Manual integration test for the full simulation-to-maintenance chain."""

from pprint import pprint

from api.services.maintenance import MaintenanceEngine
from simulation.engine.simulator import SimulationEngine
from simulation.faults import FaultInjector


def round_result(result):
    """Round floating values for readable console output."""

    return {
        "health": result["health"],
        "status": result["status"],
        "fault": result["fault"],
        "probability": result["probability"],
        "rul": {
            "hours": result["rul"]["hours"],
            "days": result["rul"]["days"],
            "condition": result["rul"]["condition"],
        },
        "alert": result["alert"],
        "recommendation": result["recommendation"],
    }


def snapshot_motor(motor):
    """Capture the internal motor state and physical outputs."""

    return {
        "running": motor.running,
        "load": round(motor.load, 2),
        "wear": round(motor.wear, 2),
        "misalignment": round(motor.misalignment, 2),
        "cooling_efficiency": round(motor.cooling_efficiency, 2),
        "internal_temperature": round(motor.internal_temperature, 2),
        "speed": round(motor.speed, 2),
        "current": round(motor.current, 2),
        "torque": round(motor.torque, 2),
        "vibration": round(motor.vibration, 3),
        "runtime": round(motor.runtime, 2),
    }


def run_chain_case(name, scenario, setup=None, cycles=1):
    """Execute one manual end-to-end simulation case."""

    simulation = SimulationEngine(interval=1.0, api_enabled=False)
    injector = FaultInjector()
    maintenance = MaintenanceEngine()

    # Keep the run deterministic for manual validation.
    simulation.temp_sensor.noise_level = 0
    simulation.vib_sensor.noise_level = 0
    simulation.curr_sensor.noise_level = 0
    simulation.torque_sensor.noise_level = 0
    simulation.speed_sensor.noise_level = 0

    motor = simulation.motor
    motor.start()

    if setup:
        setup(motor)

    injector.activate(scenario)

    for _ in range(cycles):
        injector.update(motor)
        motor.update(dt=simulation.interval)

    sensor_data = simulation._read_sensors()
    analysis = maintenance.analyze(sensor_data)

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print("Motor state:")
    pprint(snapshot_motor(motor))
    print("\nSensor data:")
    pprint(sensor_data)
    print("\nMaintenance analysis:")
    pprint(round_result(analysis))

    injector.deactivate()


def setup_bearing_wear(motor):
    motor.load = 65.0
    motor.wear = 29.8
    motor.misalignment = 4.8
    motor.cooling_efficiency = 100.0


def setup_cooling_failure(motor):
    motor.load = 70.0
    motor.wear = 20.0
    motor.misalignment = 0.0
    motor.cooling_efficiency = 0.0


def setup_rotor_misalignment(motor):
    motor.load = 40.0
    motor.wear = 10.0
    motor.misalignment = 40.0
    motor.cooling_efficiency = 100.0


if __name__ == "__main__":
    run_chain_case(
        name="TEST 1 - NORMAL",
        scenario="NORMAL",
        cycles=1,
        setup=None,
    )

    run_chain_case(
        name="TEST 2 - BEARING_WEAR",
        scenario="BEARING_WEAR",
        cycles=1,
        setup=setup_bearing_wear,
    )

    run_chain_case(
        name="TEST 3 - COOLING_FAILURE",
        scenario="COOLING_FAILURE",
        cycles=35,
        setup=setup_cooling_failure,
    )

    run_chain_case(
        name="TEST 4 - ROTOR_MISALIGNMENT",
        scenario="ROTOR_MISALIGNMENT",
        cycles=1,
        setup=setup_rotor_misalignment,
    )
