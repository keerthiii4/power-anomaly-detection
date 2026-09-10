from __future__ import print_function


ACTION_MONITOR = "MONITOR"
ACTION_WARN = "WARN_USER"
ACTION_LIMIT_LOAD = "LIMIT_LOAD"
ACTION_PROTECT = "PROTECT_SYSTEM"
ACTION_ISOLATE = "ISOLATE_LOAD"
ACTION_SHUTDOWN = "EMERGENCY_SHUTDOWN"


def determine_protection_action(state, fault, severity_score):
    """
    Deterministic protection layer.

    AI detects the condition.
    The safety layer decides the response.
    """

    # Sensor faults are handled conservatively.
    if fault == "SENSOR_FAULT":
        return ACTION_ISOLATE

    if state == "NORMAL":
        return ACTION_MONITOR

    elif state == "WARNING":
        return ACTION_WARN

    elif state == "CRITICAL":

        if fault == "HIGH_CONSUMPTION":
            return ACTION_LIMIT_LOAD

        elif fault == "LOW_POWER_FACTOR":
            return ACTION_WARN

        elif fault == "NIGHT_ANOMALY":
            return ACTION_LIMIT_LOAD

        else:
            return ACTION_PROTECT

    elif state == "EMERGENCY":
        return ACTION_SHUTDOWN

    elif state == "RECOVERY":
        return ACTION_MONITOR

    return ACTION_PROTECT


def should_isolate_load(action):
    return action in (
        ACTION_ISOLATE,
        ACTION_SHUTDOWN
    )


def should_warn_user(action):
    return action in (
        ACTION_WARN,
        ACTION_LIMIT_LOAD,
        ACTION_PROTECT
    )


def get_protection_message(action):

    messages = {
        ACTION_MONITOR:
            "System operating normally. Continue monitoring.",

        ACTION_WARN:
            "Warning condition detected. Notify the user.",

        ACTION_LIMIT_LOAD:
            "High-risk consumption detected. Limit or reduce load.",

        ACTION_PROTECT:
            "Critical electrical condition detected. Activate protection.",

        ACTION_ISOLATE:
            "Sensor fault detected. Reject reading and isolate affected load.",

        ACTION_SHUTDOWN:
            "Emergency condition detected. Initiate emergency shutdown."
    }

    return messages.get(
        action,
        "Unknown protection action."
    )


def main():

    print("")
    print("PROTECTION LOGIC")
    print("================")

    test_cases = [
        ("NORMAL", "NO_FAULT", 0.0),
        ("WARNING", "LOW_POWER_FACTOR", 50.0),
        ("CRITICAL", "HIGH_CONSUMPTION", 75.0),
        ("CRITICAL", "POWER_SPIKE", 80.0),
        ("EMERGENCY", "VOLTAGE_ANOMALY", 95.0),
        ("EMERGENCY", "SENSOR_FAULT", 100.0)
    ]

    for state, fault, score in test_cases:

        action = determine_protection_action(
            state,
            fault,
            score
        )

        print("")
        print("State       : {0}".format(state))
        print("Fault       : {0}".format(fault))
        print("Score       : {0:.1f}".format(score))
        print("Action      : {0}".format(action))
        print("Isolate     : {0}".format(
            should_isolate_load(action)
        ))
        print("Warn User   : {0}".format(
            should_warn_user(action)
        ))
        print("Message     : {0}".format(
            get_protection_message(action)
        ))


if __name__ == "__main__":
    main()
