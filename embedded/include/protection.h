#ifndef PROTECTION_H
#define PROTECTION_H

#include "power_safety.h"

ProtectionAction determine_protection_action(
    FaultType fault,
    SafetyState state,
    float anomaly_score
);

const char *protection_message(ProtectionAction action);

#endif
