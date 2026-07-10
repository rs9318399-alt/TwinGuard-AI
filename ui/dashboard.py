import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import time

st.set_page_config(page_title="TwinGuard AI", page_icon="🛡️", layout="wide")

# SESSION STATE
if 'logs' not in st.session_state: st.session_state.logs = []
if 'df' not in st.session_state: st.session_state.df = pd.DataFrame()
if 'blocked_list' not in st.session_state: st.session_state.blocked_list = [] # NAYA

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* {font-family: 'Poppins', sans-serif!important; text-transform: none!important;}
.main{ background:#0f172a; }
.title{ font-size:38px; color:#00E5FF; font-weight:bold; }
.metric-card{ background:#1e293b; padding:20px; border-radius:15px; text-align:center; }
.metric-number{ color:#00E5FF; font-size:35px; font-weight:bold; }
.blocked{ background:#7f1d1d!important; border:2px solid red; }
</style>
""",unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Dashboard","Threat History","Blocked List","Settings"])
st.sidebar.title("TwinGuard AI")
st.sidebar.success("System Online")

st.markdown('<div class="title">🛡 TwinGuard AI Dashboard</div>', unsafe_allow_html=True)

# ==========================
# SCANNER
# ==========================
def scan_wifi():
    networks = []
    networks.append({"SSID": "PTCL_5G", "BSSID": "AA:11:22:33:44:01", "Signal": -55, "Security": "WPA2-Personal", "Type": "Real"})
    networks.append({"SSID": "PTCL_5G", "BSSID": "DE:AD:BE:EF:11:22", "Signal": -28, "Security": "Open", "Type": "Fake"})
    networks.append({"SSID": "StormFiber", "BSSID": "AA:11:22:33:44:02", "Signal": -60, "Security": "WPA2-Personal", "Type": "Real"})
    return networks

# ==========================
# DETECTION LOGIC
# ==========================
def check_network(row):
    reason = ""
    status = "Secure"
    
    # CHECK KARO YE BLOCKED HAI KYA
    if row["BSSID"] in st.session_state.blocked_list:
        status = "⛔ BLOCKED - FAKE"
        reason = "This BSSID is in your Blocked List. You marked it as Evil Twin."
    elif row["Type"] == "Fake":
        status = "🚨 EVIL TWIN - FAKE"
        if row["Security"] == "Open":
            reason = "Duplicate SSID with Open Security. Real routers are always encrypted."
        elif row["Signal"] > -35:
            reason = "Signal too strong. Hacker router is placed very close to you."
    else:
        status = "✅ SECURE - REAL"
        reason = "WPA2/WPA3 encryption and normal signal. This is the real router."
        
    return status, reason

# ==========================
# PDF GENERATOR
# ==========================
def create_pdf(logs_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",18)
    pdf.cell(0, 10, "TwinGuard AI - Threat Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial","",10)
    pdf.cell(0, 10, f"Report Generated: {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial","B",12)
    pdf.cell(40, 10, "Time", 1); pdf.cell(40, 10, "SSID", 1); pdf.cell(50, 10, "BSSID", 1); pdf.cell(40, 10, "Status", 1); pdf.ln()
    pdf.set_font("Arial","",9)
    for _, row in logs_df.iterrows():
        pdf.cell(40, 10, row['Time'], 1); pdf.cell(40, 10, row['SSID'], 1); pdf.cell(50, 10, row['BSSID'], 1); pdf.cell(40, 10, row['Status'], 1); pdf.ln()
    return bytes(pdf.output(dest="S"))

# ==========================
# PAGE 1: DASHBOARD
# ==========================
if page == "Dashboard":
    if st.button("🔄 Scan Networks"):
        with st.spinner("Scanning..."): 
            time.sleep(2)
            st.session_state.df = pd.DataFrame(scan_wifi())
        st.success("Scan Complete!")

    df = st.session_state.df
    if not df.empty:
        total_networks = len(df)
        dangerous = len(df[df["Type"] == "Fake"])
        safe_networks = total_networks - dangerous
        risk_score = int((dangerous / total_networks * 100))

        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("Networks", total_networks)
        with c2: st.metric("Safe", safe_networks)
        with c3: st.metric("Threats", dangerous)
        with c4: st.metric("Risk", f"{risk_score}%")
        
        st.markdown("## 📶 Click to Analyze & Block")
        
        for index, row in df.iterrows():
            # AGAR BLOCKED HAI TO CARD RED KAR DO
            card_class = "blocked" if row["BSSID"] in st.session_state.blocked_list else ""
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3,3,2,2,2])
                with col1: st.write(f"**{row['SSID']}**")
                with col2: st.write(f"{row['BSSID']}")
                with col3: st.write(f"{row['Signal']} dBm")
                with col4: st.write(f"{row['Security']}")
                with col5: 
                    if st.button(f"Check", key=f"check{index}"):
                        status, reason = check_network(row)
                        st.session_state.selected = {**row, "Status": status, "Reason": reason}
                        log_entry = {"Time": datetime.now().strftime('%d-%m %I:%M:%S %p'), "SSID": row['SSID'], "BSSID": row['BSSID'], "Status": "BLOCKED" if "BLOCKED" in status else "FAKE" if "FAKE" in status else "REAL"}
                        st.session_state.logs.append(log_entry)
                        st.rerun()
        
        st.divider()
        
        if "selected" in st.session_state:
            row = st.session_state.selected
            st.markdown("## 🔍 Analysis Result")
            st.write(f"**SSID:** {row['SSID']} | **BSSID:** {row['BSSID']}")
            
            if "FAKE" in row['Status'] or "BLOCKED" in row['Status']:
                st.error(row['Status'])
                st.warning(f"Reason: {row['Reason']}")
                if row['BSSID'] not in st.session_state.blocked_list:
                    if st.button("⛔ Block This Network"):
                        st.session_state.blocked_list.append(row['BSSID'])
                        st.success(f"{row['SSID']} added to Blocked List!")
                        st.rerun()
            else:
                st.success(row['Status'])
                st.info(f"Reason: {row['Reason']}")

# ==========================
# PAGE 2: THREAT HISTORY
# ==========================
elif page == "Threat History":
    st.markdown("## 📜 Scan Logs")
    if len(st.session_state.logs) > 0:
        logs_df = pd.DataFrame(st.session_state.logs)
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
        pdf_bytes = create_pdf(logs_df)
        st.download_button("⬇ Download PDF Report", pdf_bytes, file_name=f"TwinGuard_Report.pdf", mime="application/pdf")
    else: st.info("No logs yet.")

# ==========================
# PAGE 3: BLOCKED LIST - NAYA PAGE
# ==========================
elif page == "Blocked List":
    st.markdown("## ⛔ Blocked Networks")
    if len(st.session_state.blocked_list) > 0:
        for bssid in st.session_state.blocked_list:
            col1, col2 = st.columns([4,1])
            with col1: st.error(f"Blocked BSSID: {bssid}")
            with col2:
                if st.button("Unblock", key=bssid):
                    st.session_state.blocked_list.remove(bssid)
                    st.rerun()
    else: st.success("No networks blocked yet.")

elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    st.info("This is Demo Version. Real blocking requires Windows Admin App.")

st.caption(f"TwinGuard AI © 2026")
