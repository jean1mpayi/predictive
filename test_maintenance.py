from pprint import pprint

from predictive.engine import MaintenanceEngine


engine = MaintenanceEngine()


def run_case(name, data, expected):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)
    print("Input:")
    pprint(data)

    result = engine.analyze(data)

    print("\nOutput:")
    pprint(result)

    checks = {
        "health_ok": expected["health"](result["health"]),
        "status_ok": result["status"] == expected["status"],
        "fault_ok": result["fault"] == expected["fault"],
    }

    print("\nChecks:")
    pprint(checks)

    if all(checks.values()):
        print("Result: PASS")
    else:
        print("Result: FAIL")


scenarios = [
    {
        "name": "TEST 1 : Moteur normal",
        "data": {
            "temperature": 40,
            "vibration": 0.25,
            "current": 7,
            "wear": 5,
            "load": 40,
            "torque": 14,
            "speed": 1500,
            "misalignment": 0,
        },
        "expected": {
            "health": lambda value: value > 90,
            "status": "NORMAL",
            "fault": "Normal",
        },
    },
    {
        "name": "TEST 2 : Bearing Wear",
        "data": {
            "temperature": 75,
            "vibration": 1.2,
            "current": 11,
            "wear": 65,
            "load": 50,
            "torque": 15,
            "speed": 1450,
            "misalignment": 5,
        },
        "expected": {
            "health": lambda value: 40 <= value < 90,
            "status": "WARNING",
            "fault": "Bearing Wear",
        },
    },
    {
        "name": "TEST 3 : Cooling Failure",
        "data": {
            "temperature": 100,
            "vibration": 0.4,
            "current": 13,
            "load": 70,
            "wear": 30,
            "torque": 16,
            "speed": 1480,
            "misalignment": 0,
        },
        "expected": {
            "health": lambda value: value < 70,
            "status": "CRITICAL",
            "fault": "Cooling Failure",
        },
    },
    {
        "name": "TEST 4 : Motor Overload",
        "data": {
            "temperature": 85,
            "current": 16,
            "load": 95,
            "vibration": 0.5,
            "wear": 20,
            "torque": 22,
            "speed": 1400,
            "misalignment": 0,
        },
        "expected": {
            "health": lambda value: value < 70,
            "status": "CRITICAL",
            "fault": "Motor Overload",
        },
    },
]


for scenario in scenarios:
    run_case(
        scenario["name"],
        scenario["data"],
        scenario["expected"],
    )

