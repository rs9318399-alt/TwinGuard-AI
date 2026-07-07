import streamlit as st
import pandas as pd
import datetime
import time

st.set_page_config(page_title="TwinGuard-AI Dashboard", page_icon="🛡️", layout="wide")

# CSS for dark theme + cards
st.markdown("""
<style>
.stMetric {background-color: #1e1e2f; padding: 20px; border-radius: 15px; border: 1px solid #3a3a5a;}
div[data-testid="stMetricValue"] {font-size: 30px !important;}
</style>
""", unsafe_allow_html=True)

# SIDEBAR HATA DIYA HAI - YAHAN KUCH NAHI HOGA

# MAIN TITLE
st.title("🛡️ TwinGuard-AI: Evil Twin Attack Detector")
st.write("Monitor Network and Detect fake WI-FI access points")

st.success("✅ System is actively protecting your network")
st.progress(85)
st.caption("Security Level: 85%")
st.caption(f"🕒 Last Scan: {datetime.datetime.now().strftime('%d %b %Y - %I:%M:%S %p')}")

# METRIC CARDS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Networks", "12")
with col2:
    st.metric("Suspicious APs", "2", delta="-1")
with col3:
    st.metric("Status", "Safe", delta="Protected")

st.subheader("📡 Detected Networks")

data = {
    'SSID': ['PTCL-5G', 'PTCL-5G', 'Jazz-4G', 'Unknown_WiFi'],
    'BSSID': ['AA:BB:CC:11:22:33', 'AA:BB:CC:11:22:34', 'DD:EE:FF:44:55:66', '99:88:77:66:55:44'],
    'Signal': [-45, -47, -68, -70],
    'Risk': ['Low', 'High', 'Low', 'Medium']
}
df = pd.DataFrame(data)

def color_risk(val):
    if val == "High": 
        return 'background-color: #ff4b4b; color: white; font-weight: bold'
    elif val == "Medium": 
        return 'background-color: #ffa500; color: black; font-weight: bold'
    else: 
        return 'background-color: #00c853; color: white; font-weight: bold'

st.dataframe(df.style.map(color_risk, subset=['Risk']), width='stretch')

# DOWNLOAD BUTTON
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📄 Download Report as CSV",
    data=csv,
    file_name=f"Scan_Report_{datetime.datetime.now().strftime('%H%M%S')}.csv",
    mime='text/csv',
)

# GRAPH
st.subheader("📊 Signal Strength Chart")
st.bar_chart(df.set_index('SSID')['Signal'])

# ALERT SYSTEM
if "High" in df['Risk'].values:
    st.error("🚨 ALERT: Evil Twin Attack Detected on PTCL-5G!")
    st.balloons()

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🔍 Start Scanning", type="primary", width='stretch'):
        st.success("Scanning started... Please wait")
        with st.spinner("Scanning networks..."):
            time.sleep(2)
        st.info("Scan Complete!")
with col_btn2:
    if st.button("🔄 Refresh Data", width='stretch'):
        st.rerun()

st.markdown("---")
st.markdown("<center>Made by Nabiha , Kanza , Rabia | TwinGuard-AI Project 2025</center>", unsafe_allow_html=True)

