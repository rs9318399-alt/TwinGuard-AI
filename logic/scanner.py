import json

def load_networks(path="data/networks.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data["networks"]