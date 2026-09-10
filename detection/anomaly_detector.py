from __future__ import print_function

import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

sys.path.insert(0, PROJECT_ROOT)

from ai.inference.predict import predict_reading


def detect_anomaly(voltage, current, power_factor,
                   frequency, hour, day_of_week):

    condition, features = predict_reading(
        voltage=voltage,
        current=current,
        power_factor=power_factor,
        frequency=frequency,
        hour=hour,
        day_of_week=day_of_week
    )

    if condition == "NORMAL":
        is_anomaly = False
    else:
        is_anomaly = True

    result = {
        "condition": condition,
        "is_anomaly": is_anomaly,
        "features": features
    }

    return result


def main():

    print("")
    print("POWER ANOMALY DETECTOR")
    print("======================")

    result = detect_anomaly(
        voltage=230.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print("Condition : {0}".format(
        result["condition"]
    ))

    print("Anomaly   : {0}".format(
        result["is_anomaly"]
    ))


if __name__ == "__main__":
    main()
