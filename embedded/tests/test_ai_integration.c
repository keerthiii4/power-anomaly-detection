#include <stdio.h>

#include "power_safety.h"
#include "safety_state_machine.h"
#include "ai_interface.h"

int main(void)
{
    AIResult ai_result;
    PowerReading reading;
    SensorStatus sensor_status;
    SafetyStateMachine state_machine;
    SafetyState safety_state;

    printf("========================================\n");
    printf(" AI Integration Test\n");
    printf("========================================\n");

    /*
     * read_ai_result() follows the standard C convention:
     *   0  = success
     *  -1  = failure
     */
    if (read_ai_result("monitoring/ai_output.csv", &ai_result) != 0)
    {
        printf("ERROR: Failed to read AI output\n");
        return 1;
    }

    printf("Voltage       : %.2f V\n", ai_result.voltage);
    printf("Current       : %.2f A\n", ai_result.current);
    printf("Power Factor  : %.2f\n", ai_result.power_factor);
    printf("Frequency     : %.2f Hz\n", ai_result.frequency);
    printf("Hour          : %d\n", ai_result.hour);
    printf("Day           : %d\n", ai_result.day_of_week);
    printf("AI Score      : %.2f\n", ai_result.anomaly_score);

    reading.voltage = ai_result.voltage;
    reading.current = ai_result.current;
    reading.power_factor = ai_result.power_factor;
    reading.frequency = ai_result.frequency;
    reading.hour = ai_result.hour;

    sensor_status = validate_sensor_reading(reading);

    printf("Sensor Status : %s\n",
           sensor_status == SENSOR_VALID ? "VALID" : "INVALID");

    state_machine_init(&state_machine);

    safety_state = state_machine_update(&state_machine,
                                        ai_result.anomaly_score,
                                        sensor_status);

    printf("Safety State  : %s\n",
           state_to_string(safety_state));

    printf("========================================\n");
    printf(" AI integration test completed\n");
    printf("========================================\n");

    /*
     * Expected result for the generated normal AI output:
     *
     * AI Score      : 0.00
     * Sensor Status : VALID
     * Safety State  : NORMAL
     */
    if (sensor_status != SENSOR_VALID)
    {
        printf("TEST RESULT: FAIL - Sensor should be valid\n");
        return 1;
    }

    if (ai_result.anomaly_score != 0.0f)
    {
        printf("TEST RESULT: FAIL - Expected AI score 0.00\n");
        return 1;
    }

    if (safety_state != STATE_NORMAL)
    {
        printf("TEST RESULT: FAIL - Expected NORMAL safety state\n");
        return 1;
    }

    printf("TEST RESULT: PASS\n");

    return 0;
}
