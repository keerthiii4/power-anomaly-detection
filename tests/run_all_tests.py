import subprocess
import sys


def run_command(title, command):
    print("")
    print("=" * 60)
    print(title)
    print("=" * 60)

    result = subprocess.call(command)

    if result != 0:
        print("")
        print("FAILED: " + title)
        return False

    print("")
    print("PASSED: " + title)
    return True


def main():
    tests = [
        (
            "Dataset analysis",
            ["python3", "ai/preprocessing/analyze_dataset.py"]
        ),
        (
            "Feature engineering test",
            ["python3", "ai/preprocessing/features.py"]
        ),
        (
            "Power monitoring system test",
            ["python3", "tests/test_power_system.py"]
        ),
        (
            "Fault injection test",
            ["python3", "tests/test_fault_injection.py"]
        ),
        (
            "End-to-end system test",
            ["python3", "tests/test_end_to_end.py"]
        ),
        (
            "AI output generation",
            ["python3", "monitoring/ai_output.py"]
        ),
        (
            "Embedded C test suite",
            ["make", "test"]
        ),
        (
            "Dashboard test",
            ["python3", "dashboard/dashboard.py"]
        )
    ]

    passed = 0
    failed = 0

    print("")
    print("=" * 60)
    print(" POWER ANOMALY DETECTION")
    print(" PROJECT-LEVEL TEST RUNNER")
    print("=" * 60)

    for title, command in tests:
        success = run_command(title, command)

        if success:
            passed += 1
        else:
            failed += 1
            print("")
            print("Stopping test runner because a test failed.")
            break

    print("")
    print("=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)
    print("Passed : " + str(passed))
    print("Failed : " + str(failed))
    print("=" * 60)

    if failed == 0:
        print("")
        print("ALL PROJECT TESTS PASSED")
        print("")
        return 0

    print("")
    print("PROJECT TEST SUITE FAILED")
    print("")
    return 1


if __name__ == "__main__":
    sys.exit(main())
