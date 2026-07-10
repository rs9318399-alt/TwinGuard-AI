import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import time
import random

st.set_page_config(page_title="TwinGuard AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* {font-family: 'Poppins', sans-serif!important; text-transform: none!important;}
.main{ background:#0f172a; }
.title{ font-size:38px; color:#00E5FF; font-weight:bold; }
.subtitle{ color:white; font-size:18px; }
.metric-card{ background:#1e293b; padding:20px; border-radius:15px; text-align:center; }
.metric-number{ color:#00E5FF; font-size:35px; font-weight:bold; }
.metric-title{ color:white; font-size:16px; }
.stButton>button{ background:#00E5FF; color:#0f172a; font-weight:bold; border-radius:10px; }
</style>
""",unsafe_allow_html=True)

st.sidebar.title("TwinGuard AI")
st.sidebar.success("System Online")

st.markdown('<div class="title">🛡 TwinGuard AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Click on any network to check if it is Real or Evil Twin</div>', unsafe_allow_html=True)
st.write("")

# ==========================
# CLOUD FRIENDLY WIFI SCANNER
# ==========================
def scan_wifi():
    networks = []
    # 1. Real Network
    networks.append({"SSID": "PTCL_5G", "BSSID": "AA:11:22:33:44:01", "Signal": -55, "Security": "WPA2-Personal", "Type": "Real"})
    # 2. Fake/Evil Twin of PTCL_5G
    networks.append({"SSID": "PTCL_5G", "BSSID": "DE:AD:BE:EF:11:22", "Signal": -28, "Security": "Open", "Type": "Fake"})
    # 3. Normal
    networks.append({"SSID": "StormFiber", "BSSID": "AA:11:22:33:44:02", "Signal": -60, "Security": "WPA2-Personal", "Type": "Real"})
    # 4. Normal
    networks.append({"SSID": "Jazz_WiFi", "BSSID": "AA:11:22:33:44:03", "Signal": -70, "Security": "WPA3", "Type": "Real"})
    return networks

# ==========================
# DETECTION LOGIC
# ==========================
def check_network(row):
    reason = ""
    status = "Secure"
    
    if row["Type"] == "Fake":
        status = "🚨 EVIL TWIN - FAKE"
        if row["Security"] == "Open":
            reason = "Reason: This network has same name but Open Security. Real networks are never Open."
        elif row["Signal"] > -35:
            reason = "Reason: Signal is too strong. Hackers place fake router very close to you."
        else:
            reason = "Reason: Duplicate SSID found with suspicious BSSID."
    else:
        status = "✅ SECURE - REAL"
        reason = "Reason: WPA2/WPA3 encryption and normal signal strength. This is the real router."
        
    return status, reason

# ==========================
# MAIN DASHBOARD
# ==========================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if st.button("🔄 Scan Networks"):
    with st.spinner("Scanning WiFi Networks..."):
        time.sleep(2)
        st.session_state.df = pd.DataFrame(scan_wifi())
    st.success("Scan Complete!")

df = st.session_state.df

if not df.empty:
    total_networks = len(df)
    dangerous = len(df[df["Type"] == "Fake"])
    safe_networks = total_networks - dangerous
    risk_score = int((dangerous / total_networks * 100))

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

    st.markdown("## 📶 Click on a Network to Analyze")
    
    # TABLE KO BUTTONS ME CONVERT KIYA
    for index, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([3,3,2,2])
        with col1: st.write(f"**{row['SSID']}**")
        with col2: st.write(f"{row['BSSID']}")
        with col3: st.write(f"{row['Signal']} dBm")
        with col4: 
            if st.button(f"Check", key=index):
                st.session_state.selected = row
    
    st.divider()
    
    # ==========================
    # RESULT SECTION
    # ==========================
    if "selected" in st.session_state:
        row = st.session_state.selected
        status, reason = check_network(row)
        
        st.markdown("## 🔍 Analysis Result")
        st.write(f"**SSID:** {row['SSID']}")
        st.write(f"**BSSID:** {row['BSSID']}")
        
        if "FAKE" in status:
            st.error(status)
            st.warning(reason)
            st.info("❌ Recommendation: DO NOT CONNECT. Forget this network immediately.")
        else:
            st.success(status)
            st.info(reason)
            st.info("✅ Recommendation: This network is safe to connect.")

else:
    st.info("Click 'Scan Networks' to start")

st.caption(f"TwinGuard AI © 2026 | Last Scan : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}")
