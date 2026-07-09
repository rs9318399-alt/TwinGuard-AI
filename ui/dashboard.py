import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import random
import json
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

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
if 'show_result' not in st.session_state: st.session_state.show_result = False
if 'result_data' not in st.session_state: st.session_state.result_data = {}

# Day 5 Loading + Risk Logic
LOADING_STEPS = ["Analyzing Network...", "Checking Security...", "Comparing MAC Address...", "Calculating Risk Score..."]
RISK_WEIGHTS = {"Duplicate Name": 40, "Different MAC Address": 30, "Open Security": 20}
def calculate_risk_score(reasons): return min(sum(RISK_WEIGHTS.get(r, 0) for r in reasons), 100)
def get_recommendation(score, ssid):
    if score >= 60: return f"🚨 Don't Connect. Connect to the verified {ssid} instead."
    elif score >= 30: return "⚠️ Caution advised. Verify this network with the venue before connecting."
    else: return "✅ Network appears safe."
def evaluate_network(network):
    reasons = []
    if "EvilTwin" in network["SSID"]: reasons.extend(["Duplicate Name", "Different MAC Address"])
    if network["Encryption"] == "Open": reasons.append("Open Security")
    return reasons
def analyze_network(network): st.session_state.show_result = True; st.session_state.result_data = network

# ===== DAY 8 CODE: PDF GENERATION FUNCTION =====
def create_pdf_report(networks_scanned, threats_found, alerts):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 1. Logo - Agar ui/logo.png hai to ye chalega
    if os.path.exists("ui/logo.png"):
        c.drawImage("ui/logo.png", inch, height - 1.5*inch, width=1*inch, height=1*inch)

    # 2. Header
    c.setFont("Helvetica-Bold", 20); c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(2.2*inch, height - 1*inch, "TwinGuard-AI Scan Report")
    c.setFont("Helvetica", 10); c.setFillColor(colors.grey)
    c.drawString(2.2*inch, height - 1.2*inch, f"Generated on: {datetime.now().strftime('%d %b %Y %I:%M %p')}")

    # 3. Summary
    c.setFont("Helvetica-Bold", 14); c.setFillColor(colors.black)
    c.drawString(inch, height - 2*inch, "Scan Summary")
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - 2.4*inch, f"Total Networks Scanned: {networks_scanned}")
    c.drawString(inch, height - 2.7*inch, f"Total Threats Found: {threats_found}")
    c.drawString(inch, height - 3.0*inch, f"Security Status: {'Safe' if threats_found == 0 else 'At Risk'}")

    # 4. Alerts
    y = height - 3.5*inch
    c.setFont("Helvetica-Bold", 14); c.drawString(inch, y, "Recent Alerts")
    c.setFont("Helvetica", 10)
    for alert in alerts[:5]:
        y -= 0.3*inch
        c.drawString(inch, y, f"- {alert['time']} | {alert['type']} | Action: {alert['action']}")

    # 5. Footer
    c.setFont("Helvetica-Oblique", 8); c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 0.5*inch, "Developed by NABIHA, KANZA, RABIA | Group Zeta | TwinGuard-AI 2026")

    c.save()
    buffer.seek(0)
    return buffer
# ===== DAY 8 CODE END =====

# Header
col1, col2 = st.columns([3,1])
with col1: st.markdown('<p class="main-header">🛡️ TwinGuard-AI: Evil Twin Detection System</p>', unsafe_allow_html=True); st.markdown('<p class="sub-header">Real-time WiFi Monitoring and Threat Detection System</p>', unsafe_allow_html=True)
with col2: st.success("✅ System Active")

# Scan Button
st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
if st.button("🔍 Start Network Scan", use_container_width=True):
    with st.spinner("Scanning..."): time.sleep(2); st.session_state.scan_done = True; st.session_state.scan_time = datetime.now()
    networks = random.randint(18, 30); threats = random.randint(0, 2)
    if threats > 0: st.session_state.alerts.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "Evil Twin Attack Detected", "level": "High", "action": "Disconnect Immediately and Block"}); st.session_state.alerts = st.session_state.alerts[:5]
    st.session_state.networks = networks; st.session_state.threats = threats
st.markdown('</div>', unsafe_allow_html=True)

# Result Screen
if st.session_state.show_result:
    network = st.session_state.result_data; progress_bar = st.progress(0); status_text = st.empty()
    for i, step in enumerate(LOADING_STEPS): status_text.markdown(f"### ⏳ {step}"); progress_bar.progress((i + 1) / len(LOADING_STEPS)); time.sleep(0.6)
    status_text.empty(); progress_bar.empty(); st.write("---"); st.subheader("🚨 Threat Analysis Result")
    reasons = evaluate_network(network); risk_score = calculate_risk_score(reasons); recommendation = get_recommendation(risk_score, network['SSID'])
    col1, col2 = st.columns([1,2]); col1.metric("Risk Score", f"{risk_score}/100"); col2.metric("Network", network['SSID'])
    st.write("**Detection Reasons:**"); [st.write(f"• {r}") for r in reasons]; st.info(f"**Recommendation:** {recommendation}")
    if st.button("🔙 Back to Dashboard", type="primary", use_container_width=True): st.session_state.show_result = False; st.rerun()
    st.stop()

# Metrics + Download PDF Button
if st.session_state.scan_done:
    security_level = 100 - (st.session_state.threats * 25); st.progress(security_level)
    st.caption(f"🕒 Last Scan: {st.session_state.scan_time.strftime('%d %b %Y - %I:%M:%S %p')}")

    # DAY 8: PDF DOWNLOAD BUTTON
    pdf_buffer = create_pdf_report(st.session_state.get("networks", 0), st.session_state.get("threats", 0), st.session_state.alerts)
    st.download_button(label="📄 Download PDF Report", data=pdf_buffer, file_name=f"TwinGuard_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", mime="application/pdf", use_container_width=True)
else: st.caption("🕒 Last Scan: Never")

st.write(""); col1, col2, col3 = st.columns(3)
with col1: st.markdown(f'<div class="metric-card-blue"><h4>📶 Networks Scanned</h4><h2>{st.session_state.get("networks", 0)}</h2></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-card-red"><h4>⚠️ Threats Found</h4><h2>{st.session_state.get("threats", 0)}</h2></div>', unsafe_allow_html=True)
with col3: status = "Safe" if st.session_state.get("threats", 0) == 0 else "At Risk"; st.markdown(f'<div class="metric-card-green"><h4>🛡️ Security Status</h4><h2>{status}</h2></div>', unsafe_allow_html=True)

st.write("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["📡 Detected Networks", "🔍 Comparison", "📜 Log Viewer"])
with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Detected Networks")
        if st.session_state.scan_done:
            data = {"SSID": ["Lab_WiFi", "TP-LINK", "EvilTwin_LabWiFi", "Guest_WiFi"], "BSSID": ["AA:BB:CC:11:22:33", "DD:EE:FF:44:55:66", "00:11:22:AA:BB:CC", "11:22:33:DD:EE:FF"], "Signal_dBm": [random.randint(-70, -40) for _ in range(4)], "Encryption": ["WPA2", "WPA2", "Open", "WPA3"], "Threat Level": ["Low", "Low", "High", "Medium"]}
            df = pd.DataFrame(data)
            header_cols = st.columns([2,2,1,1,1,1]); header_cols[0].write("**SSID**"); header_cols[1].write("**BSSID**"); header_cols[2].write("**Signal**"); header_cols[3].write("**Encryption**"); header_cols[4].write("**Threat**"); header_cols[5].write("**Action**")
            for index, row in df.iterrows(): cols = st.columns([2,2,1,1,1,1]); cols[0].write(row["SSID"]); cols[1].write(row["BSSID"]); cols[2].write(row["Signal_dBm"]); cols[3].write(row["Encryption"]); cols[4].write(row["Threat Level"]);
            with cols[5]:
                    if st.button("Analyze", key=f"analyze_{index}"): analyze_network(row.to_dict()); st.rerun()
            st.subheader("📊 Signal and Risk Analysis"); fig = px.bar(df, x="SSID", y="Signal_dBm", color="Threat Level", color_discrete_map={"Low":"#10B981", "Medium":"#F59E0B", "High":"#EF4444"}); st.plotly_chart(fig, use_container_width=True)
        else: st.info("👆 Please click 'Start Network Scan' button first")
    with col2: st.subheader("🚨 Live Alerts"); [st.markdown(f'<div class="alert-box alert-high"><b>Time: {a["time"]} - {a["type"]}</b><br><small>Action: {a["action"]}</small></div>', unsafe_allow_html=True) for a in st.session_state.alerts] if st.session_state.alerts else st.write("No alerts yet"); st.subheader("⛔ Blocked List"); [st.write(f"- {b['type']} | Time: {b['time']}") for b in st.session_state.blocked_list] if st.session_state.blocked_list else st.write("No network blocked")
with tab2:
    st.subheader("🔍 Real vs Evil Twin Network Comparison")
    if st.session_state.scan_done:
        real_network = {"SSID": "Lab_WiFi", "BSSID": "AA:BB:CC:11:22:33", "Encryption": "WPA2", "Signal": "-45 dBm"}; fake_network = {"SSID": "EvilTwin_LabWiFi", "BSSID": "00:11:22:AA:BB:CC", "Encryption": "Open", "Signal": "-38 dBm"}
        comp_df = pd.DataFrame({"Property": ["SSID", "BSSID", "Encryption", "Signal Strength"], "Real Network": [real_network["SSID"], real_network["BSSID"], real_network["Encryption"], real_network["Signal"]], "Suspicious Network": [fake_network["SSID"], fake_network["BSSID"], fake_network["Encryption"], fake_network["Signal"]]})
        def highlight_diff(val, prop):
            if prop == "BSSID" and val!= real_network["BSSID"]: return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
            if prop == "Encryption" and val!= real_network["Encryption"]: return 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
            return ''
        st.dataframe(comp_df.style.apply(lambda x: [highlight_diff(v, x['Property']) for v in x], axis=1), use_container_width=True); st.error("⚠️ Mismatch Found: BSSID and Encryption do not match the trusted network. This is a likely Evil Twin attack.")
    else: st.warning("Please run a scan first to enable comparison.")
with tab3: st.subheader("Today's Summary"); st.metric("Total Threats", st.session_state.get("threats", 0)); st.metric("De-auth Attacks", random.randint(0, 5)); st.write("---"); st.subheader("Old Alerts Record"); st.code("2026-04-05 10:23:11 - Evil Twin Detected - Blocked\n2026-04-05 10:20:02 - Open Network Found")

# Footer
st.markdown("---"); st.markdown('<div class="footer">Developed by NABIHA, KANZA, RABIA | Group Zeta | 2026</div>', unsafe_allow_html=True)
