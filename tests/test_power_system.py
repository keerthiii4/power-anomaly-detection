import os
import sys

# Add project root to Python import path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from monitoring.system_controller import PowerMonitoringSystem


def print_test(name, result):
    print("")
    print("TEST: " + name)
    print("-" * 40)

    print("Condition : " + str(result.get("condition")))
    print("Score     : " + str(result.get("anomaly_score")))
    print("Severity  : " + str(result.get("severity")))
    print("Fault     : " + str(result.get("fault")))
    print("State     : " + str(result.get("state")))
    print("Action    : " + str(result.get("action")))


def main():
    system = PowerMonitoringSystem()

    print("")
    print("POWER MONITORING SYSTEM TEST")
    print("=" * 50)

    result = system.process_reading(
        voltage=230.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_test("NORMAL READING", result)

    result = system.process_reading(
        voltage=230.0,
        current=6.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_test("HIGH CONSUMPTION", result)

    result = system.process_reading(
        voltage=230.0,
        current=8.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_test("POWER SPIKE", result)

    result = system.process_reading(
        voltage=500.0,
        current=-5.0,
        power_factor=1.5,
        frequency=70.0,
        hour=30,
        day_of_week=8
    )

    print_test("INVALID SENSOR", result)

    print("")
    print("=" * 50)
    print("POWER MONITORING SYSTEM TEST COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
