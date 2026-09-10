#!/usr/bin/env python3

import csv
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from power_simulator import (
    NORMAL,
    POWER_SPIKE,
    HIGH_CONSUMPTION,
    LOW_POWER_FACTOR,
    NIGHT_ANOMALY,
    VOLTAGE_ANOMALY,
    SENSOR_FAULT,
    generate_reading
)


OUTPUT_FILE = "ai/dataset/power_consumption_dataset.csv"

SAMPLES_PER_CLASS = 1000


CONDITIONS = [
    NORMAL,
    POWER_SPIKE,
    HIGH_CONSUMPTION,
    LOW_POWER_FACTOR,
    NIGHT_ANOMALY,
    VOLTAGE_ANOMALY,
    SENSOR_FAULT
]


FIELDNAMES = [
    "timestamp",
    "hour",
    "day_of_week",
    "voltage",
    "current",
    "power",
    "power_factor",
    "frequency",
    "condition"
]


def generate_dataset():

    output_directory = os.path.dirname(OUTPUT_FILE)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    start_time = datetime(
        2026,
        1,
        1,
        0,
        0,
        0
    )

    total_samples = 0

    with open(OUTPUT_FILE, "w", newline="") as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()

        for condition in CONDITIONS:

            for sample_index in range(SAMPLES_PER_CLASS):

                timestamp = (
                    start_time +
                    timedelta(
                        minutes=15 * total_samples
                    )
                )

                reading = generate_reading(
                    condition,
                    timestamp
                )

                row = {
                    "timestamp": reading["timestamp"],
                    "hour": timestamp.hour,
                    "day_of_week": timestamp.weekday(),
                    "voltage": reading["voltage"],
                    "current": reading["current"],
                    "power": reading["power"],
                    "power_factor": reading["power_factor"],
                    "frequency": reading["frequency"],
                    "condition": reading["condition"]
                }

                writer.writerow(row)

                total_samples += 1

    print("Dataset generation complete.")
    print("Output file :", OUTPUT_FILE)
    print("Total samples:", total_samples)
    print("Samples per class:", SAMPLES_PER_CLASS)


def main():

    print("\nPOWER CONSUMPTION DATASET GENERATOR")
    print("=" * 50)

    generate_dataset()

    print("\nConditions:")
    for condition in CONDITIONS:
        print(" -", condition)


if __name__ == "__main__":
    main()
