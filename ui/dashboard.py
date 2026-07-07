import streamlit as st
import pandas as pd

st.set_page_config(page_title="TwinGuard-AI Dashboard", layout="wide")

st.title("🛡️ TwinGuard-AI: Evil Twin Attack Detector")
st.write("Network ko monitor karke fake WiFi access points detect karein")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Networks", "12")
with col2:
    st.metric("Suspicious APs", "2", delta="-1")
with col3:
    st.metric("Status", "Safe")
st.subheader("Detected Networks")
data = {
    'SSID': ['PTCL-5G', 'PTCL-5G', 'Jazz-4G', 'Unknown_WiFi'],
    'BSSID': ['AA:BB:CC:11:22:33', 'AA:BB:CC:11:22:34', 'DD:EE:FF:44:55:66', '99:88:77:66:55:44'],
    'Signal': [-45, -47, -60, -70],
    'Risk': ['Low', 'High', 'Low', 'Medium']
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

if st.button("Start Scanning"):
    st.success("Scanning started...")
