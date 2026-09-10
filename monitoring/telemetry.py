from __future__ import print_function

import os
import csv
from datetime import datetime


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

LOG_DIR = os.path.join(
    PROJECT_ROOT,
    "monitoring",
    "logs"
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "power_system_log.csv"
)


FIELD_NAMES = [
    "timestamp",
    "voltage",
    "current",
    "power_factor",
    "frequency",
    "hour",
    "day_of_week",
    "condition",
    "anomaly_score",
    "severity",
    "fault",
    "state",
    "action",
    "sensor_valid"
]


def initialize_log():

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", newline="") as log_file:

            writer = csv.DictWriter(
                log_file,
                fieldnames=FIELD_NAMES
            )

            writer.writeheader()


def record_reading(voltage, current, power_factor,
                   frequency, hour, day_of_week,
                   result):

    initialize_log()

    row = {
        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "voltage":
            "{0:.2f}".format(voltage),

        "current":
            "{0:.2f}".format(current),

        "power_factor":
            "{0:.2f}".format(power_factor),

        "frequency":
            "{0:.2f}".format(frequency),

        "hour":
            hour,

        "day_of_week":
            day_of_week,

        "condition":
            result["condition"],

        "anomaly_score":
            "{0:.2f}".format(
                result["score"]
            ),

        "severity":
            result["severity"],

        "fault":
            result["fault"],

        "state":
            result["state"],

        "action":
            result["action"],

        "sensor_valid":
            result["valid"]
    }

    with open(LOG_FILE, "a", newline="") as log_file:

        writer = csv.DictWriter(
            log_file,
            fieldnames=FIELD_NAMES
        )

        writer.writerow(row)


def read_log():

    initialize_log()

    with open(LOG_FILE, "r", newline="") as log_file:

        reader = csv.DictReader(log_file)

        rows = []

        for row in reader:
            rows.append(row)

        return rows


def print_recent_logs(count=5):

    rows = read_log()

    print("")
    print("RECENT TELEMETRY")
    print("================")

    if len(rows) == 0:
        print("No telemetry records.")
        return

    recent = rows[-count:]

    for row in recent:

        print(
            "{0} | {1:16s} | Score: {2:6s} | "
            "State: {3:10s} | Action: {4}".format(
                row["timestamp"],
                row["condition"],
                row["anomaly_score"],
                row["state"],
                row["action"]
            )
        )


def main():

    initialize_log()

    print("Telemetry log:")
    print(LOG_FILE)

    print("")
    print("Initial record count: {0}".format(
        len(read_log())
    ))

    example_result = {
        "valid": True,
        "condition": "HIGH_CONSUMPTION",
        "score": 65.0,
        "severity": "WARNING",
        "fault": "HIGH_CONSUMPTION",
        "state": "WARNING",
        "action": "WARN_USER"
    }

    record_reading(
        voltage=230.0,
        current=6.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2,
        result=example_result
    )

    print_recent_logs()


if __name__ == "__main__":
    main()
