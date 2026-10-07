"""
Model Training & Comparative Evaluation Script for Phishing Detection.
Trains Logistic Regression, Random Forest, and Gradient Boosting.
Computes Accuracy, Precision, Recall, F1, ROC-AUC, and Confusion Matrix.
Persists best model and metadata to ml/models/ and ml/evaluation/.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
from ml.features.url_features import url_extractor

def train_and_evaluate(dataset_csv: str = "ml/datasets/phishing_dataset.csv", output_dir: str = "ml/models", eval_dir: str = "ml/evaluation"):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)

    df = pd.read_csv(dataset_csv)
    X = df[url_extractor.FEATURE_NAMES].values
    y = df["label"].values

    # Strict train-test split (avoid data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, random_state=42)
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_fitted_model = None

    for name, clf in models.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        roc_auc = float(roc_auc_score(y_test, y_prob))
        cm = confusion_matrix(y_test, y_pred).tolist()

        results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": cm
        }

        # Select model prioritizing high F1 & low false positives
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_fitted_model = clf

    # Persist evaluation metrics
    eval_payload = {
        "evaluation_timestamp": datetime.utcnow().isoformat(),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "selected_model": best_model_name,
        "selection_rationale": "Selected based on highest F1-score and optimal balance between precision (low false alarms) and recall (catching phishing URLs).",
        "models_benchmarked": results
    }

    metrics_file = os.path.join(eval_dir, "model_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(eval_payload, f, indent=2)

    # Persist the selected model with joblib
    model_artifact_path = os.path.join(output_dir, "phishing_rf_model.joblib")
    joblib.dump(best_fitted_model, model_artifact_path)

    # Feature importances if available
    feature_importances = {}
    if hasattr(best_fitted_model, "feature_importances_"):
        for feat, imp in zip(url_extractor.FEATURE_NAMES, best_fitted_model.feature_importances_):
            feature_importances[feat] = round(float(imp), 4)

    meta_payload = {
        "model_name": best_model_name,
        "model_version": "1.0.0",
        "created_at": datetime.utcnow().isoformat(),
        "feature_names": url_extractor.FEATURE_NAMES,
        "feature_importances": feature_importances,
        "metrics": results[best_model_name]
    }
    with open(os.path.join(output_dir, "model_metadata.json"), "w") as f:
        json.dump(meta_payload, f, indent=2)

    print(f"Training completed. Selected Model: {best_model_name} (F1: {best_f1:.4f})")
    print(f"Model saved to {model_artifact_path}")
    print(f"Metrics saved to {metrics_file}")
    return model_artifact_path

if __name__ == "__main__":
    train_and_evaluate()
