import pytest
from ml.live_detector import BGPAnomalyDetector
def test_detector_predict_with_mock_data():
    detector = BGPAnomalyDetector()

    # Mock events, shape must match feature engineer output expectation
    mock_events = [
        {
            "prefix": "8.8.8.0/24",
            "origin_asn": 15169,
            "timestamp": 1699161600,
            "as_path": [7018, 3356, 15169],
            "prefix_len": 24,
            "num_peers_seen": 5,
        },
        {
            "prefix": "8.8.8.0/24",
            "origin_asn": 99999,  # suspicious ASN
            "timestamp": 1699161700,
            "as_path": [7018, 99999],
            "prefix_len": 24,
            "num_peers_seen": 3,
        }
    ]

    anomalies = detector.predict(mock_events)
    # Add your assertions here based on expected anomalies output, e.g.:
    # assert isinstance(anomalies, list)
    # assert len(anomalies) >= 1

    assert isinstance(anomalies, list)
    for anomaly in anomalies:
    # Just check it's not int; or print anomaly to understand structure
          assert anomaly is not None


