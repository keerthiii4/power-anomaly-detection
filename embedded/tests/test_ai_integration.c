#include <stdio.h>

#include "ai_interface.h"
#include "safety_state_machine.h"
#include "power_safety.h"

int main(void)
{
    AIResult ai_result;
    PowerReading reading;
    SafetyStateMachine machine;
    SafetyState state;
    SensorStatus sensor_status;

    const char *filename =
        "monitoring/ai_output.csv";

    printf("\nAI + Embedded C Integration Test\n");
    printf("=================================\n");

    if (read_ai_result(filename, &ai_result) != 0)
    {
        printf("ERROR: Could not read AI output\n");
        return 1;
    }

    printf("\nAI Result\n");
    printf("---------\n");
    printf("Voltage      : %.2f V\n", ai_result.voltage);
    printf("Current      : %.2f A\n", ai_result.current);
    printf("Power Factor : %.2f\n", ai_result.power_factor);
    printf("Frequency    : %.2f Hz\n", ai_result.frequency);
    printf("Hour         : %d\n", ai_result.hour);
    printf("Day          : %d\n", ai_result.day_of_week);
    printf("AI Score     : %.2f\n", ai_result.anomaly_score);

    reading.voltage = ai_result.voltage;
    reading.current = ai_result.current;
    reading.power_factor = ai_result.power_factor;
    reading.frequency = ai_result.frequency;
    reading.hour = ai_result.hour;

    sensor_status = validate_sensor_reading(&reading);

    state_machine_init(&machine);

    state = state_machine_update(
        &machine,
        ai_result.anomaly_score,
        sensor_status
    );

    printf("\nEmbedded Safety Decision\n");
    printf("------------------------\n");
    printf("Sensor Status: %s\n",
           sensor_status == SENSOR_VALID ? "VALID" : "INVALID");

    printf("State        : %s\n",
           state_to_string(state));

    return 0;
}
