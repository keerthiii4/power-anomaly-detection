#include "protection.h"

ProtectionAction determine_protection_action(
    FaultType fault,
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

        return ACTION_PROTECT_SYSTEM;
    }

    if (state == STATE_WARNING)
    {
        return ACTION_WARN_USER;
    }

    return ACTION_MONITOR;
}


const char *protection_message(ProtectionAction action)
{
    switch (action)
    {
        case ACTION_MONITOR:
            return "System operating normally";

        case ACTION_WARN_USER:
            return "Warning: abnormal power consumption detected";

        case ACTION_LIMIT_LOAD:
            return "Limit load to protect the system";

        case ACTION_PROTECT_SYSTEM:
            return "Activate protective measures";

        case ACTION_ISOLATE_LOAD:
            return "Isolate affected load";

        case ACTION_EMERGENCY_SHUTDOWN:
            return "Emergency shutdown required";

        default:
            return "Unknown protection action";
    }
}
