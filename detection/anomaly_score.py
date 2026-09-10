from __future__ import print_function


def calculate_anomaly_score(condition, features):
    """
    Calculate a deterministic anomaly severity score from 0 to 100.

    ML detects the abnormal condition.
    This layer estimates severity using engineering rules.
    """

    if condition == "NORMAL":
        return 0.0

    score = 0.0

    power_ratio = features.get("power_ratio", 1.0)
    voltage_deviation = abs(
        features.get("voltage_deviation", 0.0)
    )
    frequency_deviation = abs(
        features.get("frequency_deviation", 0.0)
    )
    pf_deviation = abs(
        features.get("power_factor_deviation", 0.0)
    )

    if condition == "POWER_SPIKE":
        score = 50.0 + min(
            max(power_ratio - 3.0, 0.0) * 10.0,
            30.0
        )

    elif condition == "HIGH_CONSUMPTION":
        score = 40.0 + min(
            max(power_ratio - 2.0, 0.0) * 15.0,
            30.0
        )

    elif condition == "LOW_POWER_FACTOR":
        score = 40.0 + min(
            pf_deviation * 100.0,
            40.0
        )

    elif condition == "NIGHT_ANOMALY":
        score = 70.0 + min(
            max(power_ratio - 5.0, 0.0) * 5.0,
            20.0
        )

    elif condition == "VOLTAGE_ANOMALY":
        score = 60.0 + min(
            max(voltage_deviation - 20.0, 0.0) * 1.5,
            30.0
        )

    elif condition == "SENSOR_FAULT":
        score = 100.0

    else:
        score = 50.0

    if frequency_deviation > 1.0:
        score += 10.0

    if score > 100.0:
        score = 100.0

    return score


def get_severity_level(score):
    """
    Convert numerical severity into a system-level severity.
    """

    if score <= 0:
        return "NORMAL"

    elif score < 40:
        return "LOW"

    elif score < 70:
        return "WARNING"

    elif score < 90:
        return "CRITICAL"

    else:
        return "EMERGENCY"


def analyze_anomaly(condition, features):
    score = calculate_anomaly_score(
        condition,
        features
    )

    severity = get_severity_level(score)

    return {
        "condition": condition,
        "score": score,
        "severity": severity
    }


def main():

    print("")
    print("ANOMALY SEVERITY SCORING")
    print("========================")

    examples = [
        ("NORMAL", {
            "power_ratio": 1.0,
            "voltage_deviation": 0.0,
            "frequency_deviation": 0.0,
            "power_factor_deviation": 0.0
        }),

        ("POWER_SPIKE", {
            "power_ratio": 4.0,
            "voltage_deviation": 0.0,
            "frequency_deviation": 0.0,
            "power_factor_deviation": 0.0
        }),

        ("NIGHT_ANOMALY", {
            "power_ratio": 10.0,
            "voltage_deviation": 0.0,
            "frequency_deviation": 0.0,
            "power_factor_deviation": 0.0
        }),

        ("VOLTAGE_ANOMALY", {
            "power_ratio": 1.0,
            "voltage_deviation": 45.0,
            "frequency_deviation": 0.0,
            "power_factor_deviation": 0.0
        }),

        ("SENSOR_FAULT", {
            "power_ratio": 0.0,
            "voltage_deviation": 0.0,
            "frequency_deviation": 0.0,
            "power_factor_deviation": 0.0
        })
    ]

    for condition, features in examples:

        result = analyze_anomaly(
            condition,
            features
        )

        print(
            "{0:18s} Score: {1:6.1f}  Severity: {2}".format(
                condition,
                result["score"],
                result["severity"]
            )
        )


if __name__ == "__main__":
    main()
