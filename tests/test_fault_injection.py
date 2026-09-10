from __future__ import print_function

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

sys.path.insert(0, PROJECT_ROOT)

from monitoring.system_controller import PowerMonitoringSystem


def run_test(system, name, voltage, current,
             power_factor, frequency, hour, day):

    print("")
    print("TEST: {0}".format(name))
    print("----------------------------------------")

    result = system.process_reading(
        voltage=voltage,
        current=current,
        power_factor=power_factor,
        frequency=frequency,
        hour=hour,
        day_of_week=day
    )

    print("Condition : {0}".format(result["condition"]))
    print("Score     : {0:.2f}".format(result["score"]))
    print("Severity  : {0}".format(result["severity"]))
    print("Fault     : {0}".format(result["fault"]))
    print("State     : {0}".format(result["state"]))
    print("Action    : {0}".format(result["action"]))
    print("Valid     : {0}".format(result["valid"]))

    return result


def main():

    system = PowerMonitoringSystem()

    results = []

    # 1. NORMAL
    results.append(
        run_test(
            system,
            "NORMAL",
            230.0,
            2.0,
            0.95,
            50.0,
            14,
            2
        )
    )

    # 2. POWER SPIKE
    results.append(
        run_test(
            system,
            "POWER SPIKE",
            230.0,
            12.0,
            0.95,
            50.0,
            14,
            2
        )
    )

    # 3. HIGH CONSUMPTION
    results.append(
        run_test(
            system,
            "HIGH CONSUMPTION",
            230.0,
            7.0,
            0.95,
            50.0,
            14,
            2
        )
    )

    # 4. LOW POWER FACTOR
    results.append(
        run_test(
            system,
            "LOW POWER FACTOR",
            230.0,
            4.0,
            0.50,
            50.0,
            14,
            2
        )
    )

    # 5. NIGHT ANOMALY
    results.append(
        run_test(
            system,
            "NIGHT ANOMALY",
            230.0,
            8.0,
            0.95,
            50.0,
            2,
            2
        )
    )

    # 6. VOLTAGE ANOMALY
    results.append(
        run_test(
            system,
            "VOLTAGE ANOMALY",
            270.0,
            2.0,
            0.95,
            50.0,
            14,
            2
        )
    )

    # 7. SENSOR FAULT
    results.append(
        run_test(
            system,
            "SENSOR FAULT",
            500.0,
            -5.0,
            1.5,
            70.0,
            30,
            8
        )
    )

    print("")
    print("========================================")
    print("FAULT INJECTION TEST SUMMARY")
    print("========================================")

    for index, result in enumerate(results):
        print(
            "Test {0}: {1:18s} | State: {2:10s} | "
            "Action: {3}".format(
                index + 1,
                result["condition"],
                result["state"],
                result["action"]
            )
        )

    print("========================================")


if __name__ == "__main__":
    main()
