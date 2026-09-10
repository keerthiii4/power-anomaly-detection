#!/usr/bin/env python3

import csv
import os
import sys


CURRENT_DIRECTORY = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(
    0,
    CURRENT_DIRECTORY
)

from features import calculate_features


INPUT_FILE = "ai/dataset/power_consumption_dataset.csv"

OUTPUT_DIRECTORY = "ai/dataset/processed"

OUTPUT_FILE = (
    "ai/dataset/processed/"
    "power_consumption_features.csv"
)


LABEL_MAP = {
    "NORMAL": 0,
    "POWER_SPIKE": 1,
    "HIGH_CONSUMPTION": 2,
    "LOW_POWER_FACTOR": 3,
    "NIGHT_ANOMALY": 4,
    "VOLTAGE_ANOMALY": 5,
    "SENSOR_FAULT": 6
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


OUTPUT_FIELDS = FEATURE_NAMES + [
    "condition",
    "label"
]


def estimate_expected_power(hour):
    """
    Estimate expected consumption using
    the same time-of-day ranges used by
    the simulator.

    A deterministic midpoint is used here
    so that preprocessing remains repeatable.
    """

    if 0 <= hour < 6:
        return 130.0

    if 6 <= hour < 9:
        return 500.0

    if 9 <= hour < 17:
        return 425.0

    if 17 <= hour < 22:
        return 750.0

    return 350.0


def prepare_dataset():

    if not os.path.exists(INPUT_FILE):

        print(
            "ERROR: Input dataset not found:"
        )

        print(INPUT_FILE)

        return False

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    processed_count = 0

    with open(
        INPUT_FILE,
        "r"
    ) as input_file:

        reader = csv.DictReader(
            input_file
        )

        with open(
            OUTPUT_FILE,
            "w",
            newline=""
        ) as output_file:

            writer = csv.DictWriter(
                output_file,
                fieldnames=OUTPUT_FIELDS
            )

            writer.writeheader()

            for row in reader:

                voltage = float(
                    row["voltage"]
                )

                current = float(
                    row["current"]
                )

                power = float(
                    row["power"]
                )

                power_factor = float(
                    row["power_factor"]
                )

                frequency = float(
                    row["frequency"]
                )

                hour = int(
                    row["hour"]
                )

                day_of_week = int(
                    row["day_of_week"]
                )

                condition = row[
                    "condition"
                ]

                expected_power = (
                    estimate_expected_power(
                        hour
                    )
                )

                features = calculate_features(
                    voltage,
                    current,
                    power,
                    power_factor,
                    frequency,
                    hour,
                    day_of_week,
                    expected_power
                )

                output_row = {}

                for feature_name in FEATURE_NAMES:

                    output_row[
                        feature_name
                    ] = features[
                        feature_name
                    ]

                output_row[
                    "condition"
                ] = condition

                output_row[
                    "label"
                ] = LABEL_MAP[
                    condition
                ]

                writer.writerow(
                    output_row
                )

                processed_count += 1

    print(
        "Dataset preprocessing complete."
    )

    print(
        "Input file    : {0}".format(
            INPUT_FILE
        )
    )

    print(
        "Output file   : {0}".format(
            OUTPUT_FILE
        )
    )

    print(
        "Processed rows: {0}".format(
            processed_count
        )
    )

    print(
        "Features      : {0}".format(
            len(FEATURE_NAMES)
        )
    )

    print("\nLabel mapping:")

    for condition, label in LABEL_MAP.items():

        print(
            "  {0} -> {1}".format(
                label,
                condition
            )
        )

    return True


if __name__ == "__main__":

    success = prepare_dataset()

    if not success:
        sys.exit(1)
