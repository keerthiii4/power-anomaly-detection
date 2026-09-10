import os
import csv
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

LOG_FILE = os.path.join(
    PROJECT_ROOT,
    "monitoring",
    "logs",
    "power_system_log.csv"
)


def read_logs():
    if not os.path.exists(LOG_FILE):
        return []

    rows = []

    with open(LOG_FILE, "r") as file_handle:
        reader = csv.DictReader(file_handle)

        for row in reader:
            rows.append(row)

    return rows


def print_header():
    print("\n")
    print("=" * 80)
    print("        AI-BASED POWER CONSUMPTION ANOMALY DETECTION")
    print("=" * 80)


def print_latest(rows):
    if not rows:
        print("\nNo telemetry records available.")
        return

    latest = rows[-1]

    print("\nLATEST SYSTEM STATUS")
    print("-" * 80)

    print("Timestamp      :", latest.get("timestamp"))
    print("Voltage        :", latest.get("voltage"), "V")
    print("Current        :", latest.get("current"), "A")
    print("Power Factor   :", latest.get("power_factor"))
    print("Frequency      :", latest.get("frequency"), "Hz")
    print("Hour           :", latest.get("hour"))
    print("Day            :", latest.get("day_of_week"))
    print("Condition      :", latest.get("condition"))
    print("Anomaly Score  :", latest.get("anomaly_score"))
    print("Severity       :", latest.get("severity"))
    print("Fault          :", latest.get("fault"))
    print("Safety State   :", latest.get("state"))
    print("Action         :", latest.get("action"))
    print("Sensor Valid   :", latest.get("sensor_valid"))


def print_summary(rows):
    if not rows:
        return

    normal = 0
    warning = 0
    critical = 0
    emergency = 0

    for row in rows:

        severity = row.get("severity")

        if severity == "NORMAL":
            normal += 1

        elif severity == "WARNING":
            warning += 1

        elif severity == "CRITICAL":
            critical += 1

        elif severity == "EMERGENCY":
            emergency += 1

    print("\nSYSTEM SUMMARY")
    print("-" * 80)

    print("Total readings :", len(rows))
    print("Normal         :", normal)
    print("Warning        :", warning)
    print("Critical       :", critical)
    print("Emergency      :", emergency)


def print_recent(rows, count=10):
    if not rows:
        return

    print("\nRECENT TELEMETRY")
    print("-" * 80)

    recent = rows[-count:]

    print(
        "%-20s %-10s %-10s %-18s %-10s %-12s" %
        (
            "Timestamp",
            "Power",
            "Score",
            "Condition",
            "State",
            "Action"
        )
    )

    print("-" * 80)

    for row in recent:

        voltage = float(row.get("voltage", 0.0))
        current = float(row.get("current", 0.0))
        pf = float(row.get("power_factor", 0.0))

        power = voltage * current * pf

        print(
            "%-20s %-10.2f %-10s %-18s %-10s %-12s" %
            (
                row.get("timestamp", "")[:20],
                power,
                row.get("anomaly_score", ""),
                row.get("condition", ""),
                row.get("state", ""),
                row.get("action", "")
            )
        )


def main():

    rows = read_logs()

    print_header()

    print_latest(rows)

    print_summary(rows)

    print_recent(rows)

    print("\nLog file:")
    print(LOG_FILE)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
