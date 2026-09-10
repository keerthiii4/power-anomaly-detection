from __future__ import print_function


# Engineering limits for the simulated monitoring system
MIN_VOLTAGE = 180.0
MAX_VOLTAGE = 260.0

MIN_CURRENT = 0.0
MAX_CURRENT = 50.0

MIN_POWER_FACTOR = 0.0
MAX_POWER_FACTOR = 1.0

MIN_FREQUENCY = 45.0
MAX_FREQUENCY = 55.0

MIN_HOUR = 0
MAX_HOUR = 23

MIN_DAY = 0
MAX_DAY = 6


def validate_voltage(voltage):
    return MIN_VOLTAGE <= voltage <= MAX_VOLTAGE


def validate_current(current):
    return MIN_CURRENT <= current <= MAX_CURRENT


def validate_power_factor(power_factor):
    return MIN_POWER_FACTOR <= power_factor <= MAX_POWER_FACTOR


def validate_frequency(frequency):
    return MIN_FREQUENCY <= frequency <= MAX_FREQUENCY


def validate_time(hour, day_of_week):
    return (
        MIN_HOUR <= hour <= MAX_HOUR
        and
        MIN_DAY <= day_of_week <= MAX_DAY
    )


def validate_sensor_reading(voltage, current, power_factor,
                            frequency, hour, day_of_week):

    errors = []

    if not validate_voltage(voltage):
        errors.append("INVALID_VOLTAGE")

    if not validate_current(current):
        errors.append("INVALID_CURRENT")

    if not validate_power_factor(power_factor):
        errors.append("INVALID_POWER_FACTOR")

    if not validate_frequency(frequency):
        errors.append("INVALID_FREQUENCY")

    if not validate_time(hour, day_of_week):
        errors.append("INVALID_TIME")

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors
    }


def main():

    print("")
    print("SENSOR VALIDATION")
    print("==================")

    # Valid sensor reading
    result = validate_sensor_reading(
        voltage=230.0,
        current=2.0,
        power_factor=0.95,
        frequency=50.0,
        hour=14,
        day_of_week=2
    )

    print("Valid reading:")
    print("  Valid  : {0}".format(result["valid"]))
    print("  Errors : {0}".format(result["errors"]))

    # Invalid sensor reading
    result = validate_sensor_reading(
        voltage=500.0,
        current=-5.0,
        power_factor=1.5,
        frequency=70.0,
        hour=30,
        day_of_week=8
    )

    print("")
    print("Invalid reading:")
    print("  Valid  : {0}".format(result["valid"]))
    print("  Errors : {0}".format(result["errors"]))


if __name__ == "__main__":
    main()
