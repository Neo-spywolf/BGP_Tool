# src/visualizers/anomaly_dashboard.py

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
app.title = "BGP Anomaly Dashboard"

# In-memory list of anomaly records
anomaly_records = []

def launch_dashboard():
    app.run_server(debug=True, port=8050)

# App layout
app.layout = html.Div([
    html.H2("🔍 Real-Time BGP Anomaly Dashboard"),
    dcc.Interval(id="update-interval", interval=5000, n_intervals=0),
    dcc.Graph(id="anomaly-graph"),
    html.Div(id="table-div")
])

@app.callback(
    Output("anomaly-graph", "figure"),
    Output("table-div", "children"),
    Input("update-interval", "n_intervals")
)
def update_dashboard(n):
    if not anomaly_records:
        return px.scatter(title="No anomalies yet"), html.Div("Waiting for data...")

    df = pd.DataFrame(anomaly_records)
    fig = px.scatter(
        df,
        x="timestamp",
        y="anomaly_score",
        color="prefix",
        hover_data=["prefix", "origin_asn", "as_path", "anomaly_score"],
        title="Detected BGP Anomalies"
    )

    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(min(len(df), 10))
        ])
    ])

    return fig, table

# Method to add events from your pipeline
def add_anomaly_event(event_dict):
    event_flat = {
        "timestamp": event_dict["event"]["timestamp"],
        "prefix": event_dict["event"]["prefix"],
        "origin_asn": event_dict["event"].get("origin_asn", ""),
        "as_path": event_dict["event"].get("as_path", ""),
        "anomaly_score": event_dict["anomaly_score"]
    }
    anomaly_records.append(event_flat)

