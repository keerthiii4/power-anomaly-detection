#!/usr/bin/env python3

import csv
import os
import pickle

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


DATASET_FILE = (
    "ai/dataset/processed/"
    "power_consumption_features.csv"
)

MODEL_DIRECTORY = "ai/models"

MODEL_FILE = (
    "ai/models/"
    "power_anomaly_model.pkl"
)


FEATURE_NAMES = [
    "voltage",
    "current",
    "power",
    "power_factor",
    "frequency",
    "hour",
    "day_of_week",
    "apparent_power",
    "reactive_power_estimate",
    "power_change",
    "power_ratio",
    "voltage_deviation",
    "frequency_deviation",
    "power_factor_deviation",
    "night_flag",
    "high_load_flag"
]


def load_dataset():

    X = []
    y = []

    with open(DATASET_FILE, "r") as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            features = []

            for feature in FEATURE_NAMES:
                features.append(
                    float(row[feature])
                )

            X.append(features)
            y.append(
                int(row["label"])
            )

    return X, y


def build_models():

    models = {}

    models["Logistic Regression"] = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=500
            )
        )
    ])

    models["Decision Tree"] = (
        DecisionTreeClassifier(
            random_state=42
        )
    )

    models["Random Forest"] = (
        RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
    )

    return models


def evaluate_model(
        name,
        model,
        X_train,
        X_test,
        y_train,
        y_test):

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted"
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted"
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted"
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print(
        "Accuracy  : {:.4f}".format(
            accuracy
        )
    )

    print(
        "Precision : {:.4f}".format(
            precision
        )
    )

    print(
        "Recall    : {:.4f}".format(
            recall
        )
    )

    print(
        "F1 Score  : {:.4f}".format(
            f1
        )
    )

    print("\nConfusion Matrix:")

    for row in matrix:
        print(row)

    return {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def train():

    if not os.path.exists(DATASET_FILE):

        print(
            "ERROR: Processed dataset not found:"
        )

        print(DATASET_FILE)

        return

    if not os.path.exists(MODEL_DIRECTORY):
        os.makedirs(MODEL_DIRECTORY)

    X, y = load_dataset()

    print("\nPOWER ANOMALY AI TRAINING")
    print("=" * 60)

    print(
        "Total samples :",
        len(X)
    )

    print(
        "Features      :",
        len(FEATURE_NAMES)
    )

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )

    print(
        "Training samples:",
        len(X_train)
    )

    print(
        "Testing samples :",
        len(X_test)
    )

    models = build_models()

    results = []

    for name in models:

        result = evaluate_model(
            name,
            models[name],
            X_train,
            X_test,
            y_train,
            y_test
        )

        results.append(result)

    best_result = max(
        results,
        key=lambda item: item["f1"]
    )

    best_model = best_result["model"]

    package = {
        "model": best_model,
        "feature_names": FEATURE_NAMES,
        "model_name": "best_model_by_f1"
    }

    with open(
        MODEL_FILE,
        "wb"
    ) as model_file:

        pickle.dump(
            package,
            model_file,
            protocol=2
        )

    print("\n" + "=" * 60)
    print("BEST MODEL")
    print("=" * 60)

    print(
        "Selected by weighted F1 score"
    )

    print(
        "F1 Score: {:.4f}".format(
            best_result["f1"]
        )
    )

    print("\nModel saved to:")
    print(MODEL_FILE)


if __name__ == "__main__":
    train()
