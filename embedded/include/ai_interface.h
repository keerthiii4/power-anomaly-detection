#ifndef AI_INTERFACE_H
#define AI_INTERFACE_H

typedef struct
{
    float voltage;
    float current;
    float power_factor;
    float frequency;
    int hour;
    int day_of_week;
    float anomaly_score;
} AIResult;

int read_ai_result(const char *filename,
                   AIResult *result);

#endif
