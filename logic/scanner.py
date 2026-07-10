import json
import random
import time
from datetime import datetime

# =====================================================
# TwinGuard-AI Backend
# Scanner Engine
# =====================================================

# Stores every scan performed during the session
scan_logs = []

# Stores blocked suspicious networks
blocked_networks = []



# =====================================================
# Loads all available Wi-Fi networks from networks.json
# =====================================================

def load_networks(path="data/networks.json"):
    """
    Load available Wi-Fi networks from the JSON database.
    Returns a list of network dictionaries.
    """

    try:
        with open(path, "r") as file:
            data = json.load(file)

        return data.get("networks", [])

    except FileNotFoundError:
        print(f"[ERROR] Network database not found: {path}")
        return []

    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in networks.json")
        return []

    except Exception as e:
        print(f"[ERROR] {e}")
        return []
# =====================================================
# Loads trusted Wi-Fi database
# =====================================================

def load_trusted_networks(path="data/trusted_networks.json"):

    try:
        with open(path, "r") as file:
            data = json.load(file)

        return data

    except FileNotFoundError:
        print(f"[ERROR] Trusted database not found: {path}")
        return {}

    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in trusted_networks.json")
        return {}

    except Exception as e:
        print(f"[ERROR] {e}")
        return {}
    # =====================================================
# Creates a simulated Evil Twin access point
# =====================================================

def simulate_evil_twin(networks):
    """
    Creates a fake access point by copying one trusted
    network and changing its BSSID and security.
    """

    if not networks:
        return []

    # Select one genuine network randomly
    target = random.choice(networks)

    # Create a fake copy
    fake_network = target.copy()

    # Fake BSSID (MAC Address)
    fake_network["bssid"] = (
        f"DE:AD:BE:EF:"
        f"{random.randint(10,99)}:"
        f"{random.randint(10,99)}"
    )

    # Fake AP usually has stronger signal
    fake_network["signal"] = random.randint(-35, -20)

    # Fake AP often uses Open security
    fake_network["security"] = "Open"

    # Add a small label for backend use only
    fake_network["type"] = "Simulated Evil Twin"

    # Return original + fake network
    return networks + [fake_network]

# =====================================================
# Detects whether a network is genuine or suspicious
# =====================================================

def detect_evil_twin(network, trusted):
    """
    Analyze a network and determine whether it is:
    - Verified
    - Verification Required
    - Potential Evil Twin
    """

    ssid = network["ssid"]
    bssid = network["bssid"]

    detection_id = f"DET-{random.randint(1000,9999)}"

    current_date = datetime.now().strftime("%d-%b-%Y")
    current_time = datetime.now().strftime("%I:%M:%S %p")

    # -------------------------------------------------
    # Unknown Network
    # -------------------------------------------------

    if ssid not in trusted:

        confidence = random.randint(60, 75)

        return {
            "detection_id": detection_id,
            "detected_date": current_date,
            "detected_time": current_time,

            "status": "Verification Required",
            "risk": "Medium",

            "confidence": confidence,
            "category": "Unknown Network",

            "reason": "This network is not present in the trusted database.",

            "recommendation":
                "Verify the network before connecting."
        }

    # -------------------------------------------------
    # Trusted Network
    # -------------------------------------------------

    if bssid == trusted[ssid]:

        confidence = random.randint(98, 100)

        return {
            "detection_id": detection_id,
            "detected_date": current_date,
            "detected_time": current_time,

            "status": "Verified",
            "risk": "Low",

            "confidence": confidence,
            "category": "Trusted Network",

            "reason":
                "The scanned BSSID matches the trusted network.",

            "recommendation":
                "This network is verified and safe to connect."
        }

    # -------------------------------------------------
    # Potential Evil Twin
    # -------------------------------------------------

    confidence = random.randint(94, 99)

    return {
        "detection_id": detection_id,
        "detected_date": current_date,
        "detected_time": current_time,

        "status": "Potential Evil Twin",
        "risk": "High",

        "confidence": confidence,
        "category": "Evil Twin Attack",

        "reason":
            "SSID matches a trusted network but the BSSID is different.",

        "recommendation":
            "Do not connect. Verify the access point before proceeding."
    }

    # =====================================================
# Analyze all scanned networks
# =====================================================

def analyze_networks(networks, trusted):
    """
    Analyze every scanned Wi-Fi network and return
    dashboard-ready results.
    """

    results = []

    for network in networks:

        # Detect network status
        result = detect_evil_twin(network, trusted)

        # Save scan history automatically
        save_scan_log(network, result)
       
        # Prepare dashboard data
        results.append({

            "detection_id": result["detection_id"],
            "detected_date": result["detected_date"],
            "detected_time": result["detected_time"],

            "ssid": network["ssid"],
            "bssid": network["bssid"],
            "signal": network["signal"],
            "security": network["security"],

            "status": result["status"],
            "risk": result["risk"],

            "confidence": result["confidence"],
            "category": result["category"],

            "reason": result["reason"],
            "recommendation": result["recommendation"]

        })

    return results

# =====================================================
# Save every scan into scan history
# =====================================================

def save_scan_log(network, result):
    """
    Save each analyzed network into the scan history.
    """

    log = {

        "detection_id": result["detection_id"],

        "date": result["detected_date"],
        "time": result["detected_time"],

        "ssid": network["ssid"],
        "bssid": network["bssid"],

        "signal": network["signal"],
        "security": network["security"],

        "status": result["status"],
        "risk": result["risk"],

        "confidence": result["confidence"],
        "category": result["category"],

        "reason": result["reason"],
        "recommendation": result["recommendation"]

    }

    scan_logs.append(log)

    # =====================================================
# Return complete scan history
# =====================================================

def get_scan_logs():
    """
    Return all scan history.
    """

    return scan_logs

    # =====================================================
# Block a suspicious network
# =====================================================

def block_network(network, result):
    """
    Block a suspicious network and save it in the blocked list.
    """

    blocked_info = {

        "detection_id": result["detection_id"],

        "blocked_date": datetime.now().strftime("%d-%b-%Y"),
        "blocked_time": datetime.now().strftime("%I:%M:%S %p"),

        "ssid": network["ssid"],
        "bssid": network["bssid"],

        "status": result["status"],
        "risk": result["risk"],

        "confidence": result["confidence"],

        "reason": result["reason"]

    }

    blocked_networks.append(blocked_info)

    return {
        "success": True,
        "message": f'{network["ssid"]} has been blocked successfully.'
    }
    # =====================================================
# Return blocked network history
# =====================================================

def get_blocked_networks():
    """
    Return all blocked networks.
    """

    return blocked_networks

    # =====================================================
# Count High-Risk Networks
# =====================================================

def count_threats(results):
    """
    Count all High Risk (Potential Evil Twin) networks.
    """

    threats = 0

    for result in results:
        if result["risk"] == "High":
            threats += 1

    return threats


# =====================================================
# Count Verified Networks
# =====================================================

def count_safe_networks(results):
    """
    Count all verified safe networks.
    """

    safe = 0

    for result in results:
        if result["status"] == "Verified":
            safe += 1

    return safe


# =====================================================
# Count Unknown Networks
# =====================================================

def count_unknown_networks(results):
    """
    Count networks that require verification.
    """

    unknown = 0

    for result in results:
        if result["status"] == "Verification Required":
            unknown += 1

    return unknown


# =====================================================
# Calculate Security Score
# =====================================================

def calculate_security_score(results):
    """
    Calculate an overall security score (0-100).
    """

    total = len(results)

    if total == 0:
        return 100

    threats = count_threats(results)

    score = int(((total - threats) / total) * 100)

    return max(score, 0)


# =====================================================
# Generate Scan Summary
# =====================================================

def get_scan_summary(results):
    """
    Generate complete dashboard statistics.
    """

    summary = {

        "total_networks": len(results),

        "safe_networks": count_safe_networks(results),

        "unknown_networks": count_unknown_networks(results),

        "threats_found": count_threats(results),

        "security_score": calculate_security_score(results)

    }

    return summary

    # =====================================================
# Load Available Networks
# =====================================================

def load_networks(path="data/networks.json"):
    """
    Load available Wi-Fi networks from the JSON database.
    Returns a list of network dictionaries.
    """

    try:
        with open(path, "r") as file:
            data = json.load(file)

        return data.get("networks", [])

    except FileNotFoundError:
        print(f"[ERROR] Network database not found: {path}")
        return []

    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in networks.json")
        return []

    except Exception as e:
        print(f"[ERROR] {e}")
        return []
    
    # =====================================================
# Build Real vs Evil Twin Comparison
# =====================================================

def build_comparison(ssid, scanned_networks, trusted):
    """
    Compare the genuine network with a suspicious one
    having the same SSID.
    """

    comparison = {
        "real": None,
        "suspicious": None
    }

    for network in scanned_networks:

        if network["ssid"] != ssid:
            continue

        if network["bssid"] == trusted.get(ssid):
            comparison["real"] = network
        else:
            comparison["suspicious"] = network

    return comparison

    # =====================================================
# Complete Scan Process
# =====================================================

def scan_wifi():
    """
    Main backend function.
    Loads networks, simulates Evil Twin,
    analyzes them and returns everything
    required by the dashboard.
    """

    # Load JSON databases
    networks = load_networks()
    trusted = load_trusted_networks()

    # Create simulated Evil Twin
    scanned_networks = simulate_evil_twin(networks)

    # Analyze
    results = analyze_networks(scanned_networks, trusted)

    # Dashboard summary
    summary = get_scan_summary(results)

    return {
        "results": results,
        "summary": summary,
        "logs": get_scan_logs(),
        "blocked": get_blocked_networks()
    }

    # =====================================================
# Backend Test
# =====================================================

if __name__ == "__main__":

    print("\n========== TwinGuard-AI Backend Test ==========\n")

    data = scan_wifi()

    print("Scan Summary:")
    print(data["summary"])

    print("\nDetected Networks:\n")

    for network in data["results"]:
        print(network)

    print("\nScan Logs:\n")
    print(data["logs"])

    print("\nBlocked Networks:\n")
    print(data["blocked"])

    print("\n========== Test Completed ==========")