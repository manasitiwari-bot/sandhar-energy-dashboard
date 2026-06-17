import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Green Matrix Workspace",
    page_icon="🌱",
    layout="wide"
)

# 🎨 THE HIGH-PERFORMANCE ANIMATION LAYER (Custom CSS)
st.markdown("""
    <style>
    /* 1. Global Page Component Entry Animation */
    @keyframes slideUpEntrance {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Apply entry animation cleanly to key framework layout zones */
    div[data-testid="stMetric"], .stExpander, .stPlotlyChart, div[data-testid="stChatMessage"] {
        animation: slideUpEntrance 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    /* Staggered delay for rows to create a smooth sequenced ripple load effect */
    div[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.1s; }
    div[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.2s; }
    div[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.3s; }

    /* 2. Interactive Magnetic Lift & Shadow Hover Responses */
    div[data-testid="stMetric"], .stExpander {
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s !important;
    }
    
    div[data-testid="stMetric"]:hover, .stExpander:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 24px rgba(16, 185, 129, 0.15) !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
    }

    /* 3. Live Glowing Heartbeat Indicator */
    @keyframes greenPulse {
        0% { transform: scale(0.92); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); opacity: 0.6; }
        70% { transform: scale(1.08); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); opacity: 1; }
        100% { transform: scale(0.92); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); opacity: 0.6; }
    }
    .live-indicator {
        display: inline-block;
        width: 14px;
        height: 14px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 12px;
        animation: greenPulse 2.2s ease-in-out infinite;
        vertical-align: middle;
    }
    
    /* Login Framework Structure */
    .portal-banner {
        text-align: center;
        border-bottom: 3px solid #10b981;
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
        st.markdown('<div class="portal-banner"><h2>🌱 Sandhar Green Portal</h2><p>Telemetry Identity Verification Terminal</p></div>', unsafe_allow_html=True)
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

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("🔒 **Telemetry Link Connected**")
if st.sidebar.button("Log Out Node Context"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Filter Options")
selected_vertical = st.sidebar.selectbox("Business Vertical Slices", ["All Business Verticals"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Business Verticals" else df_master[df_master['vertical'] == selected_vertical].copy()

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Safety Emissions Target")
emission_target = st.sidebar.slider("Tag Out Warning Limit (MT)", 50, 15000, 5000, step=100)

# --- MAIN INDUSTRIAL WORKSPACE ---
st.markdown('<h1><span class="live-indicator"></span>Sandhar Energy Animated Matrix</h1>', unsafe_allow_html=True)
st.caption("Responsive layout with interactive graphs, active geospatial map indexing, and an inline AI auditor.")
st.markdown("---")

# Core Aggregations
m1, m2, m3 = st.columns(3)
m1.metric("⚡ Combined Grid Drawdown", f"{df_filtered['grid_mvah'].sum():,.2f} MVAh")
m2.metric("🌱 Mitigated Carbon Slices", f"{int(df_filtered['mitigation'].sum()):,} MT CO₂")
m3.metric("🛢️ Grid Footprint Emissions", f"{int(df_filtered['emission'].sum()):,} MT CO₂")

st.markdown("<br>", unsafe_allow_html=True)

# 🌐 ROW 1: ANIMATED BAR GRAPH SIDE-BY-SIDE WITH AI CHATBOT
col_left_graph, col_right_ai = st.columns([1.6, 1])

with col_left_graph:
    st.subheader("📈 High-Contrast Asset Utility Performance")
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
        margin=dict(t=10, l=10, r=10, b=10), height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Operational Plant Units"),
        yaxis=dict(title="Metrics Output"),
        hovermode="x unified"
    )
    st.plotly_chart(fig_master, use_container_width=True)

with col_right_ai:
    st.subheader("🤖 Telemetry AI Assistant")
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [{"role": "assistant", "content": "Telemetry Node link active. Ask me about a specific facility like 'ACM' or type 'summary'."}]
    
    # Message board scroller window
    chat_window = st.container(height=300)
    for msg in st.session_state["chat_history"]:
        chat_window.chat_message(msg["role"]).write(msg["content"])
        
    if user_query := st.chat_input("Input command criteria..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        chat_window.chat_message("user").write(user_query)
        
        raw_input = user_query.lower().strip()
        reply = ""
        
        if any(greet in raw_input for greet in ["hi", "hello", "hey"]):
            reply = "Session verified. Query individual plant names (e.g. 'tell me about SAD'), request math, or type 'summary'."
        elif "summary" in raw_input:
            max_mit = df_master.loc[df_master['mitigation'].idxmax()]
            reply = f"📊 **Matrix Ledger Digest:** Tracking {len(df_master)} units. Top performing clean energy node is **{max_mit['unit']}** with {max_mit['mitigation']:,} MT carbon saved."
        elif "average emission" in raw_input:
            reply = f"The calculated footprint average stands at **{df_master['emission'].mean():,.2f} MT**."
        else:
            matched = None
            for _, row in df_master.iterrows():
                if row['unit'].lower() in raw_input:
                    matched = row.to_dict()
                    break
            if matched:
                reply = f"📌 **Asset Record [{matched['unit']}]:** Sourced Grid: {matched['grid_mvah']:,.2f} MVAh. Mitigated Balance: {matched['mitigation']} MT."
            else:
                reply = "Context string unparsed. Query facility acronym tokens (e.g. 'SAD') or type 'summary'."
                
        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        chat_window.chat_message("assistant").write(reply)

st.markdown("---")

# 🗺️ ROW 2: GEOSPATIAL MAP VIEW
st.subheader("🗺️ Geospatial Node Telemetry Infrastructure Map")
st.caption("Asset scale sizes bound dynamically to combined operational footprint equations.")

fig_map = px.scatter_mapbox(
    df_filtered, lat="lat", lon="lon",
    size="total_energy_footprint", color="vertical",
    hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
    zoom=4.2, height=500, color_discrete_sequence=px.colors.qualitative.Safe
)
fig_map.update_layout(
    mapbox_style="carto-positron", 
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01)
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 🏆 ROW 3: STANDINGS & LEDGER EXPANDERS
st.subheader("🏆 Carbon Asset Standings")
top_mitigators = df_master.nlargest(3, 'mitigation')[['unit', 'mitigation']]
over_emitters = df_master[df_master['emission'] > emission_target][['unit', 'emission']]

tab1, tab2 = st.tabs(["🍏 Top Carbon Mitigators", "🚨 Exceeding Target Warning"])
with tab1:
    for _, row in top_mitigators.iterrows():
        st.write(f"🍏 **Unit {row['unit']}**: Offset {int(row['mitigation'])} MT Carbon")
        st.progress(min(int(row['mitigation']) / 8000, 1.0))
with tab2:
    if over_emitters.empty:
        st.success("All operational units tracking safely below target thresholds.")
    else:
        for _, row in over_emitters.iterrows():
            st.write(f"🛑 **Unit {row['unit']}**: Emitting {int(row['emission'])} MT")
            st.progress(min(int(row['emission']) / 14000, 1.0))

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📋 Detailed Infrastructure Node Registers")
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
