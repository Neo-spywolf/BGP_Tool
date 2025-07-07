# 🛰️ BGP Intelligence Tool

A real-time BGP anomaly detection system using feature engineering and machine learning. This tool helps identify suspicious BGP announcements such as hijacks, leaks, or path manipulation by analyzing routing data in real time.

---

## 🚀 Features

- Real-time or batch-based BGP event ingestion
- Feature engineering from raw BGP announcements
- Anomaly detection using a machine learning model
- Unit-tested components for high reliability
- Easily extendable for production use

---

## 🧠 How It Works

1. **BGP Events Input**:
   - Each event contains:
     - `prefix`
     - `origin_asn`
     - `timestamp`
     - `as_path`
     - (engineered): `prefix_len`, `num_peers_seen`, `as_path_len`

2. **Feature Engineering** (`feature_engineer.py`):
   - Extracts structured features needed for ML:
     - Prefix length
     - Path length
     - Number of peers (mocked/tested for now)

3. **ML-based Prediction** (`live_detector.py`):
   - A trained model (e.g., Isolation Forest or similar) predicts anomalies
   - Returns a list of flagged suspicious events

4. **Testing** (`test/`):
   - Unit tests using `pytest` for:
     - Feature engineering logic
     - Fetching module
     - Live anomaly prediction with mock data

---

## 🧪 Tests

Run all tests using:

```bash
PYTHONPATH=src pytest test/
