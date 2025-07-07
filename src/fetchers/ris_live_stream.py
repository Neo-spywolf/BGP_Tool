# src/fetchers/ris_live_stream.py

import json
import threading
from websocket import WebSocketApp
from src.ml.live_detector import BGPAnomalyDetector
from src.utils.logger import logger


class RISLiveStream:
    def __init__(self, target_prefixes):
        self.target_prefixes = set(target_prefixes)
        self.detector = BGPAnomalyDetector()
        self.ws_url = "wss://ris-live.ripe.net/v1/ws/"
        self.ws_app = WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def on_open(self, ws):
        logger.info("Connected to RIPE RIS Live WebSocket")
        subscription = {
            "type": "ris_subscribe",
            "data": {
                "type": "UPDATE",
                "host": "rrc00"
            }
        }
        ws.send(json.dumps(subscription))

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["type"] != "update":
            return

        announcements = data["data"].get("announcements", [])
        for ann in announcements:
            for prefix in ann.get("prefixes", []):
                if prefix in self.target_prefixes:
                    as_path = ann.get("path", [])
                    timestamp = data["data"].get("timestamp")
                    update_event = {
                        "prefix": prefix,
                        "as_path": as_path,
                        "timestamp": timestamp
                    }
                    logger.info(f"Live BGP update for {prefix}: {as_path}")
                    prediction = self.detector.predict([update_event])[0]
                    logger.info(f"AI prediction: {'Anomaly' if prediction else 'Normal'}")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, code, msg):
        logger.warning("WebSocket closed")

    def start(self):
        thread = threading.Thread(target=self.ws_app.run_forever)
        thread.daemon = True
        thread.start()

