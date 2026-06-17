import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Ecosystem Dashboard",
    page_icon="🌱",
    layout="wide"
)

# 🎨 HIGH-PERFORMANCE CUSTOM LAYER (Bubbles, Shapes & Themes)
st.markdown("""
    <style>
    /* Global Fade-In Entry Animation */
    @keyframes smoothScaleUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .bubble-wrapper, .shape-row, .stPlotlyChart, .stExpander {
        animation: smoothScaleUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    /* 🟢 BUBBLE KPI CARD DESIGN */
    .bubble-wrapper {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        margin: 30px 0;
    }
    .kpi-circle-card {
        width: 195px;
        height: 195px;
        background: radial-gradient(circle at 30% 30%, #ffffff, #f8fafc);
        border: 2px solid #e2e8f0;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s, border-color 0.4s;
        text-align: center;
        padding: 15px;
    }
    .kpi-circle-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 20px 35px rgba(16, 185, 129, 0.18);
        border-color: #10b981;
    }
    .bubble-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .bubble-value {
        font-size: 17px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }

    /* Container Alignment for Visual Buttons */
    .shape-row {
        display: flex;
        justify-content: center;
        gap: 50px;
        margin: 25px 0;
    }

    /* 💧 CSS DROPLET SHAPE BUTTON */
    .droplet-node {
        width: 110px;
        height: 110px;
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        border-radius: 0% 100% 100% 100%;
        transform: rotate(45deg);
        box-shadow: 0 8px 22px rgba(2, 132, 199, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .droplet-node:hover {
        transform: rotate(45deg) scale(1.08);
        box-shadow: 0 12px 26px rgba(2, 132, 199, 0.45);
    }
    .droplet-inner-text {
        transform: rotate(-45deg);
        color: white;
        font-weight: bold;
        font-size: 11px;
        text-align: center;
    }

    /* 🌱 CSS LEAF SHAPE BUTTON */
    .leaf-node {
        width: 110px;
        height: 110px;
        background: linear-gradient(135deg, #4ade80, #16a34a);
        border-radius: 100% 0% 100% 0%;
        box-shadow: 0 8px 22px rgba(22, 163, 74, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .leaf-node:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 12px 26px rgba(22, 163, 74, 0.45);
    }
    .leaf-inner-text {
        color: white;
        font-weight: bold;
        font-size: 11px;
        text-align: center;
    }
    
    /* Login Portal Banner Styling */
    .portal-banner {
        text-align: center;
        border-bottom: 3px solid #16a34a;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Portal Security Wall
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col_center, _ = st.columns([1, 1.4, 1])
    
    with col_center:
        st.markdown('<div class="portal-banner"><h2>🌱 Sandhar Energy Portal</h2><p>Telemetry Identity Verification</p></div>', unsafe_allow_html=True)
        username = st.text_input("Matrix Operator Key", placeholder="Username ID")
        password = st.text_input("Access Authorization Token", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Energy Workspace", type="primary", use_container_width=True):
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

# --- INITIAL COGNITIVE STATE ---
if "matrix_chart_target" not in st.session_state:
    st.session_state["matrix_chart_target"] = "emission"

# --- SIDEBAR INTERFACE ---
st.sidebar.markdown("🔒 **Secure Session Active**")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Workspace Segment Toggles")
selected_vertical = st.sidebar.selectbox("Business Verticals", ["All Segments"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Segments" else df_master[df_master['vertical'] == selected_vertical].copy()

# --- MAIN ENERGY TERMINAL FRAME ---
st.title("🌱 Sandhar Energy Ecosystem Dashboard")
st.caption("Central command node monitoring real-time solar offset generations, utility distributions, and production carbon analytics.")
st.markdown("---")

# 🟢 1. BUBBLE-SHAPED SUMMARY METRIC MATRIX
total_grid = df_filtered['grid_mvah'].sum()
total_mit = df_filtered['mitigation'].sum()
total_emi = df_filtered['emission'].sum()

st.markdown(f"""
    <div class="bubble-wrapper">
        <div class="kpi-circle-card">
            <div class="bubble-title">⚡ Total Grid Sourced</div>
            <div class="bubble-value">{total_grid:,.1f}<br><span style="font-size:11px; font-weight:normal; color:#475569;">MVAh</span></div>
        </div>
        <div class="kpi-circle-card">
            <div class="bubble-title">🌱 Carbon Offset</div>
            <div class="bubble-value">{int(total_mit):,}<br><span style="font-size:11px; font-weight:normal; color:#475569;">MT CO₂</span></div>
        </div>
        <div class="kpi-circle-card">
            <div class="bubble-title">🏭 Total Footprint</div>
            <div class="bubble-value">{int(total_emi):,}<br><span style="font-size:11px; font-weight:normal; color:#475569;">MT CO₂</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 💧 & 🌱 2. NODE GRAPH SELECTION RIGS
st.subheader("🎨 Ecosystem Visualization Layer Selection")
col_d, col_l = st.columns(2)

with col_d:
    st.markdown('<div class="shape-row">', unsafe_allow_html=True)
    if st.button("Carbon Mode Trigger", key="d_click"):
        st.session_state["matrix_chart_target"] = "emission"
    st.markdown('</div>', unsafe_allow_html=True)

with col_l:
    st.markdown('<div class="shape-row">', unsafe_allow_html=True)
    if st.button("Green Mode Trigger", key="l_click"):
        st.session_state["matrix_chart_target"] = "mitigation"
    st.markdown('</div>', unsafe_allow_html=True)

# Inject Node Mutation Logic
st.markdown("""
    <script>
    var elements = window.parent.document.getElementsByTagName('button');
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].innerText.includes('Carbon Mode')) {
            elements[i].className = 'droplet-node';
            elements[i].innerHTML = '<div class="droplet-inner-text">💧<br>Carbon & Grid Log</div>';
        }
        if (elements[i].innerText.includes('Green Mode')) {
            elements[i].className = 'leaf-node';
            elements[i].innerHTML = '<div class="leaf-inner-text">🌱<br>Green & Solar Log</div>';
        }
    }
    </script>
    """, unsafe_allow_html=True)

# --- 3. THE UNIFIED DATA MATRIX GRAPH ---
if st.session_state["matrix_chart_target"] == "emission":
    df_melted = df_filtered.melt(
        id_vars=["unit"], 
        value_vars=["emission", "grid_mvah", "capex_gen", "opex_gen"],
        var_name="Telemetry Metric", value_name="Scale Value"
    )
    df_melted["Telemetry Metric"] = df_melted["Telemetry Metric"].replace({
        "emission": "🏭 Gross Carbon Footprint (MT CO₂)",
        "grid_mvah": "⚡ Annual Grid Drawdown (MVAh)",
        "capex_gen": "☀️ CAPEX Solar Generation (MWh)",
        "opex_gen": "⚙️ OPEX Solar Generation (MWh)"
    })
    fig_primary = px.bar(
        df_melted, x="unit", y="Scale Value", color="Telemetry Metric", barmode="group",
        title="📊 Carbon Stack Assessment vs System Infrastructure Energy Logs",
        color_discrete_sequence=["#ef4444", "#0ea5e9", "#f59e0b", "#10b981"]
    )
else:
    df_melted = df_filtered.melt(
        id_vars=["unit"], 
        value_vars=["mitigation", "grid_mvah", "capex_gen", "opex_gen"],
        var_name="Telemetry Metric", value_name="Scale Value"
    )
    df_melted["Telemetry Metric"] = df_melted["Telemetry Metric"].replace({
        "mitigation": "🍏 Clean Mitigation Volume (MT CO₂)",
        "grid_mvah": "⚡ Annual Grid Drawdown (MVAh)",
        "capex_gen": "☀️ CAPEX Solar Generation (MWh)",
        "opex_gen": "⚙️ OPEX Solar Generation (MWh)"
    })
    fig_primary = px.bar(
        df_melted, x="unit", y="Scale Value", color="Telemetry Metric", barmode="group",
        title="📊 Renewable Mitigation Impact vs System Infrastructure Energy Logs",
        color_discrete_sequence=["#22c55e", "#0ea5e9", "#f59e0b", "#10b981"]
    )

fig_primary.update_layout(height=420, margin=dict(t=40, b=15, l=10, r=10), hovermode="x unified")
st.plotly_chart(fig_primary, use_container_width=True)

st.markdown("---")

# --- 4. GEOSPATIAL MAP SEGMENT ---
st.subheader("🗺️ Telepatial Asset Distribution Node Map")
fig_global_map = px.scatter_mapbox(
    df_filtered, lat="lat", lon="lon",
    size="total_energy_footprint", color="vertical",
    hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
    zoom=4.0, height=450, color_discrete_sequence=px.colors.qualitative.Safe
)
fig_global_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_global_map, use_container_width=True)

st.markdown("---")

# --- 5. PLANT EXPANDER DETAILS ---
st.subheader("📋 Infrastructure Node Register Ledger Details")
for idx, row in df_filtered.iterrows():
    card_title = f"📦 [{row['unit']}] Location: {row['location']} — Sourced Grid: {row['grid_mvah']:,.2f} MVAh"
    
    with st.expander(card_title):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        col_f1.metric("Yearly Grid Sourcing", f"{row['grid_mvah']:,.2f} MVAh")
        col_f2.metric("Green Shift Percentage", f"{row['replacement_pct']}%")
        col_f3.metric("Diesel (DG) Sideload", f"{int(row['dg']):,} Liters")
        col_f4.metric("CAPEX Array Capacity", f"{int(row['capex_capacity']):,} kWp")
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("OPEX Array Capacity", f"{int(row['opex_capacity']):,} kWp")
        col_s2.metric("CAPEX Solar Generation", f"{row['capex_gen']:,.2f} MWh")
        col_s3.metric("OPEX Solar Generation", f"{row['opex_gen']:,.2f} MWh")
        col_s4.metric("Mitigation/Emission Ratio", f"{int(row['mitigation'])} / {int(row['emission'])} MT")

st.markdown("---")

# --- 6. 🤖 INTELLIGENT UPGRADED CONVERSATIONAL CHATBOT LOOP ---
st.subheader("🤖 Sandhar Energy Intelligence Agent")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Hello! I am your Sandhar Energy Assistant. What would you like to know about our metrics today?"}]

chat_box = st.container(height=260)
for message in st.session_state["chat_history"]:
    chat_box.chat_message(message["role"]).write(message["content"])

if prompt_str := st.chat_input("Ask about Sandhar's power metrics or say hi..."):
    st.session_state["chat_history"].append({"role": "user", "content": prompt_str})
    chat_box.chat_message("user").write(prompt_str)
    
    clean_prompt = prompt_str.lower().strip()
    ai_response = ""
    
    # Check for friendly greeting
    if clean_prompt in ["hi", "hii", "hello", "hey", "yo"]:
        ai_response = "Hello! 👋 Great to have you here. What would you like to know about Sandhar's energy tracking metrics?"
    # Check for grid analytics
    elif "grid" in clean_prompt or "drawdown" in clean_prompt:
        ai_response = f"⚡ **Sandhar Energy Audit:** Combined grid utility usage amounts to **{df_master['grid_mvah'].sum():,.2f} MVAh** across all active manufacturing installations."
    # Check for financial setup profiles
    elif "capex" in clean_prompt or "opex" in clean_prompt:
        ai_response = f"💰 **Solar Infrastructure Metrics:** Collective CAPEX solar arrays generate **{df_master['capex_gen'].sum():,.2f} MWh**, while active OPEX layout models yield **{df_master['opex_gen'].sum():,.2f} MWh**."
    # Check for a specific localized plant identifier
    else:
        located = False
        for _, r in df_master.iterrows():
            if r['unit'].lower() in clean_prompt:
                ai_response = f"🔍 **Ecosystem Record Matrix [{r['unit']}]:** Grid Sourced: {r['grid_mvah']} MVAh | Solar Gen (CAPEX): {r['capex_gen']} MWh | Solar Gen (OPEX): {r['opex_gen']} MWh."
                located = True
                break
        if not located:
            ai_response = "I couldn't quite map that. You can ask me about terms like 'yearly grid drawdowns', 'total capex fields', or inspect a specific location index like 'SAD'."

    # Appending the dynamic "What else do you want to know?" loop closer
    ai_response += " \n\n*Please let me know what else you want to know!*"
            
    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
    chat_box.chat_message("assistant").write(ai_response)
