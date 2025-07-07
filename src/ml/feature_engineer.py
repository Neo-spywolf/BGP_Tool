# src/ml/feature_engineer.py

import pandas as pd

def extract_features(df: pd.DataFrame):
    df = df.copy()
    df["as_path_len"] = df["as_path"].apply(lambda x: len(x))
    df["origin_asn"] = df["origin_asn"].astype(int)
    return df[["origin_asn", "prefix_len", "num_peers_seen", "as_path_len"]]

