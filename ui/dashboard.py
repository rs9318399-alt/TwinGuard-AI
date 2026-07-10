import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="TwinGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>

.main{
    background:#0f172a;
}

.block-container{
    padding-top:1rem;
}

.title{
    font-size:38px;
    color:#00E5FF;
    font-weight:bold;
}

.subtitle{
    color:white;
    font-size:18px;
}

.metric-card{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 15px rgba(0,255,255,.2);
}

.metric-number{
    color:#00E5FF;
    font-size:35px;
    font-weight:bold;
}

.metric-title{
    color:white;
    font-size:16px;
}

.alert-box{
    background:#7f1d1d;
    color:white;
    padding:15px;
    border-radius:10px;
    border-left:8px solid red;
}

.safe-box{
    background:#14532d;
    color:white;
    padding:15px;
    border-radius:10px;
    border-left:8px solid lime;
}

</style>
""",unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.image(
"https://img.icons8.com/color/96/shield.png",
width=80
)

st.sidebar.title("TwinGuard AI")

page=st.sidebar.radio(
"Navigation",
[
"Dashboard",
"WiFi Scanner",
"Threat History",
"Settings"
]
)

st.sidebar.markdown("---")

st.sidebar.success("System Online")

# ==========================
# HEADER
# ==========================

st.markdown(
'<div class="title">🛡 TwinGuard AI Dashboard</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Evil Twin WiFi Detection System</div>',
unsafe_allow_html=True
)

st.write("")

# ==========================
# DUMMY DATA
# ==========================

total_networks=12
safe_networks=9
dangerous=3
risk_score=72

# ==========================
# METRIC CARDS
# ==========================

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-number">{total_networks}</div>
    <div class="metric-title">Networks</div>
    </div>
    """,unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-number">{safe_networks}</div>
    <div class="metric-title">Safe</div>
    </div>
    """,unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-number">{dangerous}</div>
    <div class="metric-title">Threats</div>
    </div>
    """,unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-number">{risk_score}%</div>
    <div class="metric-title">Risk</div>
    </div>
    """,unsafe_allow_html=True)

st.write("")

# ==========================
# RISK GAUGE
# ==========================

fig=go.Figure(go.Indicator(
    mode="gauge+number",
    value=risk_score,
    title={"text":"Overall Risk"},
    gauge={
        "axis":{"range":[0,100]},
        "bar":{"color":"red"},
        "steps":[
            {"range":[0,30],"color":"green"},
            {"range":[30,60],"color":"orange"},
            {"range":[60,100],"color":"red"},
        ]
    }
))

st.plotly_chart(fig,use_container_width=True)
# =====================================================
# PART 2
# LIVE WIFI SCANNER + EVIL TWIN DETECTION
# =====================================================

st.markdown("## 📶 Available WiFi Networks")

# Demo Data
# Baad mein is list ko scanner.py se replace kar dena

wifi_networks = [
    {
        "SSID": "PTCL_5G",
        "BSSID": "AA:11:22:33:44:01",
        "Signal": -60,
        "Security": "WPA2"
    },
    {
        "SSID": "StormFiber",
        "BSSID": "AA:11:22:33:44:02",
        "Signal": -55,
        "Security": "WPA2"
    },
    {
        "SSID": "Airport_Free",
        "BSSID": "AA:11:22:33:44:03",
        "Signal": -70,
        "Security": "WPA2"
    },

    # Fake Evil Twin
    {
        "SSID": "Airport_Free",
        "BSSID": "DE:AD:BE:EF:11:22",
        "Signal": -25,
        "Security": "Open"
    }
]

df = pd.DataFrame(wifi_networks)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.markdown("## 🔗 Connect To Network")

selected = st.selectbox(
    "Select WiFi",
    df["SSID"]
)

selected_network = df[df["SSID"] == selected]

if st.button("Connect"):

    same_ssid = df[df["SSID"] == selected]

    if len(same_ssid) > 1:

        fake_found = False

        for i in range(len(same_ssid)):

            row = same_ssid.iloc[i]

            if (
                row["Security"] == "Open"
                or
                row["Signal"] > -35
            ):

                fake_found = True

                st.error("🚨 EVIL TWIN DETECTED!")

                st.warning(
                    f"""
SSID : {row['SSID']}

BSSID : {row['BSSID']}

Reason:

✔ Duplicate SSID

✔ Different BSSID

✔ Open Security / Strong Signal

Recommendation:

❌ Don't Connect
"""
                )

                break

        if fake_found == False:

            st.success("✅ Connected Successfully")

    else:

        st.success("✅ Safe Network Connected")

st.divider()

st.markdown("## ⚠ Threat Analysis")

duplicate = df[df.duplicated("SSID", keep=False)]

if len(duplicate):

    st.error("Duplicate WiFi Names Found")

    st.dataframe(
        duplicate,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No Duplicate SSID Found")
  # =====================================================
# PART 3
# DASHBOARD ANALYTICS & RECENT ACTIVITY
# =====================================================

import plotly.express as px
from datetime import datetime

st.divider()

st.markdown("## 📊 Security Analytics")

col1, col2 = st.columns(2)

# -------------------------
# Pie Chart
# -------------------------

with col1:

    chart_data = pd.DataFrame({
        "Status": [
            "Safe",
            "Threat"
        ],
        "Count": [
            safe_networks,
            dangerous
        ]
    })

    fig = px.pie(
        chart_data,
        values="Count",
        names="Status",
        hole=0.60,
        title="Network Status"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------
# Signal Chart
# -------------------------

with col2:

    signal_chart = px.bar(
        df,
        x="SSID",
        y="Signal",
        color="Security",
        title="WiFi Signal Strength"
    )

    signal_chart.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        signal_chart,
        use_container_width=True
    )

st.divider()

# =====================================================
# RECENT ACTIVITY
# =====================================================

st.markdown("## 📝 Recent Activity")

activity = [

    {
        "Time":"10:20 AM",
        "Event":"Scan Started"
    },

    {
        "Time":"10:21 AM",
        "Event":"4 Networks Found"
    },

    {
        "Time":"10:22 AM",
        "Event":"Duplicate SSID Detected"
    },

    {
        "Time":"10:23 AM",
        "Event":"Threat Level High"
    },

    {
        "Time":"10:24 AM",
        "Event":"User Clicked Connect"
    }

]

for item in activity:

    st.info(
        f"🕒 {item['Time']}   ➜   {item['Event']}"
    )

st.divider()

# =====================================================
# SECURITY STATUS
# =====================================================

st.markdown("## 🛡 Security Status")

if dangerous > 0:

    st.error(
        f"""
🚨 {dangerous} Suspicious Networks Found

• Duplicate SSID Detected

• Possible Evil Twin Attack

• Verify MAC Address Before Connecting
"""
    )

else:

    st.success(
        """
✅ Network Environment Looks Safe

No Evil Twin Attack Detected.
"""
    )

st.divider()

# =====================================================
# LIVE TIMELINE
# =====================================================

st.markdown("## ⏳ Scan Timeline")

timeline = [

    "✔ Scan Started",

    "✔ Networks Loaded",

    "✔ Security Checked",

    "✔ Duplicate SSID Checked",

    "✔ MAC Address Compared",

    "✔ Risk Score Calculated",

    "✔ Dashboard Updated"

]

for step in timeline:

    st.write(step)

st.divider()

# =====================================================
# DASHBOARD FOOTER
# =====================================================

st.caption(
    f"""
TwinGuard AI © 2026

Last Scan :
{datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}
"""
)
# =====================================================
# PART 4
# COMPARISON + REPORT + SUMMARY
# =====================================================

import io
from fpdf import FPDF

st.divider()
st.markdown("## 🛡 Real vs Fake WiFi Comparison")

duplicate = df[df.duplicated("SSID", keep=False)]

if len(duplicate) > 0:

    compare = duplicate.copy()

    compare["Type"] = ""

    seen = {}

    for i in compare.index:

        ssid = compare.loc[i, "SSID"]

        if ssid not in seen:
            compare.loc[i, "Type"] = "✅ Real"
            seen[ssid] = True
        else:
            compare.loc[i, "Type"] = "❌ Fake"

    st.dataframe(
        compare[
            [
                "Type",
                "SSID",
                "BSSID",
                "Signal",
                "Security"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No Evil Twin Network Found")

st.divider()

# =====================================================
# VERIFIED NETWORK
# =====================================================

st.markdown("## ⭐ Recommended Network")

safe_df = df[df["Security"] != "Open"]

if len(safe_df):

    best = safe_df.sort_values(
        by="Signal",
        ascending=False
    ).iloc[0]

    st.success(f"""
SSID : {best['SSID']}

BSSID : {best['BSSID']}

Security : {best['Security']}

Recommendation :

✅ Connect to this network.
""")

else:

    st.error("No Verified Network Available")

st.divider()

# =====================================================
# SESSION SUMMARY
# =====================================================

st.markdown("## 📊 Session Summary")

st.write(f"**Total Networks :** {total_networks}")
st.write(f"**Safe Networks :** {safe_networks}")
st.write(f"**Threat Networks :** {dangerous}")
st.write(f"**Overall Risk :** {risk_score}%")

if dangerous > 0:

    st.error(
        "High Risk Environment Detected."
    )

else:

    st.success(
        "Network Environment Safe."
    )

st.divider()

# =====================================================
# PDF REPORT
# =====================================================

st.markdown("## 📄 Generate Report")

def create_pdf():

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial","B",18)

    pdf.cell(
        0,
        10,
        "TwinGuard AI Report",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font("Arial","",12)

    pdf.cell(
        0,
        10,
        f"Total Networks : {total_networks}",
        ln=True
    )

    pdf.cell(
        0,
        10,
        f"Safe Networks : {safe_networks}",
        ln=True
    )

    pdf.cell(
        0,
        10,
        f"Threats : {dangerous}",
        ln=True
    )

    pdf.cell(
        0,
        10,
        f"Risk Score : {risk_score}%",
        ln=True
    )

    pdf.ln(10)

    pdf.multi_cell(
        0,
        10,
        "Recommendation:\nAvoid connecting to duplicate SSID networks. Verify the MAC address before connecting."
    )

  return bytes(pdf.output(dest="S"))

pdf_bytes = create_pdf()
"""
st.download_button(
    "⬇ Download PDF Report",
    pdf_bytes,
    file_name="TwinGuard_Report.pdf",
    mime="application/pdf"
)

st.divider()
"""
# =====================================================
# REFRESH BUTTON
# =====================================================

if st.button("🔄 Refresh Dashboard"):

    st.success("Dashboard Refreshed Successfully")

    st.rerun()

st.divider()

st.markdown(
"""
<center>

<h4 style="color:#00E5FF;">
🛡 TwinGuard AI
</h4>

<p style="color:gray;">
Developed By Group Zeta
</p>

</center>
""",
unsafe_allow_html=True
)
