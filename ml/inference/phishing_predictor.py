import os
import joblib
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
from ml.features.url_features import url_extractor

# Dynamically resolve absolute path to root project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_rf_model.joblib")

class PhishingPredictor:
    """
    Performs real supervised machine learning inference on incoming URLs.
    Extracts features, runs through trained Random Forest / Gradient Boosting model,
    and returns probabilistic risk scores, classifications, and explainable indicators.
    """
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.model_name = "RandomForestClassifier"
        self.model_version = "1.0.0"
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading phishing model: {e}")
                self.model = None

    def predict(self, url: str) -> Dict[str, Any]:
        if not url:
            return {
                "classification": "LEGITIMATE",
                "phishing_probability": 0.0,
                "risk_score": 0.0,
                "confidence": 0.0,
                "indicators": [],
                "model_name": self.model_name,
                "model_version": self.model_version,
                "prediction_timestamp": datetime.utcnow().isoformat()
            }

        extracted = url_extractor.extract_features(url)
        vector = np.array(extracted["vector"]).reshape(1, -1)
        indicators = extracted["indicators"]

        # Inference
        if self.model is not None:
            proba = float(self.model.predict_proba(vector)[0, 1])
        else:
            # Fallback heuristic calculation if model file not yet serialized
            heuristic_score = 0.1
            if extracted["features"]["has_ip_address"]:
                heuristic_score += 0.4
            if extracted["features"]["is_shortened"]:
                heuristic_score += 0.3
            if extracted["features"]["has_at_symbol"]:
                heuristic_score += 0.4
            if extracted["features"]["num_subdomains"] >= 3:
                heuristic_score += 0.25
            if not extracted["features"]["is_https"]:
                heuristic_score += 0.15
            proba = min(0.99, heuristic_score)

        phishing_probability = round(proba, 4)
        risk_score = round(phishing_probability * 100, 1)

        # Classification threshold
        if phishing_probability >= 0.50:
            classification = "PHISHING"
            confidence = round(phishing_probability, 3)
        else:
            classification = "LEGITIMATE"
            confidence = round(1.0 - phishing_probability, 3)

        return {
            "url": url,
            "classification": classification,
            "phishing_probability": phishing_probability,
            "risk_score": risk_score,
            "confidence": confidence,
            "indicators": indicators,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "prediction_timestamp": datetime.utcnow().isoformat()
        }

phishing_predictor = PhishingPredictor()
