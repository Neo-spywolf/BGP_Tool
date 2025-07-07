# src/fetchers/ripe_ris_live.py

import requests
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class RipeRisFetcher:
    """
    Fetches recent BGP updates from RIPE RIS API and converts
    them into normalized BGP event dicts ready for anomaly detection.
    """

    BASE_URL = "https://stat.ripe.net/data/bgp-updates/data.json"

    def __init__(self, resource_prefix: str, last_timestamp: int = None):
        """
        :param resource_prefix: IP prefix string, e.g. '8.8.8.0/24'
        :param last_timestamp: UNIX timestamp to fetch updates since this time.
                               If None, fetches last 24 hours.
        """
        self.resource = resource_prefix
        self.last_timestamp = last_timestamp

    def fetch(self):
        """
        Fetches and returns a list of parsed BGP events since last_timestamp.
        Each event is a dict with keys:
          - prefix (str)
          - origin_asn (int)
          - as_path (list of ints)
          - prefix_len (int)
          - num_peers_seen (int) (approximated from peers count)
          - timestamp (datetime UTC)
        """
        params = {"resource": self.resource}
        if self.last_timestamp:
            params["starttime"] = datetime.fromtimestamp(self.last_timestamp, timezone.utc).isoformat()

        logger.info(f"Fetching RIPE RIS BGP updates for {self.resource} since {params.get('starttime', '24h ago')}")

        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=20)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch BGP updates from RIPE RIS: {e}")
            return []

        data = resp.json()
        if "data" not in data or "updates" not in data["data"]:
            logger.warning("No BGP update data found in RIPE RIS response.")
            return []

        updates = data["data"]["updates"]

        # Parse updates into BGP event dicts
        events = []
        for update in updates:
            # Each update may have announcements and withdrawals, handle announcements only
            anns = update.get("announcements", {}).get("ipv4", [])
            for ann in anns:
                prefix = ann.get("prefix")
                origin_asn = self._extract_origin_asn(update.get("path", []))
                as_path = self._parse_as_path(update.get("path", []))
                prefix_len = self._get_prefix_length(prefix)
                timestamp = datetime.fromtimestamp(update.get("timestamp"), timezone.utc)
                # Number of peers is the count of collectors for this announcement
                num_peers_seen = len(ann.get("collector", [])) if "collector" in ann else 1

                if origin_asn is None:
                    logger.debug(f"Skipping prefix {prefix} with no origin ASN.")
                    continue

                event = {
                    "prefix": prefix,
                    "origin_asn": origin_asn,
                    "as_path": as_path,
                    "prefix_len": prefix_len,
                    "num_peers_seen": num_peers_seen,
                    "timestamp": timestamp,
                }
                events.append(event)

        logger.info(f"Fetched and parsed {len(events)} BGP events from RIPE RIS")
        return events

    @staticmethod
    def _extract_origin_asn(path):
        """
        Origin ASN is typically the last ASN in the AS path.
        Return None if path is empty or malformed.
        """
        if not path or not isinstance(path, list):
            return None
        return path[-1]

    @staticmethod
    def _parse_as_path(path):
        """
        Return clean AS path as list of ASNs (ints).
        """
        if not path or not isinstance(path, list):
            return []
        # Filter only int ASNs, ignore anomalies
        return [asn for asn in path if isinstance(asn, int)]

    @staticmethod
    def _get_prefix_length(prefix):
        """
        Extract prefix length from CIDR notation string.
        E.g. '8.8.8.0/24' -> 24
        """
        if not prefix or '/' not in prefix:
            return None
        try:
            return int(prefix.split('/')[-1])
        except ValueError:
            return None

