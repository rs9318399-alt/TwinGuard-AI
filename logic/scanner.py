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

   
 # Detects whether a scanned Wi-Fi network is genuine or a possible Evil Twin
def detect_evil_twin(network, trusted):
    ssid = network["ssid"]
    bssid = network["bssid"]

    # Check if the scanned network exists in the trusted database
    if ssid not in trusted:
        return {
            "status": "Verification Required",
            "risk": "Medium",
            "reason": "This network is not registered in the trusted database.",
            "recommendation": "Verify the network before connecting."
        }
    # Compare the scanned BSSID with the trusted BSSID
    if bssid == trusted[ssid]:
        return {
            "status": "Verified",
            "risk": "Low",
            "reason": "The scanned network matches the trusted network.",
            "recommendation": "This network is verified and safe to connect."
        }
           
    # The SSID matches, but the BSSID is different
    # This indicates a possible Evil Twin attack
    return {
        "status": "Potential Evil Twin",
        "risk": "High",
        "reason": "The SSID matches a trusted network, but the BSSID is different.",
        "recommendation": "Do not connect. Verify the access point before proceeding."
    }

# Analyzes all scanned networks and returns the detection results
def analyze_networks(networks, trusted):
    results = []

    for network in networks:
        result = detect_evil_twin(network, trusted)

        results.append({
            "ssid": network["ssid"],
            "bssid": network["bssid"],
            "signal": network["signal"],
            "security": network["security"],
            "status": result["status"],
            "risk": result["risk"],
            "reason": result["reason"],
            "recommendation": result["recommendation"]
        })

    return results

    