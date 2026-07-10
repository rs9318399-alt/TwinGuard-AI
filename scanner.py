import subprocess
import re

def get_networks():
    networks = []
    ssid_tracker = {}

    try:
        # Windows wifi scan command
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"], 
            encoding='utf-8', 
            errors="ignore" # <-- ye theek kiya
        )

        ssid, bssid, signal, auth = "", "", 0, ""
        for line in result.split("\n"):
            line = line.strip()
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
            elif "BSSID" in line:
                bssid = line.split(":", 1)[1].strip().replace("-", ":")
            elif "Signal" in line:
                signal = int(re.findall(r'\d+', line)[0]) * -1
            elif "Authentication" in line:
                auth = line.split(":", 1)[1].strip()

                # EVIL TWIN CHECK
                net_type = "Real"
                if ssid in ssid_tracker:
                    if auth == "Open" or ssid_tracker[ssid] == "Open":
                        net_type = "Fake" # 1 real + 1 open = Evil Twin
                
                ssid_tracker[ssid] = auth # <-- ye theek kiya

                # DATA KO LIST ME DALO - ye miss tha
                networks.append({
                    "SSID": ssid, 
                    "BSSID": bssid, 
                    "Signal": signal,
                    "Security": auth, 
                    "Type": net_type
                })
    except Exception as e:
        print("Scan Error:", e)
    return networks
