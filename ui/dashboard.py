import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import time
import random

st.set_page_config(page_title="TwinGuard AI", page_icon="🛡️", layout="wide")

# SESSION STATE FOR LOGS
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

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
</style>
""",unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Dashboard","Threat History","Settings"])
st.sidebar.title("TwinGuard AI")
st.sidebar.success("System Online")

st.markdown('<div class="title">🛡 TwinGuard AI Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Click on any network to check if it is Real or Evil Twin</div>', unsafe_allow_html=True)

# ==========================
# CLOUD FRIENDLY WIFI SCANNER
# ==========================
def scan_wifi():
    networks = []
    networks.append({"SSID": "PTCL_5G", "BSSID": "AA:11:22:33:44:01", "Signal": -55, "Security": "WPA2-Personal", "Type": "Real"})
    networks.append({"SSID": "PTCL_5G", "BSSID": "DE:AD:BE:EF:11:22", "Signal": -28, "Security": "Open", "Type": "Fake"})
    networks.append({"SSID": "StormFiber", "BSSID": "AA:11:22:33:44:02", "Signal": -60, "Security": "WPA2-Personal", "Type": "Real"})
    networks.append({"SSID": "Airport_Free", "BSSID": "AA:11:22:33:44:03", "Signal": -72, "Security": "WPA2-Personal", "Type": "Real"})
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
    pdf.cell(40, 10, "Time", 1)
    pdf.cell(40, 10, "SSID", 1)
    pdf.cell(50, 10, "BSSID", 1)
    pdf.cell(40, 10, "Status", 1)
    pdf.ln()
    
    pdf.set_font("Arial","",9)
    for _, row in logs_df.iterrows():
        pdf.cell(40, 10, row['Time'], 1)
        pdf.cell(40, 10, row['SSID'], 1)
        pdf.cell(50, 10, row['BSSID'], 1)
        pdf.cell(40, 10, row['Status'], 1)
        pdf.ln()
        
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Recommendation: Avoid connecting to networks marked as FAKE. Always verify BSSID before connecting.")
    return bytes(pdf.output(dest="S"))

# ==========================
# PAGE 1: DASHBOARD
# ==========================
if page == "Dashboard":
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

        c1,c2,c3,c4=st.columns(4)
        with c1: st.markdown(f"""<div class="metric-card"><div class="metric-number">{total_networks}</div><div class="metric-title">Networks</div></div>""",unsafe_allow_html=True)
        with c2: st.markdown(f"""<div class="metric-card"><div class="metric-number">{safe_networks}</div><div class="metric-title">Safe</div></div>""",unsafe_allow_html=True)
        with c3: st.markdown(f"""<div class="metric-card"><div class="metric-number">{dangerous}</div><div class="metric-title">Threats</div></div>""",unsafe_allow_html=True)
        with c4: st.markdown(f"""<div class="metric-card"><div class="metric-number">{risk_score}%</div><div class="metric-title">Risk</div></div>""",unsafe_allow_html=True)
        st.write("")

        fig=go.Figure(go.Indicator(mode="gauge+number", value=risk_score, title={"text":"Overall Risk"},
            gauge={"axis":{"range":[0,100]}, "bar":{"color":"red"},
            "steps":[{"range":[0,30],"color":"green"},{"range":[30,60],"color":"orange"},{"range":[60,100],"color":"red"}]}))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("## 📶 Click on a Network to Analyze")
        
        for index, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([3,3,2,2,2])
            with col1: st.write(f"**{row['SSID']}**")
            with col2: st.write(f"{row['BSSID']}")
            with col3: st.write(f"{row['Signal']} dBm")
            with col4: st.write(f"{row['Security']}")
            with col5: 
                if st.button(f"Check", key=index):
                    status, reason = check_network(row)
                    st.session_state.selected = row
                    st.session_state.selected['Status'] = status
                    st.session_state.selected['Reason'] = reason
                    
                    # LOG ME SAVE KARO
                    log_entry = {
                        "Time": datetime.now().strftime('%d-%m %I:%M:%S %p'),
                        "SSID": row['SSID'],
                        "BSSID": row['BSSID'],
                        "Status": "FAKE" if "FAKE" in status else "REAL"
                    }
                    st.session_state.logs.append(log_entry)
                    st.rerun()
        
        st.divider()
        
        if "selected" in st.session_state:
            row = st.session_state.selected
            st.markdown("## 🔍 Analysis Result")
            st.write(f"**SSID:** {row['SSID']}")
            st.write(f"**BSSID:** {row['BSSID']}")
            
            if "FAKE" in row['Status']:
                st.error(row['Status'])
                st.warning(f"Reason: {row['Reason']}")
                st.info("❌ Recommendation: DO NOT CONNECT")
            else:
                st.success(row['Status'])
                st.info(f"Reason: {row['Reason']}")
                st.info("✅ Recommendation: Safe to connect")

# ==========================
# PAGE 2: THREAT HISTORY / LOGS
# ==========================
elif page == "Threat History":
    st.markdown("## 📜 Scan Logs & Threat History")
    
    if len(st.session_state.logs) > 0:
        logs_df = pd.DataFrame(st.session_state.logs)
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
        
        st.divider()
        st.markdown("## 📄 Download PDF Report")
        pdf_bytes = create_pdf(logs_df)
        st.download_button("⬇ Download Full Report", pdf_bytes, file_name=f"TwinGuard_Report_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf")
        
        if st.button("Clear Logs"):
            st.session_state.logs = []
            st.rerun()
    else:
        st.info("No scans yet. Go to Dashboard and click 'Check' on a network.")

# ==========================
# PAGE 3: SETTINGS
# ==========================
elif page == "Settings":
    st.markdown("## ⚙️ Settings")
    st.info("This is a Cloud Demo Version. Real WiFi scanning requires local PC with Admin rights.")

st.caption(f"TwinGuard AI © 2026")
