import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Ecosystem Matrix",
    page_icon="🌱",
    layout="wide"
)

# 🎨 CUSTOM STYLESHEET FOR DYNAMIC DROPLETS AND LEAVES
st.markdown("""
    <style>
    /* Global Entry Reset */
    @keyframes shapeFade {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Container Row Setup */
    .shape-container {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 30px 0;
        animation: shapeFade 0.5s ease-out;
    }

    /* 💧 THE LIQUID DROPLET BUTTON STYLE */
    .droplet-btn {
        width: 110px;
        height: 110px;
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        border-radius: 0% 100% 100% 100%;
        transform: rotate(45deg);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .droplet-btn:hover {
        transform: rotate(45deg) scale(1.08);
        box-shadow: 0 12px 28px rgba(2, 132, 199, 0.5);
    }
    .droplet-text {
        transform: rotate(-45deg);
        color: white;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        font-family: sans-serif;
    }

    /* 🌱 THE ECO LEAF BUTTON STYLE */
    .leaf-btn {
        width: 110px;
        height: 110px;
        background: linear-gradient(135deg, #4ade80, #16a34a);
        border-radius: 100% 0% 100% 0%;
        box-shadow: 0 8px 20px rgba(22, 163, 74, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .leaf-btn:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 12px 28px rgba(22, 163, 74, 0.5);
    }
    .leaf-text {
        color: white;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        font-family: sans-serif;
    }
    
    /* Clean text for details segment */
    .info-pane {
        padding: 20px;
        border-radius: 16px;
        border-left: 5px solid #0284c7;
        margin-top: 15px;
        background-color: rgba(2, 132, 199, 0.05);
    }
    .info-pane-green {
        padding: 20px;
        border-radius: 16px;
        border-left: 5px solid #16a34a;
        margin-top: 15px;
        background-color: rgba(22, 163, 74, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Portal Security Wall
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col_center, _ = st.columns([1, 1.4, 1])
    
    with col_center:
        st.markdown('<div style="text-align:center; padding: 20px; border-bottom:3px solid #16a34a;"><h2>🌱 Sandhar Eco Portal</h2><p>Identity Verification Terminal</p></div>', unsafe_allow_html=True)
        username = st.text_input("Matrix Operator Key", placeholder="Username ID")
        password = st.text_input("Access Authorization Token", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Secure Workspace", type="primary", use_container_width=True):
            if username == "sandhar" and password == "telemetry2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("System access codes rejected.")
    st.stop()

# 3. Load Dataset Matrix
@st.cache_data
def load_verified_spreadsheet_matrix():
    csv_data = """vertical,unit,location,grid_mvah,capex_capacity,opex_capacity,replacement_pct,dg,mitigation,emission,capex_gen,opex_gen,lat,lon
Automotive Business,SAD & SPB,Gurugram,4614.016,138,218,34,43194,1139,3354,36.582,106.451,28.4595,77.0266
Automotive Business,SAG,Gurugram,2074.867,33,0,34,17386,515,1508,33.878,0.0,28.4595,77.0266
Automotive Business,SAH,Uttarakhand,5657.6,251,129,5,66015,197,4113,104.663,166.675,30.0668,79.0193
Automotive Business,SAB,Karnataka,1779.327,0,340,93,10120,1204,1294,442.802,0.0,15.3173,75.7139
Automotive Business,SAESPL,Gurugram,0.0,0,0,0,0,0,0.0,0.0,28.4595,77.0266
Automotive Business,SAP,Pune,89.862,0,0,0,2147,0,65,0.0,0.0,18.5204,73.8567
Automotive Business,SHP,Rajasthan,881.47,400,262,60,13021,381,641,346.631,1779.14,27.0238,74.2179
Automotive Business,SAT,Tamil Nadu,511.762,0,0,0,5730,0,372,0.0,0.0,11.1271,78.6569
Sheet Metal & Allied Business,SEB & SAESPL,Gurugram,2955.38,50,300,12,0,265,2149,364.741,0.0,28.4595,77.0266
Sheet Metal & Allied Business,SCK,Karnataka,3207.975,0,0,57,0,1331,2332,0.0,0.0,15.3173,75.7139
Sheet Metal & Allied Business,SCY,Karnataka,2695.544,0,634,33,0,642,1960,883.541,0.0,15.3173,75.7139
Sheet Metal & Allied Business,SEK,Karnataka,5334.468,0,0,68,0,2651,3878,0.0,0.0,15.3173,75.7139
Sheet Metal & Allied Business,SED,Karnataka,324.721,0,0,0,0,0,236,0.0,0.0,15.3173,75.7139
Sheet Metal & Allied Business,SEH,Gujarat,939.684,0,0,0,66051,0,683,0.0,0.0,22.2587,71.1924
Sheet Metal & Allied Business,SMN,Himachal Pradesh,126.704,0,0,0,2149,0,92,0.0,0.0,31.1048,77.1734
Sheet Metal & Allied Business,SEC,Tamil Nadu,227.741,0,0,10,35217,17,166,23.029,0.0,11.1271,78.6569
Sheet Metal & Allied Business,SHN,Tamil Nadu,2079.137,0,624,19,15522,290,1512,398.942,0.0,11.1271,78.6569
Casting Machining & Tooling Business,ACM,Gurugram,3249.812,127,0,22,2200,525,2363,0.0,122.96,28.4595,77.0266
Casting Machining & Tooling Business,ACR,Gurugram,12081.709,50,0,30,5730,2653,8783,0.0,8.865,28.4595,77.0266
Casting Machining & Tooling Business,ATPL,Gurugram,394.008,36,0,8,55432,24,286,0.0,33.266,28.4595,77.0266
Casting Machining & Tooling Business,SMK,Karnataka,3891.277,0,0,62,5432,1761,2829,0.0,0.0,15.3173,75.7139
Casting Machining & Tooling Business,ACA,Karnataka,4232.325,115,0,59,1111,1825,3077,0.0,88.659,15.3173,75.7139
Casting Machining & Tooling Business,SKC,Pune,1653.615,0,604,23,11891,277,1202,381.131,381.131,18.5204,73.8567
Casting Machining & Tooling Business,SMT,Tamil Nadu,4993.382,0,0,53,0,1922,3630,0.0,0.0,11.1271,78.6569
Casting Machining & Tooling Business,ADH,Tamil Nadu,13568.541,0,336,52,68271,5176,9864,1434.144,0.0,11.1271,78.6569
Casting Machining & Tooling Business,SAL,Tamil Nadu,309.528,0,0,41,2378,926,225,0.0,0.0,11.1271,78.6569
Casting Machining & Tooling Business,ACH,Tamil Nadu,18864.562,0,0,53,0,7304,13715,3979.8,0.0,11.1271,78.6569
Cabin & Fabrication Division,SIA,Karnataka,1506.093,115,0,2,6470,22,1095,0.0,29.61,15.3173,75.7139
Cabin & Fabrication Division,SID,Pune,1659.539,0,0,0,33080,0,1206,0.0,0.0,18.5204,73.8567
Cabin & Fabrication Division,SIP,Pune,377.270,717,0,236,3490,648,274,891.451,0.0,18.5204,73.8567
Cabin & Fabrication Division,SIJ,Rajasthan,3272.25,0,0,0,14359,0,2379,0.0,0.0,27.0238,74.2179
Cabin & Fabrication Division,SIO,Tamil Nadu,1271.13,125,0,9,15220,81,924,110.985,0.0,11.1271,78.6569
Corp. Office,CORP,Gurugram,232.695,25,0,14,0,24,169,0.0,33.483,28.4595,77.0266
Corp. Office,SASPL,Tamil Nadu,159.629,0,0,41,0,48,116,0.0,66.246,11.1271,78.6569
Joint Venture Business,JSW,Gurugram,89.911,0,0,0,0,0,65,0.0,0.0,28.4595,77.0266
Joint Venture Business,SHT,Gurugram,555.811,0,0,0,0,0,404,0.0,0.0,28.4595,77.0266
Joint Venture Business,SHA,Karnataka,75.43,0,0,0,0,0,55,0.0,0.0,15.3173,75.7139
Joint Venture Business,JWS,Karnataka,90.846,0,0,0,0,0,66,0.0,0.0,15.3173,75.7139
Joint Venture Business,SAM,Gurugram,502.745,0,0,0,0,0,365,0.0,0.0,28.4595,77.0266
Joint Venture Business,SHC,Tamil Nadu,795.269,0,0,0,0,0,578,0.0,0.0,11.1271,78.6569
Plastic Business,SCD,Gurugram,2538.911,110,132,42,52045,772,1846,0.0,237.971,28.4595,77.0266"""
    
    df = pd.read_csv(io.StringIO(csv_data.strip()))
    df['total_energy_footprint'] = df['grid_mvah'] + (df['dg'] / 1000.0) + df['capex_gen'] + df['opex_gen']
    return df

df_master = load_verified_spreadsheet_matrix()

# --- INITIALIZE ACTIVE TRIGGER STATE ---
if "active_matrix_view" not in st.session_state:
    st.session_state["active_matrix_view"] = "carbon"  # default view

# --- MAIN INTERACTIVE CANVAS ---
st.title("🌱 Sandhar Nature-Inspired Matrix Workspace")
st.caption("Click on the Droplet shape or Leaf shape to seamlessly filter and reveal operational telemetry data layers.")
st.markdown("---")

# 💧 & 🌱 THE DYNAMIC ACTIVE GRID ROW
col_left_drop, col_right_leaf = st.columns(2)

with col_left_drop:
    st.markdown('<div class="shape-container">', unsafe_allow_html=True)
    if st.button("💧\nCarbon\nEmission", key="trigger_droplet", use_container_width=False):
        st.session_state["active_matrix_view"] = "carbon"
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold;'>Click Droplet for Carbon Emissions Matrix</p>", unsafe_allow_html=True)

with col_right_leaf:
    st.markdown('<div class="shape-container">', unsafe_allow_html=True)
    if st.button("🌱\nGreen\nOffset", key="trigger_leaf", use_container_width=False):
        st.session_state["active_matrix_view"] = "mitigation"
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-weight:bold;'>Click Leaf for Green Mitigation Matrix</p>", unsafe_allow_html=True)

# CSS trick to injection format native buttons to shapes
st.markdown("""
    <script>
    var buttons = window.parent.document.getElementsByTagName('button');
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].innerText.includes('Carbon')) {
            buttons[i].className = 'droplet-btn';
            buttons[i].innerHTML = '<div class="droplet-text">💧<br>Carbon<br>Output</div>';
        }
        if (buttons[i].innerText.includes('Offset')) {
            buttons[i].className = 'leaf-btn';
            buttons[i].innerHTML = '<div class="leaf-text">🌱<br>Green<br>Mitigate</div>';
        }
    }
    </script>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- DYNAMIC DATA RENDERING PANE ---
if st.session_state["active_matrix_view"] == "carbon":
    st.markdown('<div class="info-pane"><h3>💧 Dynamic Readout: Carbon Footprint Matrix</h3></div>', unsafe_allow_html=True)
    
    # Render Carbon Graph Matrix
    fig_carbon = px.bar(
        df_master, x="unit", y="emission", color="vertical",
        title="Total Factory Plant Footprint Output (MT CO₂)",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_carbon.update_layout(xaxis={'categoryorder':'total descending'}, height=400)
    st.plotly_chart(fig_carbon, use_container_width=True)
    
    # Context Metric Metrics
    c1, c2 = st.columns(2)
    c1.metric("🚨 Total Gross Emissions Across All Slices", f"{int(df_master['emission'].sum()):,} MT")
    c2.metric("📊 Average Branch Output Scale", f"{df_master['emission'].mean():,.1f} MT")

else:
    st.markdown('<div class="info-pane-green"><h3>🌱 Dynamic Readout: Green Mitigation Matrix</h3></div>', unsafe_allow_html=True)
    
    # Render Green Mitigation Graphs
    fig_mitigation = px.bar(
        df_master, x="unit", y="mitigation", color="vertical",
        title="Clean Energy Offset Slices by Plant Node (MT CO₂)",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig_mitigation.update_layout(xaxis={'categoryorder':'total descending'}, height=400)
    st.plotly_chart(fig_mitigation, use_container_width=True)
    
    # Context Metric Metrics
    w1, w2 = st.columns(2)
    w1.metric("🍏 Combined Offset Saved Volume", f"{int(df_master['mitigation'].sum()):,} MT")
    w2.metric("☀️ Mean Replacement Efficiency Percentage", f"{df_master['replacement_pct'].mean():,.1f} %")

st.markdown("---")

# --- ROW 2: TELEMETRY AI CONSOLE ---
st.subheader("🤖 Context-Aware AI Telemetry Assistant")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Ecosystem active. You can request direct metrics regarding any shape layer or plant id."}]

chat_window = st.container(height=260)
for msg in st.session_state["chat_history"]:
    chat_window.chat_message(msg["role"]).write(msg["content"])
    
if user_query := st.chat_input("Enter natural text audit criteria..."):
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    chat_window.chat_message("user").write(user_query)
    
    raw_input = user_query.lower().strip()
    reply = ""
    
    if "carbon" in raw_input or "emission" in raw_input:
        reply = f"💧 **Carbon Ledger Pull:** Combined emissions are currently tracking at **{int(df_master['emission'].sum()):,} MT**, with an average output scale of {df_master['emission'].mean():,.1f} MT per branch node."
    elif "green" in raw_input or "mitigation" in raw_input or "offset" in raw_input:
        reply = f"🌱 **Ecosystem Leaf Ledger Pull:** Total green offsets accounted for are **{int(df_master['mitigation'].sum()):,} MT** with an average solar generation shift ratio of {df_master['replacement_pct'].mean():,.1f}%."
    else:
        matched = None
        for _, row in df_master.iterrows():
            if row['unit'].lower() in raw_input:
                matched = row.to_dict()
                break
        if matched:
            reply = f"📌 **Node [{matched['unit']}]:** Carbon Footprint: {matched['emission']} MT | Green Mitigation Balance: {matched['mitigation']} MT."
        else:
            reply = "I didn't quite catch that. Try asking about 'carbon metrics', 'green offsets', or query a specific factory plant code like 'ACM'."
            
    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
    chat_window.chat_message("assistant").write(reply)
