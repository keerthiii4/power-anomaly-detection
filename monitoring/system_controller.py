from __future__ import print_function

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

sys.path.insert(0, PROJECT_ROOT)

from safety.sensor_validation import validate_sensor_reading
from ai.inference.predict import predict_reading
from detection.anomaly_score import calculate_anomaly_score
from safety.fault_manager import create_fault
from safety.state_machine import SafetyStateMachine
from safety.protection_logic import (
    determine_protection_action,
    get_protection_message
)
from monitoring.telemetry import record_reading


class PowerMonitoringSystem(object):

    def __init__(self):
        self.state_machine = SafetyStateMachine()

    def process_reading(self, voltage, current,
                        power_factor, frequency,
                        hour, day_of_week):

        validation = validate_sensor_reading(
            voltage=voltage,
            current=current,
            power_factor=power_factor,
            frequency=frequency,
            hour=hour,
            day_of_week=day_of_week
        )

        # -------------------------------------------------
        # INVALID SENSOR DATA
        # -------------------------------------------------
        if not validation["valid"]:

            fault_result = create_fault(
                condition="SENSOR_FAULT",
                severity_score=100.0,
                validation_errors=validation["errors"]
            )

            state = self.state_machine.update(
                severity_score=100.0,
                sensor_valid=False
            )

            action = determine_protection_action(
                state=state,
                fault=fault_result["fault"],
                severity_score=100.0
            )

            result = {
                "valid": False,
                "condition": "SENSOR_FAULT",
                "score": 100.0,
                "severity": "EMERGENCY",
                "fault": fault_result["fault"],
                "state": state,
                "action": action,
                "message": get_protection_message(action),
                "validation_errors": validation["errors"]
            }

            record_reading(
                voltage,
                current,
                power_factor,
                frequency,
                hour,
                day_of_week,
                result
            )

            return result

        # -------------------------------------------------
        # AI INFERENCE
        # -------------------------------------------------
        condition, features = predict_reading(
            voltage=voltage,
            current=current,
            power_factor=power_factor,
            frequency=frequency,
            hour=hour,
            day_of_week=day_of_week
        )

        # -------------------------------------------------
        # ANOMALY SEVERITY
        # -------------------------------------------------
        score = calculate_anomaly_score(
            condition,
            features
        )

        # -------------------------------------------------
        # FAULT MANAGEMENT
        # -------------------------------------------------
        fault_result = create_fault(
            condition=condition,
            severity_score=score
        )

        # -------------------------------------------------
        # STATE MACHINE
        # -------------------------------------------------
        state = self.state_machine.update(
            severity_score=score,
            sensor_valid=True
        )

        # -------------------------------------------------
        # PROTECTION LOGIC
        # -------------------------------------------------
        action = determine_protection_action(
            state=state,
            fault=fault_result["fault"],
            severity_score=score
        )

        result = {
            "valid": True,
            "condition": condition,
            "score": score,
            "severity": self._get_severity(score),
            "fault": fault_result["fault"],
            "state": state,
            "action": action,
            "message": get_protection_message(action),
            "validation_errors": []
        }

        # -------------------------------------------------
        # TELEMETRY
        # -------------------------------------------------
        record_reading(
            voltage,
            current,
            power_factor,
            frequency,
            hour,
            day_of_week,
            result
        )

        return result

    def _get_severity(self, score):

        if score <= 0:
            return "NORMAL"

        elif score < 40:
            return "LOW"

        elif score < 70:
            return "WARNING"

        elif score < 90:
            return "CRITICAL"

        return "EMERGENCY"


def print_result(result):

    print("")
    print("========================================")
    print(" POWER MONITORING SYSTEM")
    print("========================================")
    print("Sensor Valid       : {0}".format(
        result["valid"]
    ))
    print("Condition          : {0}".format(
        result["condition"]
    ))
    print("Anomaly Score      : {0:.1f}".format(
        result["score"]
    ))
    print("Severity           : {0}".format(
        result["severity"]
    ))
    print("Fault              : {0}".format(
        result["fault"]
    ))
    print("System State       : {0}".format(
        result["state"]
    ))
    print("Protection Action  : {0}".format(
        result["action"]
    ))
    print("Message            : {0}".format(
        result["message"]
    ))

    if result["validation_errors"]:
        print("Validation Errors  : {0}".format(
            result["validation_errors"]
        ))

    print("========================================")


def main():

    system = PowerMonitoringSystem()

    print("")
    print("TEST 1: NORMAL READING")

    result = system.process_reading(
        voltage=230.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_result(result)

    print("")
    print("TEST 2: HIGH CONSUMPTION")

    result = system.process_reading(
        voltage=230.0,
        current=8.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_result(result)

    print("")
    print("TEST 3: INVALID SENSOR READING")

    result = system.process_reading(
        voltage=500.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_result(result)


if __name__ == "__main__":
    main()
