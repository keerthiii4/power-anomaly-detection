#ifndef POWER_SAFETY_H
#define POWER_SAFETY_H

typedef enum
{
    SENSOR_VALID = 0,
    SENSOR_INVALID
} SensorStatus;

typedef enum
{
    FAULT_NONE = 0,
    FAULT_POWER_SPIKE,
    FAULT_HIGH_CONSUMPTION,
    FAULT_LOW_POWER_FACTOR,
    FAULT_NIGHT_ANOMALY,
    FAULT_VOLTAGE_ANOMALY,
    FAULT_SENSOR
} FaultType;

typedef enum
{
    STATE_NORMAL = 0,
    STATE_WARNING,
    STATE_CRITICAL,
    STATE_EMERGENCY,
    STATE_RECOVERY
} SafetyState;

typedef enum
{
    ACTION_MONITOR = 0,
    ACTION_WARN_USER,
    ACTION_LIMIT_LOAD,
    ACTION_PROTECT_SYSTEM,
    ACTION_ISOLATE_LOAD,
    ACTION_EMERGENCY_SHUTDOWN
} ProtectionAction;

typedef struct
{
    float voltage;
    float current;
    float power_factor;
    float frequency;
    int hour;
} PowerReading;

typedef struct
{
    SensorStatus sensor_status;
    FaultType fault;
    float anomaly_score;
    SafetyState state;
    ProtectionAction action;
} SafetyResult;

SensorStatus validate_sensor_reading(PowerReading reading);

FaultType classify_fault_from_reading(PowerReading reading,
                                      float anomaly_score);

SafetyState determine_state(SensorStatus sensor_status,
                            float anomaly_score);

ProtectionAction determine_action(FaultType fault,
                                  SafetyState state,
                                  float anomaly_score);

SafetyResult process_power_reading(PowerReading reading,
                                   float anomaly_score);

const char *fault_to_string(FaultType fault);
const char *state_to_string(SafetyState state);
const char *action_to_string(ProtectionAction action);

#endif
