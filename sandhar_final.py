import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Matrix",
    page_icon="🌱",
    layout="wide"
)

# 🎨 CLEAN PREMIUM VISUAL ENGINE (Respects system Light/Dark mode)
st.markdown("""
    <style>
    /* Live Pulsing Green Node Indicator */
    @keyframes greenPulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); opacity: 0.7; }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); opacity: 1; }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); opacity: 0.7; }
    }
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 10px;
        animation: greenPulse 2s infinite;
        vertical-align: middle;
    }
    
    /* Sleek Rounded Cards for Metrics & Containers */
    div[data-testid="stMetric"], .stExpander {
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.15) !important;
    }
    
    /* Login Canvas Formatting */
    .login-header {
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #10b981;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Portal Security Wall
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col_center, _ = st.columns([1, 1.5, 1])
    
    with col_center:
        st.markdown('<div class="login-header"><h2>🌱 Sandhar Secure Matrix</h2><p>Telemetry Verification Gateway</p></div>', unsafe_allow_html=True)
        username = st.text_input("Operator Username", placeholder="e.g., sandhar")
        password = st.text_input("Verification Password", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Authorize Core Session", type="primary", use_container_width=True):
            if username == "sandhar" and password == "telemetry2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Invalid corporate credentials.")
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

# --- SIDEBAR ROUTING ---
st.sidebar.markdown("🔒 **Session Secure**")
if st.sidebar.button("Log Out Context"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Filter Options")
selected_vertical = st.sidebar.selectbox("Business Vertical Slices", ["All Business Verticals"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Business Verticals" else df_master[df_master['vertical'] == selected_vertical].copy()

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Emissions Cap Target")
emission_target = st.sidebar.slider("Highlight Units Exceeding (MT)", 50, 15000, 5000, step=100)

page_routing = st.sidebar.radio("🧭 Workspace Navigation", ["📊 Performance Dashboard", "🗺️ Geospatial Map View"])

# --- WORKSPACE PAGE 1: DASHBOARD PERFORMANCE ---
if page_routing == "📊 Performance Dashboard":
    st.markdown('<h1><span class="live-indicator"></span>Sandhar Energy Architecture Matrix</h1>', unsafe_allow_html=True)
    st.caption("Interactive generation ledgers and carbon mitigation indexes.")
    st.markdown("---")
    
    # Standard KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Combined Grid Drawdown", f"{df_filtered['grid_mvah'].sum():,.2f} MVAh")
    m2.metric("🌱 Mitigated Carbon Slices", f"{int(df_filtered['mitigation'].sum()):,} MT CO₂")
    m3.metric("🛢️ Grid Footprint Emissions", f"{int(df_filtered['emission'].sum()):,} MT CO₂")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 🛹 INTERACTIVE STAIRCASE DRILL-DOWN GRAPH (Sunburst Matrix)
    st.subheader("🪜 Staircase Matrix Drilldown (Click Slices to Step Down/Up)")
    st.info("💡 **Interactive Tip:** Click an inner ring slice (Vertical) to scale up and drill down directly into its individual factory plants!")
    
    fig_staircase = px.sunburst(
        df_filtered,
        path=['vertical', 'unit'],
        values='total_energy_footprint',
        color='emission',
        color_continuous_scale='Viridis',
        labels={'total_energy_footprint': 'Total Footprint', 'emission': 'Emissions (MT)'}
    )
    fig_staircase.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_staircase, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Standings Leaderboard
    st.subheader("🏆 Carbon Asset Standings")
    top_mitigators = df_master.nlargest(3, 'mitigation')[['unit', 'mitigation']]
    over_emitters = df_master[df_master['emission'] > emission_target][['unit', 'emission']]
    
    tab1, tab2 = st.tabs(["🍏 Top Carbon Mitigators", "🚨 Exceeding Sideload Targets"])
    with tab1:
        for _, row in top_mitigators.iterrows():
            st.write(f"🍏 **{row['unit']}**: Offset {int(row['mitigation'])} MT Carbon")
            st.progress(min(int(row['mitigation']) / 8000, 1.0))
    with tab2:
        if over_emitters.empty:
            st.success("All elements running clean under specified bounds.")
        else:
            for _, row in over_emitters.iterrows():
                st.write(f"🛑 **{row['unit']}**: Emitting {int(row['emission'])} MT")
                st.progress(min(int(row['emission']) / 14000, 1.0))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Plant Cards Ledger
    st.subheader("📋 Infrastructure Node Register")
    for idx, row in df_filtered.iterrows():
        status_icon = "🛑" if row['emission'] > emission_target else "📦"
        card_title = f"{status_icon} [{row['unit']}] Location: {row['location']} — Sourced Grid: {row['grid_mvah']:,.2f} MVAh"
        
        with st.expander(card_title):
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Yearly Grid Drawdown", f"{row['grid_mvah']:,.2f} MVAh")
            r2.metric("Green Replacement Ratio", f"{row['replacement_pct']}%")
            r3.metric("Diesel Volume", f"{int(row['dg']):,} L")
            r4.metric("CAPEX Frame Capacity", f"{int(row['capex_capacity']):,} kWp")
            
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            w1, w2, w3, w4 = st.columns(4)
            w1.metric("OPEX Frame Capacity", f"{int(row['opex_capacity']):,} kWp")
            w2.metric("CAPEX Generation", f"{row['capex_gen']:,.2f} MWh")
            w3.metric("OPEX Generation", f"{row['opex_gen']:,.2f} MWh")
            w4.metric("Mitigation / Emission Balance", f"{int(row['mitigation'])} / {int(row['emission'])} MT")

# --- WORKSPACE PAGE 2: MAP ASSET VIEW ---
else:
    st.markdown('<h1><span class="live-indicator"></span>Geospatial Node Telemetry Map</h1>', unsafe_allow_html=True)
    st.caption("Interactive geographic layout mapping facility scales.")
    st.markdown("---")
    
    fig_map = px.scatter_mapbox(
        df_filtered, lat="lat", lon="lon",
        size="total_energy_footprint", color="vertical",
        hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
        zoom=4.2, height=600, color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_map.update_layout(
        mapbox_style="carto-positron", 
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df_filtered.drop(columns=["lat", "lon", "total_energy_footprint"]), use_container_width=True, hide_index=True)
