import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# Visual Layout Theme Engine
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    h1 { font-weight: 900 !important; color: #0f172a !important; font-size: 2.2rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.4rem !important; font-weight: 700 !important; color: #1e293b !important; margin-top: 1rem !important; }
    div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800 !important; font-size: 1.3rem !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.8rem !important; font-weight: 600 !important; color: #475569 !important; }
    .stMetric { background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 0.5rem 0.75rem; border-radius: 0.375rem; }
    .stExpander { border: 1px solid #cbd5e1 !important; border-radius: 0.5rem !important; background-color: #ffffff !important; margin-bottom: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Portal Security Wall (Allows secure access from ANY computer)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #0f172a;'>🔐 Sandhar Portal Login</h2>", unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="e.g., sandhar")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    if st.button("Sign In", type="primary"):
        if username == "sandhar" and password == "telemetry2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.stop()

# 3. Secure Master Data Matrix (CSV Stream Block)
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
st.sidebar.markdown("**Active Environment:** Secure Corporate Portal")
if st.sidebar.button("Exit Dashboard Context", type="secondary"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Filter Options")
selected_vertical = st.sidebar.selectbox("Business Vertical Slices", ["All Business Verticals"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Business Verticals" else df_master[df_master['vertical'] == selected_vertical].copy()

page_routing = st.sidebar.radio("🧭 Navigate Workspace", ["📊 Performance Dashboard", "🗺️ Interactive Map View"])

# --- 🤖 INTEGRATED SIDEBAR DATA CHATBOT ---
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Sandhar Telemetry AI")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Ask me anything about Sandhar's energy footprint!"}]

# Chat display box
chat_container = st.sidebar.container(height=240)
for msg in st.session_state["chat_history"]:
    chat_container.chat_message(msg["role"]).write(msg["content"])

# User query logic processing the internal dataframe
if user_query := st.sidebar.chat_input("Ask about units, emissions..."):
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    chat_container.chat_message("user").write(user_query)
    
    query_lower = user_query.lower()
    response = ""
    
    if "total emission" in query_lower or "emissions" in query_lower:
        total_emit = int(df_master['emission'].sum())
        response = f"The total carbon emissions across all operational facilities is {total_emit:,} MT."
    elif "highest grid" in query_lower or "max grid" in query_lower:
        max_row = df_master.loc[df_master['grid_mvah'].idxmax()]
        response = f"Unit {max_row['unit']} located in {max_row['location']} has the highest grid sourcing at {max_row['grid_mvah']:,.2f} MVAh."
    elif "total mitigation" in query_lower or "carbon saved" in query_lower or "mitigation" in query_lower:
        total_mit = int(df_master['mitigation'].sum())
        response = f"Sandhar has successfully mitigated {total_mit:,} MT of carbon footprint via active green infrastructure."
    elif "highest emission" in query_lower or "worst unit" in query_lower:
        max_emit = df_master.loc[df_master['emission'].idxmax()]
        response = f"Unit {max_emit['unit']} ({max_emit['vertical']}) has the highest emission footprint at {max_emit['emission']:,} MT."
    elif "list units" in query_lower or "how many units" in query_lower:
        response = f"There are currently {len(df_master)} active physical nodes tracking energy ledger telemetries."
    else:
        # Clean and normalize the query to match units safely
        matched_unit = None
        u_data = None
        
        # Look through the actual dataframe rows directly
        for idx, row in df_master.iterrows():
            if row['unit'].lower() in query_lower:
                matched_unit = row['unit']
                u_data = row.to_dict()  # Convert the matched row directly to a clean dictionary
                break
        
        # Fallback check to match fragments (e.g. typing "SAD" matches "SAD & SPB")
        if not matched_unit:
            for idx, row in df_master.iterrows():
                if any(part.strip().lower() in query_lower for part in row['unit'].split('&')):
                    matched_unit = row['unit']
                    u_data = row.to_dict()
                    break

        # FIXED: Generates response using safe dictionary structure populated right from the loops
        if matched_unit and u_data:
            response = f"**Asset Ledger [{matched_unit}]:** Located in {u_data['location']}. Grid Drawdown: {u_data['grid_mvah']:,.2f} MVAh, Mitigated Carbon: {u_data['mitigation']} MT, Total Emission Footprint: {u_data['emission']} MT."
        else:
            response = "I can compute total metrics instantly! Try asking: 'What is the total emission?', 'Which unit has the highest grid sourcing?', or search a specific unit like 'Tell me about ACM'."

    st.session_state["chat_history"].append({"role": "assistant", "content": response})
    chat_container.chat_message("assistant").write(response)


# --- WORKSPACE PAGE 1: DASHBOARD PERFORMANCE ---
if page_routing == "📊 Performance Dashboard":
    st.title("📊 Sandhar Energy Analytics Matrix")
    st.caption("Live asset summary across active industrial infrastructure nodes.")
    st.markdown("---")
    
    # KPIs Layout
    m1, m2, m3 = st.columns(3)
    m1.metric("⚡ Total Grid Sourcing", f"{df_filtered['grid_mvah'].sum():,.3f} MVAh")
    m2.metric("🌱 Total Mitigated Carbon", f"{int(df_filtered['mitigation'].sum()):,} MT")
    m3.metric("🛢️ Total Footprint Emissions", f"{int(df_filtered['emission'].sum()):,} MT")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grouped Graph Engine
    st.subheader("📈 Energy Metrics Comparison Matrix")
    df_chart_melted = df_filtered.melt(
        id_vars=["unit"], 
        value_vars=["grid_mvah", "capex_gen", "opex_gen"],
        var_name="Energy Utility Type", value_name="Energy Metrics"
    )
    
    df_chart_melted["Energy Utility Type"] = df_chart_melted["Energy Utility Type"].replace({
        "grid_mvah": "<b>Yearly Grid Sourcing (MVAh)</b>",
        "capex_gen": "<b>CAPEX Solar Generation (MWh)</b>",
        "opex_gen": "<b>OPEX Solar Generation (MWh)</b>"
    })
    
    color_map = {
        "<b>Yearly Grid Sourcing (MVAh)</b>": "#4472C4",
        "<b>CAPEX Solar Generation (MWh)</b>": "#f59e0b",
        "<b>OPEX Solar Generation (MWh)</b>": "#10b981"
    }
    
    fig_master = px.bar(
        df_chart_melted, x="unit", y="Energy Metrics", color="Energy Utility Type",
        barmode="group", color_discrete_map=color_map, text_auto=".1f"
    )
    
    fig_master.update_layout(
        plot_bgcolor="#ffffff", paper_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=25, b=10), height=480,
        font=dict(color="#000000", size=14),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1,
            title=dict(font=dict(size=15, color="#000000")),
            font=dict(size=14, color="#000000")
        ),
        xaxis=dict(
            tickfont=dict(size=14, color="#000000"),
            title=dict(text="<b>Plant Operational Unit</b>", font=dict(size=15, color="#000000")),
            gridcolor="#f1f5f9"
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="#000000"),
            title=dict(text="<b>Energy Metrics</b>", font=dict(size=15, color="#000000")),
            gridcolor="#f1f5f9"
        )
    )
    
    fig_master.update_traces(textposition="outside", textfont=dict(color="#000000", size=11))
    st.plotly_chart(fig_master, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Expandable Plant Level Ledger Cards 
    st.subheader("📋 Plant Level Assets Operational Ledger")
    for idx, row in df_filtered.iterrows():
        card_title = f"📦 [{row['unit']}] Location: {row['location']} — Verified Grid: {row['grid_mvah']:,.3f} MVAh"
        with st.expander(card_title):
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("⚡ Yearly Grid Drawdown", f"{row['grid_mvah']:,.3f} MVAh")
            r2.metric("🟢 Replacement Ratio", f"{row['replacement_pct']}%")
            r3.metric("⛽ DG Sourced Diesel", f"{int(row['dg']):,} lt")
            r4.metric("☀️ CAPEX Capacity", f"{int(row['capex_capacity']):,} kWp")
            
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            
            w1, w2, w3, w4 = st.columns(4)
            w1.metric("🏢 OPEX Capacity", f"{int(row['opex_capacity']):,} kWp")
            w2.metric("🌅 CAPEX Solar Generation", f"{row['capex_gen']:,.3f} MWh")
            w3.metric("🌿 OPEX Solar Generation", f"{row['opex_gen']:,.3f} MWh")
            w4.metric("🌱 Mitigated vs Emitted Carbon", f"{int(row['mitigation'])} / {int(row['emission'])} MT")

# --- WORKSPACE PAGE 2: MAP ASSET VIEW ---
else:
    st.title("🗺️ Asset Power Infrastructure Map")
    st.caption("Visualizing node size scaled dynamically against total energy metrics.")
    st.markdown("---")
    
    fig_map = px.scatter_mapbox(
        df_filtered, lat="lat", lon="lon",
        size="total_energy_footprint", color="vertical",
        hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
        zoom=4.2, height=650, color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_map.update_layout(
        mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📑 Global Audit Ledger Overview")
    st.dataframe(df_filtered.drop(columns=["lat", "lon", "total_energy_footprint"]), use_container_width=True, hide_index=True)
