from __future__ import print_function

import os
import sys
import pickle

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))

sys.path.insert(0, PROJECT_ROOT)

from ai.preprocessing.features import calculate_features


MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "ai",
    "models",
    "power_anomaly_model.pkl"
)


LABEL_NAMES = {
    0: "NORMAL",
    1: "POWER_SPIKE",
    2: "HIGH_CONSUMPTION",
    3: "LOW_POWER_FACTOR",
    4: "NIGHT_ANOMALY",
    5: "VOLTAGE_ANOMALY",
    6: "SENSOR_FAULT"
}


FEATURE_NAMES = [
    "voltage",
    "current",
    "power",
    "power_factor",
    "frequency",
    "hour",
    "day_of_week",
    "apparent_power",
    "reactive_power_estimate",
    "power_change",
    "power_ratio",
    "voltage_deviation",
    "frequency_deviation",
    "power_factor_deviation",
    "night_flag",
    "high_load_flag"
]


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise IOError(
            "Model file not found: {0}".format(MODEL_PATH)
        )

    with open(MODEL_PATH, "rb") as model_file:
        package = pickle.load(model_file)

    return package


def predict_reading(voltage, current, power_factor,
                    frequency, hour, day_of_week):
    package = load_model()

    model = package["model"]

    expected_power = get_expected_power(hour)

    features = calculate_features(
        voltage=voltage,
        current=current,
        power=voltage * current * power_factor,
        power_factor=power_factor,
        frequency=frequency,
        hour=hour,
        day_of_week=day_of_week,
        expected_power=expected_power
    )

    feature_vector = []

    for name in FEATURE_NAMES:
        feature_vector.append(features[name])

    prediction = model.predict([feature_vector])[0]

    try:
        prediction = int(prediction)
    except (TypeError, ValueError):
        pass

    condition = LABEL_NAMES.get(
        prediction,
        "UNKNOWN"
    )

    return condition, features


def get_expected_power(hour):
    if 0 <= hour < 6:
        return 130.0
    elif 6 <= hour < 9:
        return 500.0
    elif 9 <= hour < 17:
        return 425.0
    elif 17 <= hour < 22:
        return 750.0
    else:
        return 350.0


def print_prediction(condition, features):
    print("")
    print("========================================")
    print(" POWER CONSUMPTION AI INFERENCE")
    print("========================================")
    print("Predicted Condition : {0}".format(condition))
    print("")
    print("Input / Derived Features")
    print("----------------------------------------")
    print("Voltage             : {0:.2f} V".format(
        features["voltage"]
    ))
    print("Current             : {0:.2f} A".format(
        features["current"]
    ))
    print("Power               : {0:.2f} W".format(
        features["power"]
    ))
    print("Power Factor        : {0:.2f}".format(
        features["power_factor"]
    ))
    print("Frequency           : {0:.2f} Hz".format(
        features["frequency"]
    ))
    print("Power Ratio         : {0:.2f}".format(
        features["power_ratio"]
    ))
    print("Voltage Deviation   : {0:.2f} V".format(
        features["voltage_deviation"]
    ))
    print("PF Deviation        : {0:.2f}".format(
        features["power_factor_deviation"]
    ))
    print("Night Flag          : {0}".format(
        features["night_flag"]
    ))
    print("High Load Flag      : {0}".format(
        features["high_load_flag"]
    ))
    print("========================================")


def main():
    # Example 1: normal daytime consumption
    condition, features = predict_reading(
        voltage=230.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print_prediction(condition, features)

    # Example 2 can be tested by uncommenting:
    #
    # condition, features = predict_reading(
    #     voltage=230.0,
    #     current=8.0,
    #     power_factor=0.95,
    #     frequency=50.0,
    #     hour=14,
    #     day_of_week=2
    # )
    #
    # print_prediction(condition, features)


if __name__ == "__main__":
    main()
