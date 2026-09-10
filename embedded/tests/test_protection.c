#include <stdio.h>

#include "power_safety.h"
#include "protection.h"

static void test_case(const char *name,
                      FaultType fault,
                      SafetyState state,
                      float score)
{
    ProtectionAction action;

    action = determine_protection_action(
        fault,
        state,
        score
    );

    printf("\n%s\n", name);
    printf("Fault   : %s\n", fault_to_string(fault));
    printf("State   : %s\n", state_to_string(state));
    printf("Score   : %.2f\n", score);
    printf("Action  : %s\n", action_to_string(action));
    printf("Message : %s\n", protection_message(action));
}


int main(void)
{
    printf("\nEmbedded C Protection Logic Test\n");
    printf("================================\n");

    test_case(
        "NORMAL",
        FAULT_NONE,
        STATE_NORMAL,
        0.0f
    );

    test_case(
        "POWER SPIKE",
        FAULT_POWER_SPIKE,
        STATE_WARNING,
        61.0f
    );

    test_case(
        "HIGH CONSUMPTION",
        FAULT_HIGH_CONSUMPTION,
        STATE_CRITICAL,
        75.0f
    );

    test_case(
        "VOLTAGE ANOMALY",
        FAULT_VOLTAGE_ANOMALY,
        STATE_CRITICAL,
        80.0f
    );

    test_case(
        "SENSOR FAULT",
        FAULT_SENSOR,
        STATE_EMERGENCY,
        100.0f
    );

    return 0;
}
