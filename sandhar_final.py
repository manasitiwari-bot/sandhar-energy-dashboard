import streamlit as st
import pandas as pd
import plotly.express as px
import io
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Ecosystem Dashboard",
    page_icon="🌱",
    layout="wide"
)

# --- INITIAL STATE MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "matrix_chart_target" not in st.session_state:
    st.session_state["matrix_chart_target"] = "emission"

# 🎨 HIGH-PERFORMANCE CUSTOM LAYER
if not st.session_state["authenticated"]:
    st.markdown("""
        <style>
        /* Immersive Deep Space Background */
        .stApp {
            background: #030712 !important;
            overflow: hidden;
        }
        
        /* Premium Floating Glassmorphism Portal Core */
        div[data-testid="stVerticalBlock"] > div:has(.auth-card-wrap) {
            background: rgba(11, 19, 43, 0.88) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 45px !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7);
            z-index: 10;
            position: relative;
            margin-top: -120px;
        }
        
        .portal-banner h2 {
            color: #4ade80 !important;
            font-weight: 800 !important;
            text-shadow: 0 0 10px rgba(74, 222, 128, 0.2);
        }
        .portal-banner p {
            color: #94a3b8 !important;
        }
        label {
            color: #cbd5e1 !important;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
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
        </style>
        """, unsafe_allow_html=True)


# 2. Portal Security Wall
if not st.session_state["authenticated"]:
    # 🌍 Pure Procedural CSS/HTML 3D Rotating Planet Module (No images needed, perfectly robust)
    components.html("""
        <div style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:#02040a; overflow:hidden; z-index:-1; display:flex; justify-content:center; align-items:center;">
            <div style="position:absolute; width:100%; height:100%; background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px); background-size: 400px 400px; opacity:0.25;"></div>
            
            <div class="earth-sphere"></div>
        </div>
        <style>
        .earth-sphere {
            position: relative;
            width: 480px;
            height: 480px;
            border-radius: 50%;
            
            /* Generates realistic continental shifting and surface motion using CSS patterns */
            background: 
                radial-gradient(circle at 30% 30%, rgba(16, 185, 129, 0.8) 0%, transparent 60%),
                radial-gradient(circle at 75% 60%, rgba(14, 165, 233, 0.9) 0%, transparent 50%),
                radial-gradient(circle at 10% 80%, rgba(56, 189, 248, 0.85) 0%, transparent 45%),
                linear-gradient(90deg, #1e3a8a 0%, #0f172a 100%);
            background-size: 200% 100%;
            
            /* Powerful atmospheric lighting masks to turn a flat circle into a deep 3D globe */
            box-shadow: 
                inset 40px 0 110px rgba(0, 0, 0, 0.95),
                inset -20px 0 70px rgba(56, 189, 248, 0.4),
                0 0 50px rgba(14, 165, 233, 0.3);
                
            animation: planetRotation 25s linear infinite;
        }
        @keyframes planetRotation {
            0% { background-position: 0% 50%; transform: rotate(0deg); }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; transform: rotate(360deg); }
        }
        </style>
    """, height=520)

    _, col_center, _ = st.columns([1, 1.2, 1])
    with col_center:
        st.markdown('<div class="auth-card-wrap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="portal-banner" style="text-align: center; margin-bottom:20px;"><h2>🌱 Sandhar Energy Portal</h2><p>Ecosystem Identity Verification Matrix</p></div>', unsafe_allow_html=True)
        
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


# 3. Load Datasets
@st.cache_data
def load_energy_data_matrices():
    master_csv = """vertical,unit,location,grid_mvah,capex_capacity,opex_capacity,replacement_pct,dg,mitigation,emission,capex_gen,opex_gen,lat,lon,unit_lost_inefficiency,generation_per_kwp
Automotive Business,SAG,Gurugram,2074.867,33,0,34,17386,515,1508,33.878,0.0,28.4595,77.0266,4933,2.81
Plastic Business,SCD,Gurugram,2538.911,110,132,42,52045,772,1846,0.0,237.971,28.4595,77.0266,54539,1.93
Sheet Metal & Allied Business,SEB & SAESPL,Gurugram,2955.38,50,300,12,0,265,2149,364.741,0.0,28.4595,77.0266,0,3.28
Automotive Business,SAD & SPB,Gurugram,4614.016,138,218,34,43194,1139,3354,36.582,106.451,28.4595,77.0266,54909,2.86
Casting Machining & Tooling Business,ACR,Gurugram,12081.709,50,0,30,5730,2653,8783,0.0,8.865,28.4595,77.0266,24938,2.79
Casting Machining & Tooling Business,ATPL,Gurugram,394.008,36,0,8,55432,24,286,0.0,33.266,28.4595,77.0266,0,2.20
Casting Machining & Tooling Business,ACM,Gurugram,3249.812,127,0,22,2200,525,2363,0.0,122.96,28.4595,77.0266,51085,0.49
Corp. Office,CORP,Gurugram,232.695,25,0,14,0,24,169,0.0,33.483,28.4595,77.0266,9898,2.53
Corp. Office,SASPL,Tamil Nadu,159.629,0,0,41,0,48,116,0.0,66.246,11.1271,78.6569,29313,2.65
Automotive Business,SHP,Rajasthan,881.47,400,262,60,13021,381,641,346.631,1779.14,27.0238,74.2179,113748,3.67
Automotive Business,SAH,Uttarakhand,5657.6,251,129,5,66015,197,4113,104.663,166.675,30.0668,79.0193,167105,1.21
Casting Machining & Tooling Business,ACH,Tamil Nadu,18864.562,0,0,53,0,7304,13715,3979.8,0.0,11.1271,78.6569,0,2.14
Automotive Business,SIO,Tamil Nadu,1271.13,125,0,9,15220,81,924,110.985,0.0,11.1271,78.6569,0,2.70
Casting Machining & Tooling Business,ACA,Karnataka,4232.325,115,0,59,1111,1825,3077,0.0,88.659,15.3173,75.7139,45077,2.79
Automotive Business,SAB,Karnataka,1779.327,0,340,93,10120,1204,1294,442.802,0.0,15.3173,75.7139,0,2.31
Sheet Metal & Allied Business,SCY,Karnataka,2695.544,0,634,33,0,642,1960,883.541,0.0,15.3173,75.7139,0,3.05
Cabin & Fabrication Division,SIP,Pune,377.270,717,0,236,3490,648,274,891.451,0.0,18.5204,73.8567,13106,2.77
Cabin & Fabrication Division,SIA,Karnataka,1506.093,115,0,2,6470,22,1095,0.0,29.61,15.3173,75.7139,39572,2.11
Casting Machining & Tooling Business,SKC,Pune,1653.615,0,604,23,11891,277,1202,381.131,381.131,18.5204,73.8567,0,3.55
Sheet Metal & Allied Business,SHN,Tamil Nadu,2079.137,0,624,19,15522,290,1512,398.942,0.0,11.1271,78.6569,0,3.66"""
    
    monthly_csv = """Month,SAG,SCD,SEB,SAD,SCR,STPL,ACM,CORP,SASPL,SHP,SAH,SCH,SIO,SCA,SAB,SCY,SIP,SIA,SKC,SHN
April'25,3485,10249,17726,40557,15257,0,1264,3601,15245,3706,9800,31944,0,20850,0,39342,10218,12227,42814,86464
May'25,3687,9419,17707,36932,14781,0,1190,2933,12851,3638,8940,32448,0,19683,0,37537,11909,11436,40013,82349
June'25,3391,8710,15864,31688,13223,0,1018,3049,11281,2992,8220,28288,0,16839,0,35972,13190,10015,35427,61745
July'25,2869,5484,14493,30147,12845,0,460,2646,8561,2909,4560,28240,25768,14725,0,32358,12390,8971,30837,62178
Aug'25,2752,6140,13680,26324,11196,0,393,2053,6889,2635,4440,26032,29749,15949,0,31728,12157,7923,31711,65369
September'25,2891,6060,13844,36867,14327,15410,611,2466,9763,3142,7860,29400,14113,24714,0,33104,11837,8969,33565,63908
October'25,2250,7097,9495,26940,11282,14092,797,2779,10306,2723,7950,32049,16986,29842,11447,32291,9577,7854,35547,72851
November'25,2340,5260,8922,19260,8443,13167,761,2297,10119,2048,5220,26651,14814,28687,12762,25974,8800,5768,30739,52266
December'25,2280,2275,9758,23075,7946,9703,339,2202,7651,1998,5076,19608,13483,20253,9214,27711,8983,5155,35319,57275
January'26,2412,2669,9791,26570,8569,8815,160,2349,6286,1998,4036,12138,17977,21261,9772,22537,7800,3233,36920,75108
February'26,2412,5870,12243,28750,8867,12288,527,2961,10810,2577,0,22518,26434,26236,12536,25500,8688,3274,40764,78627
March'26,2980,8118,14945,37631,13787,21774,1345,3750,13198,3110,0,24377,31963,15633,16825,30604,10728,3834,46710,89358"""

    df_m = pd.read_csv(io.StringIO(master_csv.strip()))
    df_t = pd.read_csv(io.StringIO(monthly_csv.strip()))
    df_m['total_energy_footprint'] = df_m['grid_mvah'] + (df_m['dg'] / 1000.0) + df_m['capex_gen'] + df_m['opex_gen']
    return df_m, df_t

df_master, df_monthly = load_energy_data_matrices()

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("🔒 **Telemetry Link Stable**")
if st.sidebar.button("Log Out Context"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Selection Filters")
selected_vertical = st.sidebar.selectbox("Business Segment", ["All Segments"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Segments" else df_master[df_master['vertical'] == selected_vertical].copy()

target_month = st.sidebar.select_slider("Select Target Tracking Month (FY25-26)", options=list(df_monthly['Month']))

# --- HEADER FRAME ---
st.title("🌱 Sandhar Energy Ecosystem Dashboard")
st.caption("Central intelligence array mapped with high-fidelity asset nodes, monthly timeline metrics, and conversational automation layers.")
st.markdown("---")

# 🟢 1. BUBBLE KPI CARDS
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
            <div class="bubble-title">🏭 Gross Footprint</div>
            <div class="bubble-value">{int(total_emi):,}<br><span style="font-size:11px; font-weight:normal; color:#475569;">MT CO₂</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 💧 & 🌱 2. VISUAL LAYERING SELECTION TRIGGERS
st.subheader("🎨 Toggle Layer Perspectives")
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

st.markdown("""
    <script>
    var elements = window.parent.document.getElementsByTagName('button');
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].innerText.includes('Carbon Mode')) {
            elements[i].className = 'droplet-node';
            elements[i].innerHTML = '<div class="droplet-inner-text">💧<br>Carbon View</div>';
        }
        if (elements[i].innerText.includes('Green Mode')) {
            elements[i].className = 'leaf-node';
            elements[i].innerHTML = '<div class="leaf-inner-text">🌱<br>Green View</div>';
        }
    }
    </script>
    """, unsafe_allow_html=True)

# --- 3. TIMELINE TREND LINES (BULLETPROOF HIGH-PERFORMANCE MATCH LOOP) ---
st.subheader(f"📈 Ecosystem Performance Sequence Mapping ({target_month})")
df_month_melted = df_monthly.melt(id_vars=["Month"], var_name="Unit", value_name="Generation_kWh")

# Cleanly map shorthand names to identify rows without triggering index slice array errors
active_units = [str(u).split() for u in df_filtered['unit'].unique()]
df_month_filtered = df_month_melted[df_month_melted['Unit'].isin(df_monthly.columns[1:])]

fig_timeline = px.line(
    df_month_filtered, x="Month", y="Generation_kWh", color="Unit", markers=True,
    title="📅 Year-Round Active Generation Yield Timeline (kWh)",
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_timeline.update_layout(height=350, hovermode="x unified")
st.plotly_chart(fig_timeline, use_container_width=True)

# --- 4. THE UNIFIED DATA MATRIX GRAPH ---
if st.session_state["matrix_chart_target"] == "emission":
    df_melted = df_filtered.melt(id_vars=["unit"], value_vars=["emission", "grid_mvah", "capex_gen", "opex_gen"], var_name="Metric", value_name="Value")
    fig_primary = px.bar(df_melted, x="unit", y="Value", color="Metric", barmode="group", title="📊 Carbon Stack Assessment vs System Infrastructure Energy Logs", color_discrete_sequence=["#ef4444", "#0ea5e9", "#f59e0b", "#10b981"])
else:
    df_melted = df_filtered.melt(id_vars=["unit"], value_vars=["mitigation", "grid_mvah", "capex_gen", "opex_gen"], var_name="Metric", value_name="Value")
    fig_primary = px.bar(df_melted, x="unit", y="Value", color="Metric", barmode="group", title="📊 Renewable Mitigation Impact vs System Infrastructure Energy Logs", color_discrete_sequence=["#22c55e", "#0ea5e9", "#f59e0b", "#10b981"])

fig_primary.update_layout(height=380, hovermode="x unified")
st.plotly_chart(fig_primary, use_container_width=True)

st.markdown("---")

# --- 5. GEOSPATIAL MAP SEGMENT ---
st.subheader("🗺️ Telepatial Asset Distribution Node Map")
fig_global_map = px.scatter_mapbox(df_filtered, lat="lat", lon="lon", size="total_energy_footprint", color="vertical", hover_name="unit", hover_data=["location", "grid_mvah", "emission"], zoom=4.0, height=400, color_discrete_sequence=px.colors.qualitative.Safe)
fig_global_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_global_map, use_container_width=True)

st.markdown("---")

# --- 6. PLANT DETAILS LEDGER ---
st.subheader("📋 Infrastructure Node Register Ledger Details")

name_map = {
    "SAG": "SAG", "SCD": "SCD", "SEB & SAESPL": "SEB", "SAD & SPB": "SAD",
    "ACR": "SCR", "ATPL": "STPL", "ACM": "ACM", "CORP": "CORP", "SASPL": "SASPL",
    "SHP": "SHP", "SAH": "SAH", "ACH": "SCH", "SIO": "SIO", "ACA": "SCA",
    "SAB": "SAB", "SCY": "SCY", "SIP": "SIP", "SIA": "SIA", "SKC": "SKC", "SHN": "SHN"
}

for idx, row in df_filtered.iterrows():
    unit_string = str(row['unit']).strip()
    monthly_col_name = name_map.get(unit_string, None)
    
    current_mon_val = 0
    if monthly_col_name and monthly_col_name in df_monthly.columns:
        matching_rows = df_monthly.loc[df_monthly['Month'] == target_month, monthly_col_name].values
        if len(matching_rows) > 0:
            current_mon_val = matching_rows
            
    card_title = f"📦 [{row['unit']}] Location: {row['location']} — Selected Month ({target_month}): {int(current_mon_val):,} Generation Units"
    
    with st.expander(card_title):
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        col_f1.metric("Yearly Grid Sourcing", f"{row['grid_mvah']:,.2f} MVAh")
        col_f2.metric("Green Shift Percentage", f"{row['replacement_pct']}%")
        col_f3.metric("Diesel (DG) Sideload", f"{int(row['dg']):,} Liters")
        col_f4.metric("Generation per KWP Ratio", f"{row['generation_per_kwp']} Yield")
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("CAPEX / OPEX Capacities", f"{int(row['capex_capacity'])} / {int(row['opex_capacity'])} kWp")
        col_s2.metric("CAPEX Solar Generation", f"{row['capex_gen']:,.2f} MWh")
        col_s3.metric("OPEX Solar Generation", f"{row['opex_gen']:,.2f} MWh")
        col_s4.metric("Lost Due to Inefficiency", f"{int(row['unit_lost_inefficiency']):,} Units", delta=f"-{int(row['unit_lost_inefficiency'])} Units", delta_color="inverse")

st.markdown("---")

# --- 7. 🤖 CONVERSATIONAL INTELLIGENCE CHATBOT LOOP ---
st.subheader("🤖 Sandhar Energy Intelligence Agent")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Hello! I am your Sandhar Energy Assistant. I have indexed our monthly matrix profiles. What would you like to know about our metrics today?"}]

chat_box = st.container(height=260)
for message in st.session_state["chat_history"]:
    chat_box.chat_message(message["role"]).write(message["content"])

if prompt_str := st.chat_input("Ask about monthly outputs, inefficient loads, or say hi..."):
    st.session_state["chat_history"].append({"role": "user", "content": prompt_str})
    chat_box.chat_message("user").write(prompt_str)
    
    clean_prompt = prompt_str.lower().strip()
    ai_response = ""
    
    if clean_prompt in ["hi", "hii", "hello", "hey"]:
        ai_response = "Hello! 👋 Great to have you here. What would you like to know about Sandhar's energy tracking metrics?"
    elif "inefficiency" in clean_prompt or "lost" in clean_prompt:
        ai_response = f"⚠️ **Inefficiency Alert Audit:** Across our entire operational architecture, our plants registered a combined system optimization loss totaling **{df_master['unit_lost_inefficiency'].sum():,} units** due to configuration drops."
    elif "grid" in clean_prompt:
        ai_response = f"⚡ **Sandhar Energy Audit:** Combined grid utility usage amounts to **{df_master['grid_mvah'].sum():,.2f} MVAh** across all active manufacturing installations."
    elif "capex" in clean_prompt or "opex" in clean_prompt:
        ai_response = f"💰 **Solar Infrastructure Metrics:** Collective CAPEX solar arrays generate **{df_master['capex_gen'].sum():,.2f} MWh**, while active OPEX layouts yield **{df_master['opex_gen'].sum():,.2f} MWh**."
    else:
        located = False
        for _, r in df_master.iterrows():
            short_code = r['unit'].split()
            if short_code.lower() in clean_prompt:
                ai_response = f"🔍 **Ecosystem Record [{r['unit']}]:** Grid: {r['grid_mvah']} MVAh | Efficiency: {r['generation_per_kwp']} Gen/KWP | Inefficiency Loss: {r['unit_lost_inefficiency']:,} Units."
                located = True
                break
        if not located:
            ai_response = "I couldn't quite parse that filter context. Try asking about 'inefficiency losses', 'yearly grid usage', or drop a direct identifier token like 'SAD'."

    ai_response += " \n\n*Please let me know what else you want to know!*"
            
    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
    chat_box.chat_message("assistant").write(ai_response)
