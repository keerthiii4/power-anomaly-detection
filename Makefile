.RECIPEPREFIX := >

CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -Iembedded/include

TARGETS = test_power_safety \
          test_state_machine \
          test_protection \
          test_ai_integration

all: build

build: $(TARGETS)

test: build
> @echo "========================================"
> @echo " Running Embedded C Test Suite"
> @echo "========================================"
> @echo ""
> @echo "[1/4] Power safety tests"
> @./test_power_safety
> @echo ""
> @echo "[2/4] State machine tests"
> @./test_state_machine
> @echo ""
> @echo "[3/4] Protection tests"
> @./test_protection
> @echo ""
> @echo "[4/4] AI integration test"
> @./test_ai_integration
> @echo ""
> @echo "========================================"
> @echo " All Embedded C tests completed"
> @echo "========================================"

test_power_safety: embedded/src/power_safety.c embedded/tests/test_power_safety.c
> $(CC) $(CFLAGS) embedded/src/power_safety.c embedded/tests/test_power_safety.c -o test_power_safety

test_state_machine: embedded/src/power_safety.c embedded/src/safety_state_machine.c embedded/tests/test_state_machine.c
> $(CC) $(CFLAGS) embedded/src/power_safety.c embedded/src/safety_state_machine.c embedded/tests/test_state_machine.c -o test_state_machine

test_protection: embedded/src/power_safety.c embedded/src/protection.c embedded/tests/test_protection.c
> $(CC) $(CFLAGS) embedded/src/power_safety.c embedded/src/protection.c embedded/tests/test_protection.c -o test_protection

test_ai_integration: embedded/src/power_safety.c embedded/src/safety_state_machine.c embedded/src/ai_interface.c embedded/tests/test_ai_integration.c
> $(CC) $(CFLAGS) embedded/src/power_safety.c embedded/src/safety_state_machine.c embedded/src/ai_interface.c embedded/tests/test_ai_integration.c -o test_ai_integration

clean:
> rm -f test_power_safety
> rm -f test_state_machine
> rm -f test_protection
> rm -f test_ai_integration
