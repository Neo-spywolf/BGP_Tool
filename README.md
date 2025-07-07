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

Sample output:
======================== test session starts =========================
...
test/test_feature_engineer.py ....                             [ 57%]
test/test_fetcher.py ..                                        [ 85%]
test/test_live_detector.py .                                   [100%]
========================= 7 passed in X.XXs =========================
🛠️ Installation
git clone https://github.com/Neo-spywolf/BGP_Tool.git
cd BGP_Tool

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
▶️ Running the Tool
This project is modular. You can plug in your own live feed or use the test harness:

python src/main.py

📁 Project Structure
bgp_intel_tool/
├── src/
│   ├── ml/
│   │   ├── feature_engineer.py
│   │   ├── live_detector.py
│   ├── fetcher.py
│   └── ...
├── test/
│   ├── test_feature_engineer.py
│   ├── test_live_detector.py
│   └── test_fetcher.py
├── requirements.txt
└── README.md
🤖 Machine Learning
Trained on synthetic and real-world BGP features

Can be replaced or retrained using your own dataset

Predicts anomalies like:

Suspicious AS path lengths

Rare origin ASNs

Unexpected subprefixes

🔒 Security Use Cases
Detect route hijacks

Spot subprefix takeovers

Monitor for BGP leaks and blackhole attempts

Integrate into alerting or mitigation pipelines

📜 License
MIT License
You are free to use, modify, and distribute this tool.

🙋‍♂️ Author
Ben (@Neo-spywolf)
Built with ❤️ to make BGP more secure.
