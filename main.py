import logging
import time
import datetime
from src.fetchers.ripe_ris_live import RipeRisFetcher
from src.ml.live_detector import BGPAnomalyDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Define prefixes to monitor
PREFIXES_TO_MONITOR = [
    "8.8.8.0/24",
    "1.1.1.0/24",
    "45.143.203.0/24"
]

# Fetch interval in seconds (e.g. 15 mins)
FETCH_INTERVAL = 15 * 60

def main():
    logging.info("🚀 BGP AI Anomaly Detector started...")

    # Load ML model
    detector = BGPAnomalyDetector()

    # First run: get data from last 1 hour
    last_fetch_ts = int(time.time()) - 3600

    try:
        while True:
            logging.info("🔁 Starting fetch cycle...")
            for prefix in PREFIXES_TO_MONITOR:
                logging.info(f"📡 Fetching BGP updates for {prefix} since {datetime.datetime.utcfromtimestamp(last_fetch_ts)}")

                fetcher = RipeRisFetcher(prefix, last_timestamp=last_fetch_ts)
                events = fetcher.fetch()

                if not events:
                    logging.warning(f"⚠️ No events found for {prefix}")
                    continue

                logging.info(f"🔍 Running anomaly detection on {len(events)} events...")
                anomalies = detector.predict(events)

                for anomaly in anomalies:
                    logging.warning(f"🚨 Anomaly detected for {prefix}: {anomaly}")

            last_fetch_ts = int(time.time())

            logging.info(f"⏳ Sleeping for {FETCH_INTERVAL // 60} minutes...\n")
            time.sleep(FETCH_INTERVAL)

    except KeyboardInterrupt:
        logging.info("🛑 Stopping anomaly detector.")

if __name__ == "__main__":
    main()
