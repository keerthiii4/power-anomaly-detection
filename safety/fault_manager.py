from __future__ import print_function


FAULT_NONE = "NO_FAULT"
FAULT_SENSOR = "SENSOR_FAULT"
FAULT_POWER_SPIKE = "POWER_SPIKE"
FAULT_HIGH_CONSUMPTION = "HIGH_CONSUMPTION"
FAULT_LOW_POWER_FACTOR = "LOW_POWER_FACTOR"
FAULT_NIGHT_ANOMALY = "NIGHT_ANOMALY"
FAULT_VOLTAGE = "VOLTAGE_ANOMALY"
FAULT_UNKNOWN = "UNKNOWN_FAULT"


FAULT_PRIORITY = {
    FAULT_NONE: 0,
    FAULT_LOW_POWER_FACTOR: 1,
    FAULT_HIGH_CONSUMPTION: 2,
    FAULT_NIGHT_ANOMALY: 3,
    FAULT_POWER_SPIKE: 4,
    FAULT_VOLTAGE: 5,
    FAULT_SENSOR: 6,
    FAULT_UNKNOWN: 1
}


def classify_fault(condition):
    if condition == "NORMAL":
        return FAULT_NONE

    elif condition == "POWER_SPIKE":
        return FAULT_POWER_SPIKE

    elif condition == "HIGH_CONSUMPTION":
        return FAULT_HIGH_CONSUMPTION

    elif condition == "LOW_POWER_FACTOR":
        return FAULT_LOW_POWER_FACTOR

    elif condition == "NIGHT_ANOMALY":
        return FAULT_NIGHT_ANOMALY

    elif condition == "VOLTAGE_ANOMALY":
        return FAULT_VOLTAGE

    elif condition == "SENSOR_FAULT":
        return FAULT_SENSOR

    return FAULT_UNKNOWN


def get_priority(fault):
    return FAULT_PRIORITY.get(
        fault,
        FAULT_PRIORITY[FAULT_UNKNOWN]
    )


def create_fault(condition, severity_score=0.0,
                 validation_errors=None):

    if validation_errors is None:
        validation_errors = []

    # Sensor validation has highest priority.
    if len(validation_errors) > 0:
        fault = FAULT_SENSOR
    else:
        fault = classify_fault(condition)

    priority = get_priority(fault)

    return {
        "fault": fault,
        "priority": priority,
        "severity_score": severity_score,
        "validation_errors": validation_errors
    }


def is_critical_fault(fault):
    return fault in (
        FAULT_SENSOR,
        FAULT_VOLTAGE,
        FAULT_POWER_SPIKE
    )


def get_fault_action(fault):
    if fault == FAULT_NONE:
        return "CONTINUE_NORMAL_OPERATION"

    elif fault == FAULT_LOW_POWER_FACTOR:
        return "MONITOR_AND_WARN"

    elif fault == FAULT_HIGH_CONSUMPTION:
        return "REDUCE_LOAD_OR_WARN"

    elif fault == FAULT_NIGHT_ANOMALY:
        return "ALERT_USER"

    elif fault == FAULT_POWER_SPIKE:
        return "PROTECT_LOAD"

    elif fault == FAULT_VOLTAGE:
        return "PROTECT_SYSTEM"

    elif fault == FAULT_SENSOR:
        return "REJECT_READING"

    return "RAISE_SYSTEM_ALERT"


def main():

    print("")
    print("FAULT MANAGER")
    print("=============")

    test_conditions = [
        "NORMAL",
        "LOW_POWER_FACTOR",
        "HIGH_CONSUMPTION",
        "POWER_SPIKE",
        "VOLTAGE_ANOMALY",
        "SENSOR_FAULT"
    ]

    for condition in test_conditions:

        if condition == "SENSOR_FAULT":
            result = create_fault(
                condition=condition,
                severity_score=100.0,
                validation_errors=["INVALID_VOLTAGE"]
            )
        else:
            result = create_fault(
                condition=condition,
                severity_score=60.0
            )

        action = get_fault_action(
            result["fault"]
        )

        print("")
        print("Condition : {0}".format(condition))
        print("Fault     : {0}".format(result["fault"]))
        print("Priority  : {0}".format(result["priority"]))
        print("Score     : {0:.1f}".format(
            result["severity_score"]
        ))
        print("Critical  : {0}".format(
            is_critical_fault(result["fault"])
        ))
        print("Action    : {0}".format(action))


if __name__ == "__main__":
    main()
