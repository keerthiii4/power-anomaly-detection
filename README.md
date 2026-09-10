# AI-Based Power Consumption Anomaly Detection System

## 1. Project Overview

The AI-Based Power Consumption Anomaly Detection System is an embedded-AI and machine-learning based system designed to monitor electrical power consumption and identify abnormal operating conditions.

The system combines:

- Power consumption simulation
- Sensor-data validation
- Feature engineering
- Machine learning based anomaly detection
- Anomaly scoring
- Fault classification
- Safety state-machine logic
- Protection and load-control decisions
- Telemetry logging
- Embedded C implementation
- Console-based monitoring

The project follows an important engineering principle:

> AI detects and predicts abnormal behavior, while deterministic safety logic makes the final protection decision.

---

## 2. Objectives

The main objectives are:

1. Monitor electrical power parameters.
2. Detect abnormal consumption patterns.
3. Identify different types of power anomalies.
4. Validate sensor measurements before AI processing.
5. Generate an anomaly score.
6. Classify the detected fault.
7. Determine the appropriate system safety state.
8. Select an appropriate protection action.
9. Store system telemetry for analysis.
10. Demonstrate integration between AI software and embedded C safety logic.

---

## 3. System Architecture

```text
                +-----------------------+
                |   Power Data Source   |
                |    / Simulation       |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Sensor Validation     |
                +-----------+-----------+
                            |
                     Valid Reading?
                       /         \
                     NO           YES
                     |             |
                     v             v
              SENSOR FAULT     Feature Engineering
                     |             |
                     |             v
                     |       AI Anomaly Detection
                     |             |
                     |             v
                     |       Anomaly Score
                     |             |
                     |             v
                     |       Fault Manager
                     |             |
                     |             v
                     |       Safety State Machine
                     |             |
                     |             v
                     |       Protection Logic
                     |             |
                     +------+------+
                            |
                            v
                +-----------------------+
                |   System Action       |
                | Monitor / Warn /      |
                | Limit / Protect /      |
                | Isolate / Shutdown    |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Telemetry & Dashboard |
                +-----------------------+
