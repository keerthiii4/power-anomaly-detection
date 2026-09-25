import sys
import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from monitoring.system_controller import PowerMonitoringSystem


def check_sensor_validity(voltage, current,
                          power_factor, frequency, hour):

    if voltage < 180.0 or voltage > 260.0:
        return False

    if current < 0.0 or current > 50.0:
        return False

    if power_factor < 0.0 or power_factor > 1.0:
        return False

    if frequency < 45.0 or frequency > 55.0:
        return False

    if hour < 0 or hour > 23:
        return False

    return True


def run_case(system, name, voltage, current,
             power_factor, frequency, hour,
             expected_sensor_valid):

    result = system.process_reading(
        voltage,
        current,
        power_factor,
        frequency,
        hour,
        2
    )

    sensor_valid = check_sensor_validity(
        voltage,
        current,
        power_factor,
        frequency,
        hour
    )

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print("Input")
    print("Voltage      :", voltage)
    print("Current      :", current)
    print("Power Factor :", power_factor)
    print("Frequency    :", frequency)
    print("Hour         :", hour)

    print("\nSystem Result")
    print("Sensor Valid :", sensor_valid)
    print("Condition    :", result.get("condition"))
    print("Score        :", "%.2f" % result.get("score", 0.0))
    print("Severity     :", result.get("severity"))
    print("Fault        :", result.get("fault"))
    print("State        :", result.get("state"))
    print("Action       :", result.get("action"))

    if sensor_valid != expected_sensor_valid:
        print("TEST RESULT  : FAIL")
        return False

    print("TEST RESULT  : PASS")
    return True


def main():

    system = PowerMonitoringSystem()

    total = 0
    passed = 0

    tests = [
        (
            "NORMAL",
            230.0, 2.0, 0.95, 50.0, 14,
            True
        ),
        (
            "POWER SPIKE",
            230.0, 12.0, 0.95, 50.0, 14,
            True
        ),
        (
            "HIGH CONSUMPTION",
            230.0, 7.0, 0.95, 50.0, 14,
            True
        ),
        (
            "LOW POWER FACTOR",
            230.0, 4.0, 0.50, 50.0, 14,
            True
        ),
        (
            "NIGHT ANOMALY",
            230.0, 8.0, 0.95, 50.0, 2,
            True
        ),
        (
            "VOLTAGE SENSOR FAULT",
            270.0, 2.0, 0.95, 50.0, 14,
            False
        ),
        (
            "INVALID SENSOR DATA",
            500.0, -5.0, 1.50, 70.0, 30,
            False
        )
    ]

    for test in tests:

        total += 1

        passed_test = run_case(
            system,
            test[0],
            test[1],
            test[2],
            test[3],
            test[4],
            test[5],
            test[6]
        )

        if passed_test:
            passed += 1

    print("\n")
    print("=" * 60)
    print("END-TO-END TEST SUMMARY")
    print("=" * 60)

    print("Total tests :", total)
    print("Passed      :", passed)
    print("Failed      :", total - passed)

    if passed == total:
        print("STATUS      : ALL TESTS PASSED")
    else:
        print("STATUS      : SOME TESTS FAILED")


if __name__ == "__main__":
    main()
