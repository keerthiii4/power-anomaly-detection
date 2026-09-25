#include <stdio.h>
#include "power_safety.h"

static void run_test(const char *name,
                     PowerReading reading,
                     float score)
{
    SafetyResult result;

    result = process_power_reading(reading, score);

    printf("\n[%s]\n", name);
    printf("Voltage       : %.2f V\n", reading.voltage);
    printf("Current       : %.2f A\n", reading.current);
    printf("Power Factor  : %.2f\n", reading.power_factor);
    printf("Frequency     : %.2f Hz\n", reading.frequency);
    printf("Hour          : %d\n", reading.hour);
    printf("Anomaly Score : %.2f\n", result.anomaly_score);
    printf("Sensor        : %s\n",
           result.sensor_status == SENSOR_VALID ? "VALID" : "INVALID");
    printf("Fault         : %s\n", fault_to_string(result.fault));
    printf("State         : %s\n", state_to_string(result.state));
    printf("Action        : %s\n", action_to_string(result.action));
}

int main(void)
{
    PowerReading normal = {
        230.0f, 2.0f, 0.95f, 50.0f, 14
    };

    PowerReading warning = {
        230.0f, 6.0f, 0.95f, 50.0f, 14
    };

    PowerReading critical = {
        230.0f, 7.0f, 0.95f, 50.0f, 14
    };

    PowerReading invalid = {
        500.0f, -5.0f, 1.5f, 70.0f, 14
    };

    printf("========================================\n");
    printf(" Power Safety Test\n");
    printf("========================================\n");

    run_test("NORMAL READING", normal, 0.0f);
    run_test("WARNING READING", warning, 50.0f);
    run_test("HIGH CONSUMPTION", critical, 75.0f);
    run_test("INVALID SENSOR", invalid, 100.0f);

    printf("\n========================================\n");
    printf(" Test completed\n");
    printf("========================================\n");

    return 0;
}
