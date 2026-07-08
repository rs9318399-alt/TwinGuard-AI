import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random
import json
import os

st.set_page_config(page_title="TwinGuard-AI", layout="wide", page_icon="🛡️")

# CSS and Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main-header { font-family: 'Poppins', sans-serif; font-size: 2.4rem; font-weight: 700; color: #1E3A8A; }
    .sub-header { color: #64748B; font-size: 1.1rem; margin-bottom: 20px; }
    .metric-card-blue { background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%); padding: 20px; border-radius: 16px; color: white; text-align: center; }
    .metric-card-red { background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%); padding: 20px; border-radius: 16px; color: white; text-align: center; }
    .metric-card-green { background: linear-gradient(135deg, #059669 0%, #10B981 100%); padding: 20px; border-radius: 16px; color: white; text-align: center; }
    .metric-card h4 { margin: 0; font-size: 1rem; font-weight: 500; }
    .metric-card h2 { margin: 8px 0 0 0; font-size: 2.2rem; font-weight: 700; }
    .alert-box { padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 5px solid; }
    .alert-high { background: #FEE2E2; border-color: #EF4444; }
    .alert-med { background: #FEF3C7; border-color: #F59E0B; }
    .scan-btn button { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; font-family: 'Poppins'; font-weight: 600; border-radius: 12px; width: 100%; font-size: 1.1rem; }
    .footer { text-align: center; color: #64748B; padding-top: 30px; }
</style>
""", unsafe_allow_html=True)

# Session State
if 'alerts' not in st.session_state: st.session_state.alerts = []
if 'blocked_list' not in st.session_state: st.session_state.blocked_list = []
if 'scan_done' not in st.session_state: st.session_state.scan_done = False

# Load Trusted Baseline
if os.path.exists("baseline.json"):
    with open("baseline.json", "r") as f: baseline = json.load(f)
else:
    baseline = {"trusted_ssid": "Lab_WiFi", "trusted_bssid": "AA:BB:CC:11:22:33"}

# Header and Scan Button
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<p class="main-header">🛡️ TwinGuard-AI: Evil Twin Detection System</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time WiFi Monitoring and Threat Detection System</p>', unsafe_allow_html=True)
with col2:
    st.success("✅ System Active")

st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
if st.button("🔍 Start Network Scan", use_container_width=True):
    with st.spinner("Scanning... Checking Beacon and De-auth Frames"):
        time.sleep(2)
        st.session_state.scan_done = True
        st.session_state.scan_time = datetime.now()
        
        networks = random.randint(18, 30)
        threats = random.randint(0, 2)
        
        if threats > 0:
            new_alert = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "type": "Evil Twin Attack Detected",
                "level": "High",
                "action": "Disconnect Immediately and Block"
            }
            st.session_state.alerts.insert(0, new_alert)
            st.session_state.alerts = st.session_state.alerts[:5]
            
            if new_alert['type'] not in [b['type'] for b in st.session_state.blocked_list]:
                 st.session_state.blocked_list.append({"type": new_alert['type'], "time": new_alert['time']})
        
        st.session_state.networks = networks
        st.session_state.threats = threats
st.markdown('</div>', unsafe_allow_html=True)

# 3 Metric Cards
if st.session_state.scan_done:
    security_level = 100 - (st.session_state.threats * 25)
    st.progress(security_level)
    st.caption(f"🕒 Last Scan: {st.session_state.scan_time.strftime('%d %b %Y - %I:%M:%S %p')}")
else:
    security_level = 0
    st.caption("🕒 Last Scan: Never")

st.write("")
col1, col2, col3 = st.columns(3)
with col1: st.markdown(f'<div class="metric-card-blue"><h4>📶 Networks Scanned</h4><h2>{st.session_state.get("networks", 0)}</h2></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-card-red"><h4>⚠️ Threats Found</h4><h2>{st.session_state.get("threats", 0)}</h2></div>', unsafe_allow_html=True)
with col3: 
    status = "Safe" if st.session_state.get("threats", 0) == 0 else "At Risk"
    st.markdown(f'<div class="metric-card-green"><h4>🛡️ Security Status</h4><h2>{status}</h2></div>', unsafe_allow_html=True)

st.write("---")

# Main Dashboard
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("📡 Detected Networks")
    if st.session_state.scan_done:
        data = {
            "SSID": ["Lab_WiFi", "TP-LINK", "EvilTwin_LabWiFi", "Guest_WiFi"],
            "BSSID": ["AA:BB:CC:11:22:33", "DD:EE:FF:44:55:66", "00:11:22:AA:BB:CC", "11:22:33:DD:EE:FF"],
            "Signal_dBm": [random.randint(-70, -40) for _ in range(4)],
            "Encryption": ["WPA2", "WPA2", "Open", "WPA3"],
            "Threat Level": ["Low", "Low", "High", "Medium"]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        st.subheader("📊 Signal and Risk Analysis")
        fig = px.bar(df, x="SSID", y="Signal_dBm", color="Threat Level", 
                     color_discrete_map={"Low":"#10B981", "Medium":"#F59E0B", "High":"#EF4444"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Please click 'Start Network Scan' button first")

with col2:
    st.subheader("🚨 Live Alerts")
    if st.session_state.alerts:
        for alert in st.session_state.alerts:
            css_class = "alert-high" if alert['level'] == "High" else "alert-med"
            st.markdown(f'<div class="alert-box {css_class}"><b>Time: {alert["time"]} - {alert["type"]}</b><br><small>Action: {alert["action"]}</small></div>', unsafe_allow_html=True)
    else:
        st.write("No alerts yet")
    
    st.subheader("⛔ Blocked List")
    if st.session_state.blocked_list:
        for b in st.session_state.blocked_list:
            st.write(f"- {b['type']} | Time: {b['time']}")
    else:
        st.write("No network blocked")

# Tabs
st.write("---")
tab1, tab2 = st.tabs(["📈 Statistics", "📜 Log Viewer"])
with tab1:
    st.subheader("Today's Summary")
    st.metric("Total Threats", st.session_state.get("threats", 0))
    st.metric("De-auth Attacks", random.randint(0, 5))

with tab2:
    st.subheader("Old Alerts Record")
    st.code("2026-04-05 10:23:11 - Evil Twin Detected - Blocked\n2026-04-05 10:20:02 - Open Network Found")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Developed by Group Zeta | 2026</div>', unsafe_allow_html=True)
