#include <stdio.h>
#include "ai_interface.h"

int read_ai_result(const char *filename,
                   AIResult *result)
{
    FILE *file;
    char header[512];
    char condition[64];

    if (filename == NULL || result == NULL)
    {
        return -1;
    }

    file = fopen(filename, "r");

    if (file == NULL)
    {
        return -1;
    }

    if (fgets(header, sizeof(header), file) == NULL)
    {
        fclose(file);
        return -1;
    }

    if (fscanf(file,
               "%f,%f,%f,%f,%d,%d,%63[^,],%f",
               &result->voltage,
               &result->current,
               &result->power_factor,
               &result->frequency,
               &result->hour,
               &result->day_of_week,
               condition,
               &result->anomaly_score) != 8)
    {
        fclose(file);
        return -1;
    }

    fclose(file);

    return 0;
}
