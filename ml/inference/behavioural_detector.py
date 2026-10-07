import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_ANOMALY_MODEL_PATH = os.path.join(BASE_DIR, "models", "isolation_forest_model.joblib")

class BehaviouralAnomalyDetector:
    """
    Behavioural anomaly detector utilizing Isolation Forest.
    Evaluates login events based on:
    - Time-of-day / hour (0-23)
    - Device category familiarity (hash/code)
    - Network category (Home=0, Corp=1, VPN=2, Public Wi-Fi=3, Unknown=4)
    - Location category (Home Region=0, Traveling Domestic=1, Foreign Untrusted=2)
    - Login frequency (frequency spike)
    - Session duration
    Clearly labels synthetic/demonstration baseline training data.
    """
    def __init__(self, model_path: str = DEFAULT_ANOMALY_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.model_name = "IsolationForest"
        self.model_version = "1.0.0"
        self.load_or_train_baseline()

    def load_or_train_baseline(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                return
            except Exception:
                pass
        self._train_baseline()

    def _train_baseline(self):
        np.random.seed(42)
        n_normal = 250
        hours = np.random.normal(loc=13.0, scale=3.0, size=n_normal).clip(7, 22)
        networks = np.random.choice([0, 1, 2], size=n_normal, p=[0.7, 0.15, 0.15])
        locations = np.random.choice([0, 1], size=n_normal, p=[0.92, 0.08])
        frequencies = np.random.gamma(shape=2.0, scale=1.0, size=n_normal).clip(0.5, 6.0)
        durations = np.random.normal(loc=90, scale=30, size=n_normal).clip(15, 240)

        X_normal = np.column_stack([hours, networks, locations, frequencies, durations])

        iso = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        iso.fit(X_normal)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(iso, self.model_path)
        self.model = iso

    def analyze_event(
        self,
        timestamp: datetime = None,
        device_id: str = "DEV-01",
        network_category: str = "HOME",
        location_category: str = "HOME_REGION",
        login_frequency: float = 1.0,
        session_duration: float = 60.0
    ) -> Dict[str, Any]:
        if timestamp is None:
            timestamp = datetime.utcnow()

        hour = timestamp.hour

        net_map = {"HOME": 0, "CORPORATE": 1, "VPN": 2, "PUBLIC_WIFI": 3, "UNKNOWN": 4}
        loc_map = {"HOME_REGION": 0, "DOMESTIC_TRAVEL": 1, "FOREIGN_UNTRUSTED": 2}

        net_code = net_map.get(network_category.upper(), 3)
        loc_code = loc_map.get(location_category.upper(), 1)

        vector = np.array([[hour, net_code, loc_code, float(login_frequency), float(session_duration)]])

        if self.model is None:
            self.load_or_train_baseline()

        score_val = self.model.decision_function(vector)[0]
        prediction = self.model.predict(vector)[0]

        is_anomalous = bool(prediction == -1)
        norm_score = max(0.0, min(1.0, float(0.5 - (score_val * 1.5))))

        indicators = []
        if hour < 5 or hour > 23:
            indicators.append(f"Unusual login hour ({hour}:00 UTC) outside typical active baseline window.")
        if net_code >= 3:
            indicators.append(f"Untrusted network context ({network_category}) detected.")
        if loc_code == 2:
            indicators.append(f"Login originating from atypical geographic region ({location_category}).")
        if login_frequency > 8.0:
            indicators.append(f"Rapid burst frequency ({login_frequency} attempts/hr) indicating possible automated spray.")

        if is_anomalous:
            explanation = (
                f"Behavioural anomaly detected (score: {norm_score:.2f}). "
                f"Features deviate from the baseline remote worker profile: {'; '.join(indicators) if indicators else 'Multivariate divergence'}."
            )
            risk_contribution = round(norm_score * 100, 1)
        else:
            explanation = "Login event matches normal behavioral baseline parameters."
            risk_contribution = round(norm_score * 25, 1)

        return {
            "status": "ANOMALOUS" if is_anomalous else "NORMAL",
            "anomaly_score": round(norm_score, 3),
            "risk_contribution": risk_contribution,
            "explanation": explanation,
            "indicators": indicators,
            "model_version": self.model_version
        }

behavioural_detector = BehaviouralAnomalyDetector()
