"""Manual test for the dashboard-ready maintenance payload."""

from datetime import datetime
from json import dumps
from pprint import pprint

from predictive.engine import MaintenanceEngine
from simulation.engine.simulator import SimulationEngine
from simulation.faults import FaultInjector


def setup_normal(motor):
    motor.load = 40.0
    motor.wear = 5.0
    motor.misalignment = 0.0
    motor.cooling_efficiency = 100.0


def setup_bearing_wear(motor):
    motor.load = 65.0
    motor.wear = 29.8
    motor.misalignment = 4.8
    motor.cooling_efficiency = 100.0


def setup_cooling_failure(motor):
    motor.load = 100.0
    motor.wear = 70.0
    motor.misalignment = 0.0
    motor.cooling_efficiency = 20.0


def setup_motor_overload(motor):
    motor.load = 95.0
    motor.wear = 20.0
    motor.misalignment = 0.0
    motor.cooling_efficiency = 100.0


def run_case(name, scenario, setup, cycles, expected_fault, expected_status):
    simulation = SimulationEngine(interval=1.0, api_enabled=False)
    injector = FaultInjector()
    engine = MaintenanceEngine()

    simulation.temp_sensor.noise_level = 0
    simulation.vib_sensor.noise_level = 0
    simulation.curr_sensor.noise_level = 0
    simulation.torque_sensor.noise_level = 0
    simulation.speed_sensor.noise_level = 0

    motor = simulation.motor
    motor.start()
    setup(motor)
    injector.activate(scenario)

    for _ in range(cycles):
        injector.update(motor)
        motor.update(dt=simulation.interval)

    sensor_data = simulation._read_sensors()
    analysis = engine.analyze(sensor_data)
    payload = engine.build_payload(
        motor=motor,
        simulation={
            "running": motor.running,
            "mode": "SIMULATION",
            "fault": injector.current_fault,
        },
    )

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)
    print("Payload:")
    print(dumps(payload, ensure_ascii=False, indent=2))

    try:
        datetime.fromisoformat(payload["timestamp"])
        timestamp_ok = True
    except ValueError:
        timestamp_ok = False

    checks = {
        "timestamp": timestamp_ok,
        "simulation": all(
            key in payload["simulation"]
            for key in ["running", "mode", "fault"]
        ),
        "machine": all(
            key in payload["machine"]
            for key in ["id", "name", "line"]
        ),
        "motor": all(
            key in payload["motor"]
            for key in [
                "load",
                "wear",
                "misalignment",
                "cooling_efficiency",
                "runtime",
            ]
        ),
        "sensors": all(
            key in payload["sensors"]
            for key in [
                "temperature",
                "current",
                "speed",
                "torque",
                "vibration",
            ]
        ),
        "maintenance": all(
            key in payload["maintenance"]
            for key in [
                "health",
                "status",
                "fault",
                "probability",
                "confidence",
                "recommendation",
                "rul",
                "alert",
            ]
        ),
        "fault_ok": payload["maintenance"]["fault"] == expected_fault,
        "status_ok": payload["maintenance"]["status"] == expected_status,
    }

    print("\nChecks:")
    pprint(checks)
    print("Analysis:")
    pprint(analysis)

    injector.deactivate()


if __name__ == "__main__":
    run_case(
        name="TEST 1 - NORMAL",
        scenario="NORMAL",
        setup=setup_normal,
        cycles=1,
        expected_fault="Normal",
        expected_status="NORMAL",
    )

    run_case(
        name="TEST 2 - BEARING_WEAR",
        scenario="BEARING_WEAR",
        setup=setup_bearing_wear,
        cycles=1,
        expected_fault="Bearing Wear",
        expected_status="WARNING",
    )

    run_case(
        name="TEST 3 - COOLING_FAILURE",
        scenario="COOLING_FAILURE",
        setup=setup_cooling_failure,
        cycles=18,
        expected_fault="Cooling Failure",
        expected_status="CRITICAL",
    )

    run_case(
        name="TEST 4 - MOTOR_OVERLOAD",
        scenario="MOTOR_OVERLOAD",
        setup=setup_motor_overload,
        cycles=1,
        expected_fault="Motor Overload",
        expected_status="CRITICAL",
    )
