# src/ml/train_model.py

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from src.ml.feature_engineer import extract_features

# Simulated labeled BGP events (0 = normal, 1 = anomaly)
bgp_data = [
    {
        "prefix": "8.8.8.0/24",
        "origin_asn": 15169,
        "as_path": [3356, 15169],
        "prefix_len": 24,
        "num_peers_seen": 35,
        "label": 0
    },
    {
        "prefix": "1.1.1.0/24",
        "origin_asn": 13335,
        "as_path": [6453, 13335],
        "prefix_len": 24,
        "num_peers_seen": 5,
        "label": 1  # suspicious
    },
    {
        "prefix": "185.132.182.0/24",
        "origin_asn": 12389,
        "as_path": [1299, 9002, 12389],
        "prefix_len": 24,
        "num_peers_seen": 15,
        "label": 0
    },
    {
        "prefix": "185.132.182.0/24",
        "origin_asn": 64512,
        "as_path": [64512],
        "prefix_len": 24,
        "num_peers_seen": 2,
        "label": 1
    }
]

# Convert to DataFrame
df = pd.DataFrame(bgp_data)

# Feature engineering
X = extract_features(df)
y = df["label"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/bgp_rf_model.pkl")
print("✅ Model saved to models/bgp_rf_model.pkl")

