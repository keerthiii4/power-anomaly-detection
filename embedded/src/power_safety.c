#include <stdio.h>
#include "power_safety.h"

#define MIN_VOLTAGE       180.0f
#define MAX_VOLTAGE       260.0f

#define MIN_CURRENT       0.0f
#define MAX_CURRENT       50.0f

#define MIN_POWER_FACTOR  0.0f
#define MAX_POWER_FACTOR  1.0f

#define MIN_FREQUENCY     45.0f
#define MAX_FREQUENCY     55.0f

#define MIN_HOUR          0
#define MAX_HOUR          23


SensorStatus validate_sensor_reading(const PowerReading *reading)
{
    if (reading == NULL)
    {
        return SENSOR_INVALID;
    }

    if (reading->voltage < MIN_VOLTAGE ||
        reading->voltage > MAX_VOLTAGE)
    {
        return SENSOR_INVALID;
    }

    if (reading->current < MIN_CURRENT ||
        reading->current > MAX_CURRENT)
    {
        return SENSOR_INVALID;
    }

    if (reading->power_factor < MIN_POWER_FACTOR ||
        reading->power_factor > MAX_POWER_FACTOR)
    {
        return SENSOR_INVALID;
    }

    if (reading->frequency < MIN_FREQUENCY ||
        reading->frequency > MAX_FREQUENCY)
    {
        return SENSOR_INVALID;
    }

    if (reading->hour < MIN_HOUR ||
        reading->hour > MAX_HOUR)
    {
        return SENSOR_INVALID;
    }

    return SENSOR_VALID;
}


FaultType classify_fault(float anomaly_score)
{
    if (anomaly_score >= 90.0f)
    {
        return FAULT_SENSOR;
    }

    if (anomaly_score >= 70.0f)
    {
        return FAULT_VOLTAGE_ANOMALY;
    }

    if (anomaly_score >= 60.0f)
    {
        return FAULT_POWER_SPIKE;
    }

    if (anomaly_score >= 40.0f)
    {
        return FAULT_HIGH_CONSUMPTION;
    }

    return FAULT_NONE;
}


SafetyState determine_state(float anomaly_score,
                            SensorStatus sensor_status)
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
                                  SafetyState state)
{
    if (fault == FAULT_SENSOR)
    {
        return ACTION_ISOLATE_LOAD;
    }

    switch (state)
    {
        case STATE_NORMAL:
            return ACTION_MONITOR;

        case STATE_WARNING:
            return ACTION_WARN_USER;

        case STATE_CRITICAL:
            if (fault == FAULT_HIGH_CONSUMPTION)
            {
                return ACTION_LIMIT_LOAD;
            }

            if (fault == FAULT_POWER_SPIKE)
            {
                return ACTION_PROTECT_SYSTEM;
            }

            return ACTION_PROTECT_SYSTEM;

        case STATE_EMERGENCY:
            return ACTION_EMERGENCY_SHUTDOWN;

        case STATE_RECOVERY:
            return ACTION_MONITOR;

        default:
            return ACTION_EMERGENCY_SHUTDOWN;
    }
}


SafetyResult process_power_reading(const PowerReading *reading,
                                   float anomaly_score)
{
    SafetyResult result;

    result.sensor_status = validate_sensor_reading(reading);

    if (result.sensor_status == SENSOR_INVALID)
    {
        result.fault = FAULT_SENSOR;
        result.anomaly_score = 100.0f;
        result.state = STATE_EMERGENCY;
        result.action = ACTION_ISOLATE_LOAD;

        return result;
    }

    result.anomaly_score = anomaly_score;
    result.fault = classify_fault(anomaly_score);
    result.state = determine_state(anomaly_score,
                                   result.sensor_status);
    result.action = determine_action(result.fault,
                                     result.state);

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
