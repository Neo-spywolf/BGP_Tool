import os
import json
from flask import Flask, jsonify, abort

app = Flask(__name__)

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))

def load_latest_report():
    try:
        reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]
        if not reports:
            return None
        latest_report_file = max(reports, key=lambda f: os.path.getmtime(os.path.join(REPORTS_DIR, f)))
        with open(os.path.join(REPORTS_DIR, latest_report_file), "r") as f:
            return json.load(f)
    except Exception:
        return None

@app.route("/report/latest", methods=["GET"])
def get_latest_report():
    report = load_latest_report()
    if report is None:
        abort(404, description="No threat reports found.")
    return jsonify(report)

@app.route("/status", methods=["GET"])
def get_status():
    report = load_latest_report()
    if report is None:
        return jsonify({"hijack_active": False, "message": "No reports available."})
    return jsonify({"hijack_active": report.get("hijack_detected", False), "prefix": report.get("prefix")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

