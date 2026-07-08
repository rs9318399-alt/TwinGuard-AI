import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="TwinGuard-AI", layout="wide", page_icon="🛡️")

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1E3A8A;
    }
    .sub-header {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .metric-card-blue {
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
        padding: 20px; border-radius: 15px; color: white;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
    }
    .metric-card-red {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        padding: 20px; border-radius: 15px; color: white;
        box-shadow: 0 4px 10px rgba(220, 38, 38, 0.3);
    }
    .metric-card-green {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 20px; border-radius: 15px; color: white;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);
    }
    .metric-card h4 { margin: 0; font-size: 1rem; font-weight: 500; }
    .metric-card h2 { margin: 5px 0 0 0; font-size: 2.2rem; font-weight: 700; }
    .footer {
        text-align: center; 
        color: #64748B; 
        font-size: 0.9rem;
        padding-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
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

# ========== 3 METRIC CARDS ==========
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card-blue"><h4>📶 Networks Scanned</h4><h2>24</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card-red"><h4>⚠️ Threats Found</h4><h2>1</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card-green"><h4>🛡️ Status</h4><h2>Safe</h2></div>', unsafe_allow_html=True)

st.write("---")

# ========== DETECTED NETWORKS TABLE ==========
st.subheader("📡 Detected Networks")

# Yahan apna real data lagao. Ye sample hai
data = {
    "SSID": ["PTCL-BB", "TP-LINK_2.4G", "EvilTwin_FreeWiFi", "Home_WiFi"],
    "BSSID": ["AA:BB:CC:11:22:33", "DD:EE:FF:44:55:66", "00:11:22:AA:BB:CC", "11:22:33:DD:EE:FF"],
    "Signal": [-45, -60, -52, -70],
    "Risk": ["Low", "Low", "High", "Medium"]
}
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

# ========== GRAPHS ==========
st.write("")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Signal Strength")
    fig1 = px.bar(df, x="SSID", y="Signal", color="Risk", 
                  color_discrete_map={"Low":"#10B981", "Medium":"#F59E0B", "High":"#EF4444"})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("⚠️ Risk Distribution")
    risk_count = df["Risk"].value_counts().reset_index()
    risk_count.columns = ["Risk", "Count"]
    fig2 = px.pie(risk_count, values="Count", names="Risk",
                  color_discrete_map={"Low":"#10B981", "Medium":"#F59E0B", "High":"#EF4444"})
    st.plotly_chart(fig2, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown('<div class="footer">Made by NABIHA , KANZA , RABIA | project 2026</div>', unsafe_allow_html=True)
