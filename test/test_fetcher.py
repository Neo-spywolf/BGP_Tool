import pytest
from fetchers.ripe_ris_live import RipeRisFetcher

def test_fetcher_fetches_events():
    # Use a known prefix and None for initial timestamp to fetch last 24h
    fetcher = RipeRisFetcher("8.8.8.0/24", last_timestamp=None)
    events = fetcher.fetch()

    assert isinstance(events, list), "Fetcher should return a list"
    # Events could be empty if no data, but should never be None
    assert events is not None

def test_fetcher_with_invalid_prefix():
    fetcher = RipeRisFetcher("invalid_prefix", last_timestamp=None)
    events = fetcher.fetch()
    assert events == [] or isinstance(events, list)

