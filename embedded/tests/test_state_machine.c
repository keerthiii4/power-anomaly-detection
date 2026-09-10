#include <stdio.h>
#include "safety_state_machine.h"

static void update_and_print(SafetyStateMachine *machine,
                             float score,
                             SensorStatus sensor)
{
    SafetyState state;

    state = state_machine_update(machine, score, sensor);

    printf("Score: %6.1f | State: %-10s | Changed: %s\n",
           score,
           state_to_string(state),
           state_changed(machine) ? "YES" : "NO");
}

int main(void)
{
    SafetyStateMachine machine;

    state_machine_init(&machine);

    printf("\nPower Safety State Machine Test\n");
    printf("--------------------------------\n");

    update_and_print(&machine, 0.0f, SENSOR_VALID);
    update_and_print(&machine, 50.0f, SENSOR_VALID);
    update_and_print(&machine, 75.0f, SENSOR_VALID);
    update_and_print(&machine, 100.0f, SENSOR_VALID);
    update_and_print(&machine, 0.0f, SENSOR_VALID);
    update_and_print(&machine, 0.0f, SENSOR_VALID);

    printf("\nSensor fault transition:\n");

    update_and_print(&machine, 0.0f, SENSOR_INVALID);

    return 0;
}
