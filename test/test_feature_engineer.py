import pandas as pd
import pytest
from ml.feature_engineer import extract_features

def test_extract_features_basic():
    # Prepare sample input DataFrame
    data = {
        "as_path": [[123, 456, 789], [101, 202], []],
        "origin_asn": [123, 101, 0],
        "prefix_len": [24, 24, 24],
        "num_peers_seen": [10, 5, 0],
    }
    df = pd.DataFrame(data)

    # Call the function
    result = extract_features(df)

    # Check expected columns
    assert list(result.columns) == ["origin_asn", "prefix_len", "num_peers_seen", "as_path_len"]

    # Check values for as_path_len
    expected_as_path_len = [3, 2, 0]
    assert result["as_path_len"].tolist() == expected_as_path_len

    # Check origin_asn type is int
    assert pd.api.types.is_integer_dtype(result["origin_asn"])

    # Check values for origin_asn match input
    assert result["origin_asn"].tolist() == [123, 101, 0]

    # Check prefix_len and num_peers_seen match input
    assert result["prefix_len"].tolist() == [24, 24, 24]
    assert result["num_peers_seen"].tolist() == [10, 5, 0]

@pytest.mark.parametrize("as_path, expected_len", [
    ([1, 2, 3, 4], 4),
    ([], 0),
    ([999], 1),
])
def test_extract_features_varied_as_path_len(as_path, expected_len):
    df = pd.DataFrame({
        "as_path": [as_path],
        "origin_asn": [123],
        "prefix_len": [24],
        "num_peers_seen": [1],
    })
    result = extract_features(df)
    assert result["as_path_len"].iloc[0] == expected_len
