"""Manual test script for the fault injection package.

Run this file directly to inspect how each scenario changes the motor's
internal state after one simulation cycle.
"""

from pprint import pprint

from simulation.core.motor import SynchronousMotor
from simulation.faults import FaultInjector


def snapshot(motor):
    return {
        "running": motor.running,
        "load": round(motor.load, 2),
        "wear": round(motor.wear, 2),
        "misalignment": round(motor.misalignment, 2),
        "cooling_efficiency": round(motor.cooling_efficiency, 2),
        "temperature": round(motor.internal_temperature, 2),
        "speed": round(motor.speed, 2),
        "current": round(motor.current, 2),
        "torque": round(motor.torque, 2),
        "vibration": round(motor.vibration, 2),
    }


def run_case(name, scenario, expected):
    motor = SynchronousMotor()
    injector = FaultInjector()

    print("\n" + "=" * 72)
    print(name)
    print("=" * 72)

    print("Before:")
    pprint(snapshot(motor))

    injector.activate(scenario)
    injector.update(motor)

    print("\nAfter 1 update:")
    pprint(snapshot(motor))

    print("\nExpected:")
    pprint(expected)

    injector.deactivate()


if __name__ == "__main__":
    run_case(
        "TEST 1 - NORMAL",
        "NORMAL",
        {
            "active": False,
            "current_fault": "NORMAL",
            "load": 40.00,
            "wear": 5.00,
            "misalignment": 0.00,
            "cooling_efficiency": 100.00,
        },
    )

    run_case(
        "TEST 2 - BEARING_WEAR",
        "BEARING_WEAR",
        {
            "active": True,
            "current_fault": "BEARING_WEAR",
            "load": 40.00,
            "wear": 5.20,
            "misalignment": 0.01,
            "cooling_efficiency": 100.00,
        },
    )

    run_case(
        "TEST 3 - COOLING_FAILURE",
        "COOLING_FAILURE",
        {
            "active": True,
            "current_fault": "COOLING_FAILURE",
            "load": 40.00,
            "wear": 5.00,
            "misalignment": 0.00,
            "cooling_efficiency": 99.50,
        },
    )

    run_case(
        "TEST 4 - MOTOR_OVERLOAD",
        "MOTOR_OVERLOAD",
        {
            "active": True,
            "current_fault": "MOTOR_OVERLOAD",
            "load": 40.50,
            "wear": 5.00,
            "misalignment": 0.00,
            "cooling_efficiency": 100.00,
        },
    )

    run_case(
        "TEST 5 - ROTOR_MISALIGNMENT",
        "ROTOR_MISALIGNMENT",
        {
            "active": True,
            "current_fault": "ROTOR_MISALIGNMENT",
            "load": 40.00,
            "wear": 5.00,
            "misalignment": 0.05,
            "cooling_efficiency": 100.00,
        },
    )

    run_case(
        "TEST 6 - ELECTRICAL_FAULT",
        "ELECTRICAL_FAULT",
        {
            "active": True,
            "current_fault": "ELECTRICAL_FAULT",
            "load": 40.20,
            "wear": 5.00,
            "misalignment": 0.02,
            "cooling_efficiency": 100.00,
        },
    )

    run_case(
        "TEST 7 - POWER_LOSS",
        "POWER_LOSS",
        {
            "active": True,
            "current_fault": "POWER_LOSS",
            "load": 39.00,
            "wear": 5.00,
            "misalignment": 0.00,
            "cooling_efficiency": 100.00,
        },
    )

