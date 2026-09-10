#!/usr/bin/env python3

import random
from datetime import datetime, timedelta


NORMAL = "NORMAL"
POWER_SPIKE = "POWER_SPIKE"
HIGH_CONSUMPTION = "HIGH_CONSUMPTION"
LOW_POWER_FACTOR = "LOW_POWER_FACTOR"
NIGHT_ANOMALY = "NIGHT_ANOMALY"
VOLTAGE_ANOMALY = "VOLTAGE_ANOMALY"
SENSOR_FAULT = "SENSOR_FAULT"


ANOMALY_TYPES = [
    NORMAL,
    POWER_SPIKE,
    HIGH_CONSUMPTION,
    LOW_POWER_FACTOR,
    NIGHT_ANOMALY,
    VOLTAGE_ANOMALY,
    SENSOR_FAULT
]


def get_expected_power(hour):
    """
    Return approximate expected power consumption based on time.
    """

    if 0 <= hour < 6:
        return random.uniform(80.0, 180.0)

    if 6 <= hour < 9:
        return random.uniform(300.0, 700.0)

    if 9 <= hour < 17:
        return random.uniform(250.0, 600.0)

    if 17 <= hour < 22:
        return random.uniform(500.0, 1000.0)

    return random.uniform(200.0, 500.0)


def calculate_power(voltage, current, power_factor):
    """
    Calculate active power.

    Single-phase approximation:
        P = V x I x PF
    """

    return voltage * current * power_factor


def generate_normal_reading(timestamp):
    """
    Generate a normal electrical reading.
    """

    hour = timestamp.hour

    voltage = random.gauss(230.0, 2.0)
    power_factor = random.uniform(0.90, 0.99)

    expected_power = get_expected_power(hour)

    current = expected_power / (voltage * power_factor)

    current += random.gauss(0.0, 0.05)

    if current < 0:
        current = 0.0

    power = calculate_power(
        voltage,
        current,
        power_factor
    )

    frequency = random.gauss(50.0, 0.05)

    return {
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "voltage": round(voltage, 2),
        "current": round(current, 3),
        "power": round(power, 2),
        "power_factor": round(power_factor, 3),
        "frequency": round(frequency, 3),
        "condition": NORMAL
    }


def generate_power_spike(timestamp):
    """
    Generate a short-duration power spike.
    """

    reading = generate_normal_reading(timestamp)

    spike_multiplier = random.uniform(3.0, 6.0)

    reading["power"] = round(
        reading["power"] * spike_multiplier,
        2
    )

    reading["current"] = round(
        reading["power"] /
        (reading["voltage"] * reading["power_factor"]),
        3
    )

    reading["condition"] = POWER_SPIKE

    return reading


def generate_high_consumption(timestamp):
    """
    Generate sustained high power consumption.
    """

    reading = generate_normal_reading(timestamp)

    multiplier = random.uniform(2.0, 3.5)

    reading["power"] = round(
        reading["power"] * multiplier,
        2
    )

    reading["current"] = round(
        reading["power"] /
        (reading["voltage"] * reading["power_factor"]),
        3
    )

    reading["condition"] = HIGH_CONSUMPTION

    return reading


def generate_low_power_factor(timestamp):
    """
    Generate an inefficient electrical load.
    """

    reading = generate_normal_reading(timestamp)

    reading["power_factor"] = round(
        random.uniform(0.45, 0.70),
        3
    )

    reading["current"] = round(
        reading["power"] /
        (reading["voltage"] * reading["power_factor"]),
        3
    )

    reading["condition"] = LOW_POWER_FACTOR

    return reading


def generate_night_anomaly(timestamp):
    """
    Generate unusually high consumption during night hours.
    """

    reading = generate_normal_reading(timestamp)

    reading["power"] = round(
        random.uniform(1200.0, 2500.0),
        2
    )

    reading["current"] = round(
        reading["power"] /
        (reading["voltage"] * reading["power_factor"]),
        3
    )

    reading["condition"] = NIGHT_ANOMALY

    return reading


def generate_voltage_anomaly(timestamp):
    """
    Generate abnormal supply voltage.
    """

    reading = generate_normal_reading(timestamp)

    if random.choice([True, False]):
        reading["voltage"] = round(
            random.uniform(170.0, 195.0),
            2
        )
    else:
        reading["voltage"] = round(
            random.uniform(255.0, 280.0),
            2
        )

    reading["current"] = round(
        reading["power"] /
        (
            reading["voltage"] *
            reading["power_factor"]
        ),
        3
    )

    reading["condition"] = VOLTAGE_ANOMALY

    return reading


def generate_sensor_fault(timestamp):
    """
    Generate physically invalid sensor data.
    """

    fault_type = random.choice([
        "voltage",
        "current",
        "power_factor",
        "frequency"
    ])

    reading = generate_normal_reading(timestamp)

    if fault_type == "voltage":
        reading["voltage"] = random.choice([
            -10.0,
            0.0,
            500.0
        ])

    elif fault_type == "current":
        reading["current"] = random.choice([
            -5.0,
            500.0
        ])

    elif fault_type == "power_factor":
        reading["power_factor"] = random.choice([
            -1.0,
            1.5,
            2.0
        ])

    elif fault_type == "frequency":
        reading["frequency"] = random.choice([
            -10.0,
            100.0
        ])

    reading["condition"] = SENSOR_FAULT

    return reading


def generate_reading(condition, timestamp=None):
    """
    Generate a reading for the requested condition.
    """

    if timestamp is None:
        timestamp = datetime.now()

    if condition == NORMAL:
        return generate_normal_reading(timestamp)

    if condition == POWER_SPIKE:
        return generate_power_spike(timestamp)

    if condition == HIGH_CONSUMPTION:
        return generate_high_consumption(timestamp)

    if condition == LOW_POWER_FACTOR:
        return generate_low_power_factor(timestamp)

    if condition == NIGHT_ANOMALY:
        return generate_night_anomaly(timestamp)

    if condition == VOLTAGE_ANOMALY:
        return generate_voltage_anomaly(timestamp)

    if condition == SENSOR_FAULT:
        return generate_sensor_fault(timestamp)

    raise ValueError(
        "Unknown condition: " + str(condition)
    )


def print_reading(reading):
    """
    Display one simulated reading.
    """

    print("Timestamp     :", reading["timestamp"])
    print("Voltage       :", reading["voltage"], "V")
    print("Current       :", reading["current"], "A")
    print("Power         :", reading["power"], "W")
    print("Power Factor  :", reading["power_factor"])
    print("Frequency     :", reading["frequency"], "Hz")
    print("Condition     :", reading["condition"])
    print("-" * 50)


def main():
    """
    Generate one sample of every condition.
    """

    base_time = datetime.now().replace(
        minute=0,
        second=0,
        microsecond=0
    )

    print("\nPOWER CONSUMPTION SENSOR SIMULATOR")
    print("=" * 50)

    for index, condition in enumerate(ANOMALY_TYPES):

        timestamp = base_time + timedelta(
            hours=index
        )

        reading = generate_reading(
            condition,
            timestamp
        )

        print_reading(reading)


if __name__ == "__main__":
    main()
