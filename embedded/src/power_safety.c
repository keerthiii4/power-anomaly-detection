#include "power_safety.h"

#define MIN_VOLTAGE 180.0f
#define MAX_VOLTAGE 260.0f

#define MIN_CURRENT 0.0f
#define MAX_CURRENT 50.0f

#define MIN_POWER_FACTOR 0.0f
#define MAX_POWER_FACTOR 1.0f

#define MIN_FREQUENCY 45.0f
#define MAX_FREQUENCY 55.0f

#define VOLTAGE_LOW_THRESHOLD 210.0f
#define VOLTAGE_HIGH_THRESHOLD 250.0f

#define LOW_POWER_FACTOR_THRESHOLD 0.80f

#define NIGHT_START_HOUR 0
#define NIGHT_END_HOUR 5

#define NIGHT_POWER_THRESHOLD 1000.0f
#define HIGH_CONSUMPTION_THRESHOLD 1000.0f
#define POWER_SPIKE_THRESHOLD 1800.0f


SensorStatus validate_sensor_reading(PowerReading reading)
{
    if (reading.voltage < MIN_VOLTAGE ||
        reading.voltage > MAX_VOLTAGE)
    {
        return SENSOR_INVALID;
    }

    if (reading.current < MIN_CURRENT ||
        reading.current > MAX_CURRENT)
    {
        return SENSOR_INVALID;
    }

    if (reading.power_factor < MIN_POWER_FACTOR ||
        reading.power_factor > MAX_POWER_FACTOR)
    {
        return SENSOR_INVALID;
    }

    if (reading.frequency < MIN_FREQUENCY ||
        reading.frequency > MAX_FREQUENCY)
    {
        return SENSOR_INVALID;
    }

    if (reading.hour < 0 || reading.hour > 23)
    {
        return SENSOR_INVALID;
    }

    return SENSOR_VALID;
}


/*
 * Fault classification uses the actual electrical reading,
 * not anomaly score alone.
 *
 * Priority:
 * 1. Sensor validity
 * 2. Voltage anomaly
 * 3. Low power factor
 * 4. Night anomaly
 * 5. Power spike
 * 6. High consumption
 * 7. Normal
 */
FaultType classify_fault_from_reading(PowerReading reading,
                                      float anomaly_score)
{
    float active_power;

    (void)anomaly_score;

    if (validate_sensor_reading(reading) == SENSOR_INVALID)
    {
        return FAULT_SENSOR;
    }

    if (reading.voltage < VOLTAGE_LOW_THRESHOLD ||
        reading.voltage > VOLTAGE_HIGH_THRESHOLD)
    {
        return FAULT_VOLTAGE_ANOMALY;
    }

    if (reading.power_factor < LOW_POWER_FACTOR_THRESHOLD)
    {
        return FAULT_LOW_POWER_FACTOR;
    }

    active_power = reading.voltage *
                   reading.current *
                   reading.power_factor;

    if (reading.hour >= NIGHT_START_HOUR &&
        reading.hour <= NIGHT_END_HOUR &&
        active_power > NIGHT_POWER_THRESHOLD)
    {
        return FAULT_NIGHT_ANOMALY;
    }

    if (active_power > POWER_SPIKE_THRESHOLD)
    {
        return FAULT_POWER_SPIKE;
    }

    if (active_power > HIGH_CONSUMPTION_THRESHOLD)
    {
        return FAULT_HIGH_CONSUMPTION;
    }

    return FAULT_NONE;
}


SafetyState determine_state(SensorStatus sensor_status,
                            float anomaly_score)
{
    if (sensor_status == SENSOR_INVALID)
    {
        return STATE_EMERGENCY;
    }

    if (anomaly_score >= 90.0f)
    {
        return STATE_EMERGENCY;
    }

    if (anomaly_score >= 70.0f)
    {
        return STATE_CRITICAL;
    }

    if (anomaly_score >= 40.0f)
    {
        return STATE_WARNING;
    }

    return STATE_NORMAL;
}


ProtectionAction determine_action(FaultType fault,
                                  SafetyState state,
                                  float anomaly_score)
{
    (void)anomaly_score;

    if (fault == FAULT_SENSOR)
    {
        return ACTION_ISOLATE_LOAD;
    }

    if (state == STATE_EMERGENCY)
    {
        return ACTION_EMERGENCY_SHUTDOWN;
    }

    if (state == STATE_WARNING)
    {
        return ACTION_WARN_USER;
    }

    if (state == STATE_CRITICAL)
    {
        if (fault == FAULT_HIGH_CONSUMPTION)
        {
            return ACTION_LIMIT_LOAD;
        }

        if (fault == FAULT_POWER_SPIKE)
        {
            return ACTION_PROTECT_SYSTEM;
        }

        if (fault == FAULT_VOLTAGE_ANOMALY)
        {
            return ACTION_ISOLATE_LOAD;
        }

        if (fault == FAULT_LOW_POWER_FACTOR)
        {
            return ACTION_WARN_USER;
        }

        if (fault == FAULT_NIGHT_ANOMALY)
        {
            return ACTION_LIMIT_LOAD;
        }

        return ACTION_PROTECT_SYSTEM;
    }

    if (state == STATE_RECOVERY)
    {
        return ACTION_MONITOR;
    }

    return ACTION_MONITOR;
}


SafetyResult process_power_reading(PowerReading reading,
                                   float anomaly_score)
{
    SafetyResult result;

    result.sensor_status = validate_sensor_reading(reading);

    result.fault = classify_fault_from_reading(reading,
                                               anomaly_score);

    result.state = determine_state(result.sensor_status,
                                   anomaly_score);

    result.action = determine_action(result.fault,
                                     result.state,
                                     anomaly_score);

    result.anomaly_score = anomaly_score;

    return result;
}


const char *fault_to_string(FaultType fault)
{
    switch (fault)
    {
        case FAULT_NONE:
            return "NONE";

        case FAULT_POWER_SPIKE:
            return "POWER_SPIKE";

        case FAULT_HIGH_CONSUMPTION:
            return "HIGH_CONSUMPTION";

        case FAULT_LOW_POWER_FACTOR:
            return "LOW_POWER_FACTOR";

        case FAULT_NIGHT_ANOMALY:
            return "NIGHT_ANOMALY";

        case FAULT_VOLTAGE_ANOMALY:
            return "VOLTAGE_ANOMALY";

        case FAULT_SENSOR:
            return "SENSOR_FAULT";

        default:
            return "UNKNOWN";
    }
}


const char *state_to_string(SafetyState state)
{
    switch (state)
    {
        case STATE_NORMAL:
            return "NORMAL";

        case STATE_WARNING:
            return "WARNING";

        case STATE_CRITICAL:
            return "CRITICAL";

        case STATE_EMERGENCY:
            return "EMERGENCY";

        case STATE_RECOVERY:
            return "RECOVERY";

        default:
            return "UNKNOWN";
    }
}


const char *action_to_string(ProtectionAction action)
{
    switch (action)
    {
        case ACTION_MONITOR:
            return "MONITOR";

        case ACTION_WARN_USER:
            return "WARN_USER";

        case ACTION_LIMIT_LOAD:
            return "LIMIT_LOAD";

        case ACTION_PROTECT_SYSTEM:
            return "PROTECT_SYSTEM";

        case ACTION_ISOLATE_LOAD:
            return "ISOLATE_LOAD";

        case ACTION_EMERGENCY_SHUTDOWN:
            return "EMERGENCY_SHUTDOWN";

        default:
            return "UNKNOWN";
    }
}
