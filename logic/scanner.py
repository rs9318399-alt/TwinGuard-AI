import json
import random

def load_networks(path="data/networks.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return data["networks"]

def simulate_evil_twin(networks):
    target = random.choice(networks)
    fake = {
        "ssid": target["ssid"],
        "bssid": f"DE:AD:BE:EF:{random.randint(10,99)}:{random.randint(10,99)}",
        "signal": -25,
        "security": "Open"
    }
    return networks + [fake]

def build_comparison(ssid, all_networks, trusted):
    real_entry = None
    fake_entry = None
    for net in all_networks:
        if net["ssid"] == ssid:
            if net["bssid"] == trusted.get(ssid):
                real_entry = net
            else:
                fake_entry = net
    return {"real": real_entry, "fake": fake_entry}