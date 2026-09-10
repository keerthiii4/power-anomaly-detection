#!/usr/bin/env python3

import csv
import os


DATASET_FILE = (
    "ai/dataset/processed/"
    "power_consumption_features.csv"
)


def load_dataset():

    if not os.path.exists(DATASET_FILE):
        print("ERROR: Dataset not found.")
        print(DATASET_FILE)
        return []

    with open(DATASET_FILE, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def analyze_dataset():

    rows = load_dataset()

    if not rows:
        return

    print("\nPOWER CONSUMPTION DATASET ANALYSIS")
    print("=" * 60)

    print("Total samples :", len(rows))

    print("Total columns :", len(rows[0]))

    print("\nColumns:")

    for column in rows[0].keys():
        print(" -", column)

    # -------------------------------------------------
    # Class distribution
    # -------------------------------------------------

    class_counts = {}

    for row in rows:

        condition = row["condition"]

        if condition not in class_counts:
            class_counts[condition] = 0

        class_counts[condition] += 1

    print("\nCLASS DISTRIBUTION")
    print("-" * 60)

    for condition in sorted(class_counts.keys()):

        print(
            "{0:25s} : {1}".format(
                condition,
                class_counts[condition]
            )
        )

    # -------------------------------------------------
    # Missing values
    # -------------------------------------------------

    missing_counts = {}

    for column in rows[0].keys():

        missing_counts[column] = 0

        for row in rows:

            value = row[column]

            if value is None or value.strip() == "":
                missing_counts[column] += 1

    print("\nMISSING VALUE ANALYSIS")
    print("-" * 60)

    total_missing = 0

    for column in missing_counts:

        count = missing_counts[column]

        print(
            "{0:30s} : {1}".format(
                column,
                count
            )
        )

        total_missing += count

    print(
        "Total missing values:",
        total_missing
    )

    # -------------------------------------------------
    # Numeric ranges
    # -------------------------------------------------

    numeric_columns = [
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

    print("\nNUMERIC FEATURE RANGES")
    print("-" * 60)

    for column in numeric_columns:

        values = []

        for row in rows:

            try:
                values.append(
                    float(row[column])
                )
            except ValueError:
                pass

        if values:

            print(
                "{0:30s} min={1:.3f} max={2:.3f}".format(
                    column,
                    min(values),
                    max(values)
                )
            )

    # -------------------------------------------------
    # Average power by condition
    # -------------------------------------------------

    print("\nAVERAGE POWER BY CONDITION")
    print("-" * 60)

    power_data = {}

    for row in rows:

        condition = row["condition"]
        power = float(row["power"])

        if condition not in power_data:
            power_data[condition] = []

        power_data[condition].append(power)

    for condition in sorted(power_data.keys()):

        values = power_data[condition]

        average = sum(values) / len(values)

        print(
            "{0:25s} : {1:.2f} W".format(
                condition,
                average
            )
        )

    # -------------------------------------------------
    # Average electrical parameters
    # -------------------------------------------------

    print("\nAVERAGE ELECTRICAL PARAMETERS")
    print("-" * 60)

    parameter_columns = [
        "voltage",
        "current",
        "power_factor",
        "frequency"
    ]

    for condition in sorted(class_counts.keys()):

        condition_rows = [
            row for row in rows
            if row["condition"] == condition
        ]

        print("\n" + condition)

        for column in parameter_columns:

            values = [
                float(row[column])
                for row in condition_rows
            ]

            average = sum(values) / len(values)

            print(
                "  {0:20s}: {1:.3f}".format(
                    column,
                    average
                )
            )

    # -------------------------------------------------
    # Final validation
    # -------------------------------------------------

    expected_samples = 7000
    expected_classes = 7

    print("\nDATASET VALIDATION")
    print("-" * 60)

    if len(rows) == expected_samples:
        print("PASS: Sample count is 7000")
    else:
        print(
            "FAIL: Expected 7000 samples, got {0}".format(
                len(rows)
            )
        )

    if len(class_counts) == expected_classes:
        print("PASS: Seven classes found")
    else:
        print(
            "FAIL: Expected 7 classes, got {0}".format(
                len(class_counts)
            )
        )

    if total_missing == 0:
        print("PASS: No missing values")
    else:
        print("FAIL: Missing values detected")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    analyze_dataset()
