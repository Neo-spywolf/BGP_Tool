import requests

def get_bgp_origins(prefix):
    url = f"https://stat.ripe.net/data/bgplay/data.json?resource={prefix}&rrcs=0"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            events = data['data']['events']
            origins = set()
            paths = []
            for event in events:
                if event['type'] == 'A':  # Announcement event
                    path = event.get('path', [])
                    if path:
                        origins.add(path[-1])  # Origin AS is last in path
                        paths.append(path)
            return list(origins), paths
        except KeyError:
            return [], []
    else:
        return [], []

