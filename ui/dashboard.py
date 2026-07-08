import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="TwinGuard-AI", layout="wide", page_icon="🛡️")

# Custom CSS for acha look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .safe-card {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    .danger-card {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([4,1])
with col1:
    st.markdown('<p class="main-header">🛡️ TwinGuard-AI: Evil Twin Attack Detector</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitor Network and Detect fake Wi-Fi access points</p>', unsafe_allow_html=True)
with col2:
    st.success("✅ System Active")

st.progress(85)
st.write("**Security Level: 85%**")
st.caption(f"🕒 Last Scan: {datetime.now().strftime('%d %b %Y - %I:%M:%S %p')}")

st.write("")

# 3 Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><h3>📶 Networks Scanned</h3><h1>24</h1></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="danger-card"><h3>⚠️ Threats Found</h3><h1>1</h1></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="safe-card"><h3>🛡️ Status</h3><h1>Safe</h1></div>', unsafe_allow_html=True)

st.write("---")
st.subheader("📡 Detected Networks")

# Sample table
data = {
    "SSID": ["PTCL-BB", "TP-LINK_2.4G", "EvilTwin_FreeWiFi"],
    "BSSID": ["AA:BB:CC:11:22:33", "DD:EE:FF:44:55:66", "00:11:22:AA:BB:CC"],
    "Signal": ["-45 dBm", "-60 dBm", "-52 dBm"],
    "Risk": ["Low", "Low", "High"]
}
st.dataframe(pd.DataFrame(data), use_container_width=True)
