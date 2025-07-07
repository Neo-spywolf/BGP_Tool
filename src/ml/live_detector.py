# src/ml/live_detector.py

import os
import joblib
import pandas as pd
from .feature_engineer import extract_features

class BGPAnomalyDetector:
    def __init__(self, model_path="models/bgp_rf_model.pkl"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = joblib.load(model_path)

    def predict(self, bgp_events):
        """
        bgp_events: list of dicts, each dict has keys:
          - prefix
          - origin_asn
          - as_path (list)
          - prefix_len
          - num_peers_seen
        Returns list of anomaly scores (0 = normal, 1 = anomaly)
        """
        df = pd.DataFrame(bgp_events)
        X = extract_features(df)
        preds = self.model.predict(X)
        return preds.tolist()

