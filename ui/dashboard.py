import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import subprocess
import re
from fpdf import FPDF
import time
import os

st.set_page_config(page_title="TwinGuard AI", page_icon="🛡️", layout="wide")

# ==========================
# CUSTOM CSS - FONT FIX KIYA
# ==========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* {font-family: 'Poppins', sans-serif!important; text-transform: none!important;}
.main{ background:#0f172a; }
.block-container{ padding-top:1rem; }
.title{ font-size:38px; color:#00E5FF; font-weight:bold; }
.subtitle{ color:white; font-size:18px; }
.metric-card{ background:#1e293b; padding:20px; border-radius:15px; text-align:center; box-shadow:0px 0px 15px rgba(0,255,255,.2); }
.metric-number{ color:#00E5FF; font-size:35px; font-weight:bold; }
.metric-title{ color:white; font-size:16px; }
</style>
""",unsafe_allow_html=True)

st.sidebar.image("https://img.icons8.com/color/96/shield.png", width=80)
st.sidebar.title("TwinGuard AI")
page=st.sidebar.radio("Navigation", ["Dashboard","WiFi Scanner","Threat History","Settings"])
st.sidebar.markdown("---")
st.sidebar.success("System Online")

st.markdown('<div class="title">🛡 TwinGuard AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Evil Twin WiFi Detection System</div>', unsafe_allow_html=True)
st.write("")

# ==========================
# REAL WIFI SCANNER FUNCTION - FIXED
# ==========================
def scan_wifi():
    networks = []
    try:
        # NETSH KA FULL PATH DIYA
        netsh_path = r"C:\Windows\System32\netsh.exe"
        if not os.path.exists(netsh_path):
            raise FileNotFoundError("netsh.exe not found")

        result = subprocess.run([netsh_path, 'wlan', 'show', 'networks', 'mode=bssid'],
                                capture_output=True, text=True, encoding='cp850', shell=True, timeout=15)
        output = result.stdout

        ssid = ""
        bssid_list = []
        signal_list = []
        security = "Unknown"

        for line in output.split('\n'):
            line = line.strip()
            if "SSID" in line and "BSSID" not in line:
                if ssid and bssid_list:
                    for j in range(len(bssid_list)):
                        networks.append({"SSID": ssid, "BSSID": bssid_list[j], "Signal": signal_list[j], "Security": security})
                    bssid_list = []
                    signal_list = []
                ssid = line.split(":")[1].strip()

            if "Authentication" in line:
                security = line.split(":")[1].strip()
            if "BSSID" in line:
                bssid_list.append(line.split(":")[1].strip())
            if "Signal" in line:
                signal_str = line.split(":")[1].strip().replace("%","")
                signal = int((int(signal_str) / 2) - 100)
                signal_list.append(signal)

        if ssid and bssid_list:
            for j in range(len(bssid_list)):
                networks.append({"SSID": ssid, "BSSID": bssid_list[j], "Signal": signal_list[j], "Security": security})

    except Exception as e:
        st.warning(f"⚠️ Real Scan Failed. Showing Demo Data. Error: {e}")
        networks = [
            {"SSID": "PTCL_5G", "BSSID": "AA:11:22:33:44:01", "Signal": -60, "Security": "WPA2-Personal"},
            {"SSID": "StormFiber", "BSSID": "AA:11:22:33:44:02", "Signal": -55, "Security": "WPA2-Personal"},
            {"SSID": "Airport_Free", "BSSID": "AA:11:22:33:44:03", "Signal": -70, "Security": "WPA2-Personal"},
            {"SSID": "Airport_Free", "BSSID": "DE:AD:BE:EF:11:22", "Signal": -25, "Security": "Open"}
        ]
    return networks

# ==========================
# EVIL TWIN DETECTION LOGIC
# ==========================
def detect_evil_twins(df):
    threats = []
    duplicate_ssids = df[df.duplicated("SSID", keep=False)]
    for ssid in duplicate_ssids["SSID"].unique():
        same_name = df[df["SSID"] == ssid]
        if len(same_name) > 1:
            for _, row in same_name.iterrows():
                if row["Security"] == "Open" or row["Signal"] > -35:
                    threats.append({"SSID": row["SSID"], "BSSID": row["BSSID"], "Reason": "Duplicate SSID + Open/Strong Signal"})
    return threats

# ==========================
# MAIN DASHBOARD
# ==========================
if st.button("🔄 Scan Networks"):
    with st.spinner("Scanning WiFi Networks..."):
        time.sleep(2)

wifi_networks = scan_wifi()
df = pd.DataFrame(wifi_networks)
total_networks = len(df)
dangerous = len(detect_evil_twins(df))
safe_networks = total_networks - dangerous
risk_score = int((dangerous / total_networks * 100) if total_networks > 0 else 0)

# METRICS
c1,c2,c3,c4=st.columns(4)
with c1: st.markdown(f"""<div class="metric-card"><div class="metric-number">{total_networks}</div><div class="metric-title">Networks</div></div>""",unsafe_allow_html=True)
with c2: st.markdown(f"""<div class="metric-card"><div class="metric-number">{safe_networks}</div><div class="metric-title">Safe</div></div>""",unsafe_allow_html=True)
with c3: st.markdown(f"""<div class="metric-card"><div class="metric-number">{dangerous}</div><div class="metric-title">Threats</div></div>""",unsafe_allow_html=True)
with c4: st.markdown(f"""<div class="metric-card"><div class="metric-number">{risk_score}%</div><div class="metric-title">Risk</div></div>""",unsafe_allow_html=True)
st.write("")

# RISK GAUGE
fig=go.Figure(go.Indicator(mode="gauge+number", value=risk_score, title={"text":"Overall Risk"},
    gauge={"axis":{"range":[0,100]}, "bar":{"color":"red"},
    "steps":[{"range":[0,30],"color":"green"},{"range":[30,60],"color":"orange"},{"range":[60,100],"color":"red"}]}))
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig,use_container_width=True)

st.markdown("## 📶 Available WiFi Networks")
st.dataframe(df, use_container_width=True, hide_index=True)
st.divider()

# ==========================
# THREAT DETECTION
# ==========================
st.markdown("## 🚨 Evil Twin Detection")
threats = detect_evil_twins(df)

if len(threats) > 0:
    for t in threats:
        st.error(f"🚨 EVIL TWIN DETECTED!")
        st.warning(f"**SSID:** {t['SSID']}\n**BSSID:** {t['BSSID']}\n**Reason:** {t['Reason']}\n\n❌ **Don't Connect**")
else:
    st.success("✅ No Evil Twin Detected. Network is Safe")

st.divider()

# PDF REPORT
st.markdown("## 📄 Generate Report")
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",18)
    pdf.cell(0, 10, "TwinGuard AI Report", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial","",12)
    pdf.cell(0, 10, f"Total Networks : {total_networks}", ln=True)
    pdf.cell(0, 10, f"Safe Networks : {safe_networks}", ln=True)
    pdf.cell(0, 10, f"Threats : {dangerous}", ln=True)
    pdf.cell(0, 10, f"Risk Score : {risk_score}%", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Recommendation:\nAvoid connecting to duplicate SSID networks with Open security. Always verify MAC address.")
    return bytes(pdf.output(dest="S"))

pdf_bytes = create_pdf()
st.download_button("⬇ Download PDF Report", pdf_bytes, file_name="TwinGuard_Report.pdf", mime="application/pdf")

st.caption(f"TwinGuard AI © 2026 | Last Scan : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}")
