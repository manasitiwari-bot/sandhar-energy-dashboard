import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Green Energy Matrix",
    page_icon="🌱",
    layout="wide"
)

# 🎨 EXTREME GREEN ENERGY VISUAL ENGINE (Custom CSS & Canvas Animations)
st.markdown("""
    <style>
    /* Premium Tech Dark/Green Theme Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #041d13 0%, #020b07 100%);
        color: #e2f1ea !important;
    }
    
    /* Global Text Styling to match theme */
    h1, h2, h3, p, span, label, div {
        color: #e2f1ea !important;
    }

    /* Ambient Floating Particles Background Animation */
    @keyframes floatParticles {
        0% { background-position: 0px 0px, 0px 0px; }
        100% { background-position: 500px 1000px, 400px 400px; }
    }
    body {
        background-image: 
            radial-gradient(rgba(16, 185, 129, 0.1) 1px, transparent 0),
            radial-gradient(rgba(16, 185, 129, 0.05) 2px, transparent 0);
        background-size: 40px 40px, 60px 60px;
        animation: floatParticles 80s linear infinite;
    }

    /* Live Pulsing Indicator for Title */
    @keyframes neonGlow {
        0% { transform: scale(0.95); box-shadow: 0 0 4px #10b981; opacity: 0.7; }
        50% { transform: scale(1.05); box-shadow: 0 0 20px #10b981; opacity: 1; }
        100% { transform: scale(0.95); box-shadow: 0 0 4px #10b981; opacity: 0.7; }
    }
    .live-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 12px;
        animation: neonGlow 2.5s infinite;
        vertical-align: middle;
    }

    /* Modern Glassmorphism Cards for Metrics & Data */
    div[data-testid="stMetric"], .stExpander {
        background: rgba(6, 37, 26, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        padding: 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    div[data-testid="stMetric"]:hover, .stExpander:hover {
        transform: translateY(-5px) scale(1.01);
        border-color: rgba(16, 185, 129, 0.6) !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2) !important;
    }

    /* Login Board Custom Frame */
    .login-box {
        background: rgba(4, 28, 19, 0.85);
        border: 2px solid #10b981;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.25);
        border-radius: 20px;
        padding: 40px;
        margin-top: 50px;
        position: relative;
        overflow: hidden;
    }

    /* CSS Green Energy Sketch: Moving Wind Turbine Blueprint */
    .turbine-container {
        width: 100%;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: flex-end;
        margin-bottom: 20px;
        position: relative;
    }
    .turbine-mast {
        width: 4px;
        height: 90px;
        background: linear-gradient(to top, rgba(16, 185, 129, 0), rgba(16, 185, 129, 0.8));
        position: absolute;
    }
    @keyframes spinBlades {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .turbine-blades {
        width: 80px;
        height: 80px;
        border: 2px dashed rgba(16, 185, 129, 0.6);
        border-radius: 50%;
        position: absolute;
        top: 0px;
        animation: spinBlades 6s linear infinite;
    }
    .turbine-blades::before, .turbine-blades::after {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        width: 100%; height: 2px;
        background: rgba(16, 185, 129, 0.8);
        transform: translate(-50%, -50%);
    }
    .turbine-blades::after {
        transform: translate(-50%, -50%) rotate(90deg);
    }
    
    /* Input adjustments for dark green mode */
    input {
        background-color: rgba(2, 15, 10, 0.8) !important;
        color: #e2f1ea !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Portal Security Wall
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    # Center the login panel visually
    _, col_center, _ = st.columns([1, 1.8, 1])
    
    with col_center:
        st.markdown("""
        <div class="login-box">
            <div class="turbine-container">
                <div class="turbine-mast"></div>
                <div class="turbine-blades"></div>
            </div>
            <h2 style='text-align: center; margin-top:0;'>🌱 Sandhar Green Matrix</h2>
            <p style='text-align: center; color: #a3ccc4 !important; font-size: 14px;'>Secure Telemetry Gateway</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Matrix Operator Identity", placeholder="Username")
        password = st.text_input("Access Verification Key", type="password", placeholder="Password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Matrix Session", type="primary", use_container_width=True):
            if username == "sandhar" and password == "telemetry2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Access codes failed verification authorization.")
    st.stop()

# 3. Secure Master Data Matrix
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

# --- SIDEBAR CONFIGURATIONS ---
st.sidebar.markdown("**⚡ Telemetry Node Active**")
if st.sidebar.button("Close Secure Session", type="secondary"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Filter Options")
selected_vertical = st.sidebar.selectbox("Business Vertical Slices", ["All Business Verticals"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Business Verticals" else df_master[df_master['vertical'] == selected_vertical].copy()

# Sustainability Simulator Slider
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Sustainability Goal Simulator")
emission_target = st.sidebar.slider("Target Max Emission Allowance per Unit (MT)", 50, 15000, 5000, step=100)

page_routing = st.sidebar.radio("🧭 Navigate Workspace", ["📊 Performance Dashboard", "🗺️ Interactive Map View"])

# --- 🤖 DATA CHATBOT ---
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Sandhar Telemetry AI")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Ready to scan. Ask me about Sandhar green metrics or type 'summary'."}]

chat_container = st.sidebar.container(height=180)
for msg in st.session_state["chat_history"]:
    chat_container.chat_message(msg["role"]).write(msg["content"])

if user_query := st.sidebar.chat_input("Query the matrix..."):
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    chat_container.chat_message("user").write(user_query)
    
    query_lower = user_query.lower().strip()
    response = ""
    
    if query_lower in ["hi", "hello", "hey"]:
        response = "System online. Ask for calculations like 'average emission', plant metrics like 'tell me about ACM', or type 'summary'!"
    elif "summary" in query_lower:
        total_plants = len(df_master)
        max_emit_row = df_master.loc[df_master['emission'].idxmax()]
        max_mit_row = df_master.loc[df_master['mitigation'].idxmax()]
        response = (
            f"📊 **Matrix Report:**\n\n"
            f"• Tracking {total_plants} operational facilities.\n"
            f"• **Top Green Node:** {max_mit_row['unit']} mitigated {max_mit_row['mitigation']:,} MT of CO₂.\n"
            f"• **Peak Emission Node:** {max_emit_row['unit']} carbon output at {max_emit_row['emission']:,} MT."
        )
    elif "average emission" in query_lower:
        response = f"Average node carbon emission footprint: **{df_master['emission'].mean():,.2f} MT**."
    elif "total solar" in query_lower or "generation" in query_lower:
        total_solar = df_master['capex_gen'].sum() + df_master['opex_gen'].sum()
        response = f"Aggregate green matrix production output: **{total_solar:,.2f} MWh**."
    else:
        matched_unit = None
        u_data = None
        for idx, row in df_master.iterrows():
            if row['unit'].lower() in query_lower:
                matched_unit = row['unit']
                u_data = row.to_dict()
                break
        if matched_unit and u_data:
            response = f"**Asset Vector [{matched_unit}]:** Grid Draw: {u_data['grid_mvah']:,.2f} MVAh, Mitigated CO₂: {u_data['mitigation']} MT, Total Emission: {u_data['emission']} MT."
        else:
            response = "Query unrecognized. Use syntax report names like 'ACM' or commands like 'summary'."

    st.session_state["chat_history"].append({"role": "assistant", "content": response})
    chat_container.chat_message("assistant").write(response)

# --- WORKSPACE PAGE 1: DASHBOARD PERFORMANCE ---
if page_routing == "📊 Performance Dashboard":
    st.markdown('<h1><span class="live-indicator"></span>Sandhar Green Energy Framework</h1>', unsafe_allow_html=True)
    st.caption("Cybernetic matrix processing clean generation arrays and asset carbon footprints.")
    st.markdown("---")
    
    # Glowing Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Combined Grid Drawdown", f"{df_filtered['grid_mvah'].sum():,.2f} MVAh")
    m2.metric("🟢 Mitigated Carbon Assets", f"{int(df_filtered['mitigation'].sum()):,} MT CO₂")
    m3.metric("🔥 Operational Emissions", f"{int(df_filtered['emission'].sum()):,} MT CO₂")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bar Matrix Graphic Upgrades (Neon Glow Layout Configuration)
    st.subheader("📈 High-Contrast Telemetry Chart")
    df_chart_melted = df_filtered.melt(
        id_vars=["unit"], 
        value_vars=["grid_mvah", "capex_gen", "opex_gen"],
        var_name="Utility", value_name="Metrics"
    )
    df_chart_melted["Utility"] = df_chart_melted["Utility"].replace({
        "grid_mvah": "Grid Sourcing (MVAh)",
        "capex_gen": "CAPEX Solar Array (MWh)",
        "opex_gen": "OPEX Solar Array (MWh)"
    })
    
    fig_master = px.bar(
        df_chart_melted, x="unit", y="Metrics", color="Utility",
        barmode="group", color_discrete_sequence=["#0ea5e9", "#f59e0b", "#10b981"]
    )
    fig_master.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2f1ea"),
        margin=dict(l=10, r=10, t=20, b=10), height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#e2f1ea")),
        xaxis=dict(gridcolor="rgba(16,185,129,0.1)", title=""),
        yaxis=dict(gridcolor="rgba(16,185,129,0.1)")
    )
    st.plotly_chart(fig_master, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Leaderboard Tabs
    st.subheader("🏆 Matrix Clean Asset Standings")
    top_mitigators = df_master.nlargest(3, 'mitigation')[['unit', 'mitigation']]
    over_emitters = df_master[df_master['emission'] > emission_target][['unit', 'emission']]
    
    tab1, tab2 = st.tabs(["🍃 Certified Green Nodes", "⚠️ Critical Emissions Limits"])
    
    with tab1:
        for _, row in top_mitigators.iterrows():
            st.write(f"🟢 **Node {row['unit']}** -> Successfully offset {int(row['mitigation'])} MT of carbon elements.")
            st.progress(min(int(row['mitigation']) / 8000, 1.0))
            
    with tab2:
        if over_emitters.empty:
            st.success("All facilities operating safely below target limits.")
        else:
            for _, row in over_emitters.iterrows():
                st.write(f"🚨 **Node {row['unit']}** -> Alert! Emission footprint reading {int(row['emission'])} MT.")
                st.progress(min(int(row['emission']) / 14000, 1.0))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Operational Cards
    st.subheader("📋 Plant Level Assets Operational Ledger")
    for idx, row in df_filtered.iterrows():
        status_icon = "⚡" if row['emission'] <= emission_target else "🔥"
        card_title = f"{status_icon} Node Matrix Reference ID: [{row['unit']}] — {row['location']}"
        
        with st.expander(card_title):
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Grid Drawing", f"{row['grid_mvah']:,.2f} MVAh")
            r2.metric("Green Replacement Ratio", f"{row['replacement_pct']}%")
            r3.metric("Diesel Vol Sourced", f"{int(row['dg']):,} L")
            r4.metric("CAPEX Frame Cap", f"{int(row['capex_capacity']):,} kWp")
            
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            
            w1, w2, w3, w4 = st.columns(4)
            w1.metric("OPEX Frame Cap", f"{int(row['opex_capacity']):,} kWp")
            w2.metric("CAPEX Solar Array Gen", f"{row['capex_gen']:,.2f} MWh")
            w3.metric("OPEX Solar Array Gen", f"{row['opex_gen']:,.2f} MWh")
            w4.metric("Mitigated / Output Carbon", f"{int(row['mitigation'])} / {int(row['emission'])} MT")

# --- WORKSPACE PAGE 2: MAP ASSET VIEW ---
else:
    st.markdown('<h1><span class="live-indicator"></span>Global Node Telemetry Grid Map</h1>', unsafe_allow_html=True)
    st.caption("Active geospatial arrays scaled dynamically against node generation values.")
    st.markdown("---")
    
    fig_map = px.scatter_mapbox(
        df_filtered, lat="lat", lon="lon",
        size="total_energy_footprint", color="vertical",
        hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
        zoom=4.2, height=600, color_discrete_sequence=px.colors.qualitative.G10
    )
    fig_map.update_layout(
        mapbox_style="carto-darkmatter", 
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01, font=dict(color="#e2f1ea"))
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📑 Global Audit Ledger Overview")
    st.dataframe(df_filtered.drop(columns=["lat", "lon", "total_energy_footprint"]), use_container_width=True, hide_index=True)
