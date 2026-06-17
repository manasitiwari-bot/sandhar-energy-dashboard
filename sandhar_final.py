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

# 🎨 HIGH-PERFORMANCE CUSTOM LAYER (Shapes, Themes & Animations)
st.markdown("""
    <style>
    /* Global Fade-In Entry Animation */
    @keyframes smoothScaleUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    div[data-testid="stMetric"], .stExpander, .stPlotlyChart {
        animation: smoothScaleUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    /* Container Alignment for Visual Buttons */
    .shape-row {
        display: flex;
        justify-content: center;
        gap: 50px;
        margin: 20px 0;
    }

    /* 💧 CSS DROPLET SHAPE BUTTON */
    .droplet-node {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #38bdf8, #0284c7);
        border-radius: 0% 100% 100% 100%;
        transform: rotate(45deg);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .droplet-node:hover {
        transform: rotate(45deg) scale(1.08);
        box-shadow: 0 12px 24px rgba(2, 132, 199, 0.45);
    }
    .droplet-inner-text {
        transform: rotate(-45deg);
        color: white;
        font-weight: bold;
        font-size: 13px;
        text-align: center;
    }

    /* 🌱 CSS LEAF SHAPE BUTTON */
    .leaf-node {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #4ade80, #16a34a);
        border-radius: 100% 0% 100% 0%;
        box-shadow: 0 8px 20px rgba(22, 163, 74, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        cursor: pointer;
        border: none;
    }
    .leaf-node:hover {
        transform: scale(1.08) rotate(5deg);
        box-shadow: 0 12px 24px rgba(22, 163, 74, 0.45);
    }
    .leaf-inner-text {
        color: white;
        font-weight: bold;
        font-size: 13px;
        text-align: center;
    }
    
    /* Interactive Highlight Borders */
    div[data-testid="stMetric"], .stExpander {
        border-radius: 14px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(16, 185, 129, 0.12) !important;
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

# 2. Portal Security Wall (FIXED & RESTORED)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    _, col_center, _ = st.columns([1, 1.4, 1])
    
    with col_center:
        st.markdown('<div class="portal-banner"><h2>🌱 Sandhar Eco Portal</h2><p>Identity Verification Terminal</p></div>', unsafe_allow_html=True)
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

# --- INSTANT SCRIPTING CACHE INITIALIZER ---
if "matrix_chart_target" not in st.session_state:
    st.session_state["matrix_chart_target"] = "emission"

# --- SIDEBAR INTERFACE ---
st.sidebar.markdown("🔒 **Telemetry Link Connected**")
if st.sidebar.button("Log Out"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🕹️ Workspace Filters")
selected_vertical = st.sidebar.selectbox("Business Verticals", ["All Segments"] + list(df_master['vertical'].unique()))
df_filtered = df_master.copy() if selected_vertical == "All Segments" else df_master[df_master['vertical'] == selected_vertical].copy()

# --- MAIN DASHBOARD FRAME ---
st.title("🌱 Sandhar Energy Ecosystem Matrix Workspace")
st.caption("Complete operational intelligence layout featuring live shape-toggled metrics, spatial maps, and structural ledger logs.")
st.markdown("---")

# 📊 1. THE KPI CARDS BLOCK
m1, m2, m3 = st.columns(3)
m1.metric("⚡ Combined Grid Drawdown", f"{df_filtered['grid_mvah'].sum():,.2f} MVAh")
m2.metric("🌱 Mitigated Carbon Slices", f"{int(df_filtered['mitigation'].sum()):,} MT CO₂")
m3.metric("🛢️ Grid Footprint Emissions", f"{int(df_filtered['emission'].sum()):,} MT CO₂")

st.markdown("<br>", unsafe_allow_html=True)

# 💧 & 🌱 2. INTERACTIVE VISUAL TUNER SHAPES
st.subheader("🎨 Matrix Tuning Nodes (Click Shapes to Toggle Main Graph)")
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

# Custom Javascript Injector to convert standard buttons into custom Droplet/Leaf styling
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

# --- 3. DYNAMIC BAR GRAPH VIEW ---
if st.session_state["matrix_chart_target"] == "emission":
    fig_primary = px.bar(
        df_filtered, x="unit", y="emission", color="vertical",
        title="🏭 Active Gross Emissions Stack (MT CO₂)", color_discrete_sequence=px.colors.sequential.Blues_r
    )
else:
    fig_primary = px.bar(
        df_filtered, x="unit", y="mitigation", color="vertical",
        title="🍏 Active Offsets & Mitigation Profile (MT CO₂)", color_discrete_sequence=px.colors.sequential.Greens_r
    )
fig_primary.update_layout(height=360, margin=dict(t=30, b=10, l=10, r=10))
st.plotly_chart(fig_primary, use_container_width=True)

st.markdown("---")

# --- 4. THE MAP SECTION ---
st.subheader("🗺️ Telemetry Geospatial Node Allocation Map")
fig_global_map = px.scatter_mapbox(
    df_filtered, lat="lat", lon="lon",
    size="total_energy_footprint", color="vertical",
    hover_name="unit", hover_data=["location", "grid_mvah", "emission"],
    zoom=4.0, height=450, color_discrete_sequence=px.colors.qualitative.Prism
)
fig_global_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_global_map, use_container_width=True)

st.markdown("---")

# --- 5. THE DATA EXPANDERS (CAPEX, OPEX, GRID DRAWDOWN DETAILS) ---
st.subheader("📋 Infrastructure Node Register & Financial Ledger")
st.caption("Expand any node block below to pull complete engineering parameters, financial distributions, and carbon mitigation scales.")

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

# --- 6. INLINE AI AGENT WINDOW ---
st.subheader("🤖 Systems Telemetry Chatbot Link")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role": "assistant", "content": "Ecosystem data sync complete. Audit requests active."}]

chat_box = st.container(height=240)
for message in st.session_state["chat_history"]:
    chat_box.chat_message(message["role"]).write(message["content"])

if prompt_str := st.chat_input("Enter evaluation criteria query..."):
    st.session_state["chat_history"].append({"role": "user", "content": prompt_str})
    chat_box.chat_message("user").write(prompt_str)
    
    clean_prompt = prompt_str.lower().strip()
    ai_response = ""
    
    if "grid" in clean_prompt or "drawdown" in clean_prompt:
        ai_response = f"⚡ **Grid Power Audit:** Combined grid utility usage amounts to **{df_master['grid_mvah'].sum():,.2f} MVAh** across all manufacturing sectors."
    elif "capex" in clean_prompt or "opex" in clean_prompt:
        ai_response = f"💰 **Solar Allocation Summary:** Combined CAPEX capacity setup metrics stand at **{int(df_master['capex_capacity'].sum()):,} kWp**, while active OPEX frameworks track at **{int(df_master['opex_capacity'].sum()):,} kWp**."
    else:
        located = False
        for _, r in df_master.iterrows():
            if r['unit'].lower() in clean_prompt:
                ai_response = f"🔍 **Record Matrix [{r['unit']}]:** Grid: {r['grid_mvah']} MVAh | CAPEX Solar Gen: {r['capex_gen']} MWh | OPEX Solar Gen: {r['opex_gen']} MWh."
                located = True
                break
        if not located:
            ai_response = "Telemetry context unparsed. Try querying 'yearly grid usage', 'capex capacity values', or enter a localized asset token code like 'SAD'."
            
    st.session_state["chat_history"].append({"role": "assistant", "content": ai_response})
    chat_box.chat_message("assistant").write(ai_response)
