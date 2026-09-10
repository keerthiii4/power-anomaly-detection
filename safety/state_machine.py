from __future__ import print_function


STATE_NORMAL = "NORMAL"
STATE_WARNING = "WARNING"
STATE_CRITICAL = "CRITICAL"
STATE_EMERGENCY = "EMERGENCY"
STATE_RECOVERY = "RECOVERY"


class SafetyStateMachine(object):

    def __init__(self):
        self.state = STATE_NORMAL
        self.previous_state = STATE_NORMAL

    def update(self, severity_score, sensor_valid=True):

        self.previous_state = self.state

        # Invalid sensor data has highest priority.
        if not sensor_valid:
            self.state = STATE_EMERGENCY

        elif severity_score >= 90:
            self.state = STATE_EMERGENCY

        elif severity_score >= 70:
            self.state = STATE_CRITICAL

        elif severity_score >= 40:
            self.state = STATE_WARNING

        elif self.state != STATE_NORMAL:
            self.state = STATE_RECOVERY

        else:
            self.state = STATE_NORMAL

        return self.state

    def reset(self):
        self.previous_state = self.state
        self.state = STATE_NORMAL

    def get_state(self):
        return self.state

    def get_previous_state(self):
        return self.previous_state

    def has_state_changed(self):
        return self.state != self.previous_state


def get_state_action(state):

    if state == STATE_NORMAL:
        return "CONTINUE_MONITORING"

    elif state == STATE_WARNING:
        return "ISSUE_WARNING"

    elif state == STATE_CRITICAL:
        return "PROTECT_SYSTEM"

    elif state == STATE_EMERGENCY:
        return "SHUTDOWN_OR_ISOLATE_LOAD"

    elif state == STATE_RECOVERY:
        return "VERIFY_AND_RESUME"

    return "UNKNOWN_ACTION"


def main():

    print("")
    print("SAFETY STATE MACHINE")
    print("====================")

    state_machine = SafetyStateMachine()

    test_scores = [
        0,
        20,
        50,
        75,
        95,
        20,
        0
    ]

    for score in test_scores:

        state = state_machine.update(
            severity_score=score,
            sensor_valid=True
        )

        print(
            "Score: {0:5.1f} | Previous: {1:10s} | "
            "Current: {2:10s} | Action: {3}".format(
                score,
                state_machine.get_previous_state(),
                state,
                get_state_action(state)
            )
        )

    print("")
    print("Testing invalid sensor condition...")

    state = state_machine.update(
        severity_score=0,
        sensor_valid=False
    )

    print(
        "Invalid sensor -> State: {0} | Action: {1}".format(
            state,
            get_state_action(state)
        )
    )


if __name__ == "__main__":
    main()
