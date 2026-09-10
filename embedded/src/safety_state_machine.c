#include "safety_state_machine.h"

void state_machine_init(SafetyStateMachine *machine)
{
    if (machine == 0)
    {
        return;
    }

    machine->current_state = STATE_NORMAL;
    machine->previous_state = STATE_NORMAL;
}


SafetyState state_machine_update(SafetyStateMachine *machine,
                                 float anomaly_score,
                                 SensorStatus sensor_status)
{
    SafetyState next_state;

    if (machine == 0)
    {
        return STATE_EMERGENCY;
    }

    machine->previous_state = machine->current_state;

    if (sensor_status == SENSOR_INVALID)
    {
        next_state = STATE_EMERGENCY;
    }
    else if (anomaly_score >= 90.0f)
    {
        next_state = STATE_EMERGENCY;
    }
    else if (anomaly_score >= 70.0f)
    {
        next_state = STATE_CRITICAL;
    }
    else if (anomaly_score >= 40.0f)
    {
        next_state = STATE_WARNING;
    }
    else if (machine->current_state != STATE_NORMAL)
    {
        next_state = STATE_RECOVERY;
    }
    else
    {
        next_state = STATE_NORMAL;
    }

    machine->current_state = next_state;

    return next_state;
}


int state_changed(const SafetyStateMachine *machine)
{
    if (machine == 0)
    {
        return 0;
    }

    return machine->current_state != machine->previous_state;
}
