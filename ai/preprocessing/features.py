#!/usr/bin/env python3

import math


NOMINAL_VOLTAGE = 230.0
NOMINAL_FREQUENCY = 50.0
NORMAL_POWER_FACTOR = 0.95


def calculate_apparent_power(voltage, current):
    """
    Apparent power:

        S = V x I

    Unit: VA
    """

    return voltage * current


def calculate_reactive_power(voltage, current, power_factor):
    """
    Approximate reactive power.

        Q = S x sin(phi)

    where:

        S = apparent power
        cos(phi) = power factor
    """

    apparent_power = calculate_apparent_power(
        voltage,
        current
    )

    pf = abs(power_factor)

    if pf > 1.0:
        pf = 1.0

    angle_component = math.sqrt(
        max(0.0, 1.0 - (pf * pf))
    )

    return apparent_power * angle_component


def calculate_power_change(power, expected_power):
    """
    Difference between actual and expected power.
    """

    return power - expected_power


def calculate_power_ratio(power, expected_power):
    """
    Ratio of actual power to expected power.
    """

    if expected_power <= 0:
        return 0.0

    return power / expected_power


def calculate_voltage_deviation(voltage):
    """
    Absolute deviation from nominal 230 V.
    """

    return abs(voltage - NOMINAL_VOLTAGE)


def calculate_frequency_deviation(frequency):
    """
    Absolute deviation from nominal 50 Hz.
    """

    return abs(frequency - NOMINAL_FREQUENCY)


def calculate_power_factor_deviation(power_factor):
    """
    Deviation from a normal power factor.
    """

    return abs(
        power_factor - NORMAL_POWER_FACTOR
    )


def calculate_night_flag(hour):
    """
    Mark low-activity night hours.

    00:00 - 05:59
    """

    if hour >= 0 and hour < 6:
        return 1

    return 0


def calculate_high_load_flag(power, expected_power):
    """
    Detect unusually high power compared
    with the expected load.
    """

    if expected_power <= 0:
        return 0

    if power > expected_power * 2.0:
        return 1

    return 0


def calculate_features(
        voltage,
        current,
        power,
        power_factor,
        frequency,
        hour,
        day_of_week,
        expected_power):

    apparent_power = calculate_apparent_power(
        voltage,
        current
    )

    reactive_power = calculate_reactive_power(
        voltage,
        current,
        power_factor
    )

    power_change = calculate_power_change(
        power,
        expected_power
    )

    power_ratio = calculate_power_ratio(
        power,
        expected_power
    )

    voltage_deviation = calculate_voltage_deviation(
        voltage
    )

    frequency_deviation = calculate_frequency_deviation(
        frequency
    )

    power_factor_deviation = (
        calculate_power_factor_deviation(
            power_factor
        )
    )

    night_flag = calculate_night_flag(hour)

    high_load_flag = calculate_high_load_flag(
        power,
        expected_power
    )

    return {
        "voltage": round(voltage, 3),
        "current": round(current, 3),
        "power": round(power, 3),
        "power_factor": round(power_factor, 3),
        "frequency": round(frequency, 3),
        "hour": int(hour),
        "day_of_week": int(day_of_week),
        "apparent_power": round(
            apparent_power,
            3
        ),
        "reactive_power_estimate": round(
            reactive_power,
            3
        ),
        "power_change": round(
            power_change,
            3
        ),
        "power_ratio": round(
            power_ratio,
            3
        ),
        "voltage_deviation": round(
            voltage_deviation,
            3
        ),
        "frequency_deviation": round(
            frequency_deviation,
            3
        ),
        "power_factor_deviation": round(
            power_factor_deviation,
            3
        ),
        "night_flag": night_flag,
        "high_load_flag": high_load_flag
    }


def get_feature_names():
    """
    Return the ordered feature list.
    """

    return [
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


if __name__ == "__main__":

    sample = calculate_features(
        voltage=230.0,
        current=2.0,
        power=437.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2,
        expected_power=450.0
    )

    print("FEATURE ENGINEERING TEST")
    print("=" * 50)

    for name in get_feature_names():
        print(
            "{0}: {1}".format(
                name,
                sample[name]
            )
        )
