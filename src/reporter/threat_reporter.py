import json
import os
from datetime import datetime
import socket

def enrich_asn_info(asns):
    enriched = []
    for asn in asns:
        try:
            whois_host = f"AS{asn}.asn.cymru.com"
            result = socket.gethostbyname(whois_host)
            enriched.append({
                "asn": asn,
                "whois_host": whois_host,
                "dns_resolved": result
            })
        except Exception:
            enriched.append({
                "asn": asn,
                "whois_host": "N/A",
                "dns_resolved": "Failed"
            })
    return enriched

def generate_threat_report(prefix, asns, detected=True):
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "prefix": prefix,
        "hijack_detected": detected,
        "origin_asns": enrich_asn_info(asns)
    }

    os.makedirs("reports", exist_ok=True)
    path = f"reports/report_{prefix.replace('/', '_')}.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path

