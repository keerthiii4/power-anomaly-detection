#ifndef SAFETY_STATE_MACHINE_H
#define SAFETY_STATE_MACHINE_H

#include "power_safety.h"

typedef struct
{
    SafetyState current_state;
    SafetyState previous_state;
} SafetyStateMachine;

void state_machine_init(SafetyStateMachine *machine);

SafetyState state_machine_update(SafetyStateMachine *machine,
                                 float anomaly_score,
                                 SensorStatus sensor_status);

int state_changed(const SafetyStateMachine *machine);

const char *state_to_string(SafetyState state);

#endif
