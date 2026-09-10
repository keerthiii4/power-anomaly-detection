import sys
import os
import csv

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from ai.inference.predict import predict_reading
from detection.anomaly_score import calculate_anomaly_score


OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "ai_output.csv"
)


def generate_ai_output(voltage, current, power_factor,
                       frequency, hour, day_of_week):

    condition, features = predict_reading(
        voltage,
        current,
        power_factor,
        frequency,
        hour,
        day_of_week
    )

    score = calculate_anomaly_score(
        condition,
        features
    )

    with open(OUTPUT_FILE, "w") as file_handle:

        writer = csv.writer(file_handle)

        writer.writerow([
            "voltage",
            "current",
            "power_factor",
            "frequency",
            "hour",
            "day_of_week",
            "condition",
            "anomaly_score"
        ])

        writer.writerow([
            voltage,
            current,
            power_factor,
            frequency,
            hour,
            day_of_week,
            condition,
            score
        ])

    print("AI output generated")
    print("Condition:", condition)
    print("Anomaly Score:", "%.2f" % score)
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":

    generate_ai_output(
        230.0,
        2.0,
        0.95,
        50.0,
        14,
        2
    )
