import streamlit as st
import pandas as pd
import io
import plotly.express as px
import folium
from streamlit_folium import st_folium

# 🟢 Import variables and logic from our custom modules
from data_store import MASTER_CSV_DATA, MONTHLY_CSV_DATA, FY27_CSV_DATA
from excel_engine import generate_excel_report

# Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Ecosystem Dashboard",
    page_icon="🌱",
    layout="wide"
)

# --- INITIAL STATE MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Telemetry interface fully online. Ask me about your worst-performing locations, total carbon emissions, or request a complete summary."}
    ]

# 🎨 CSS Overlays
if not st.session_state["authenticated"]:
    st.markdown("""
        <style>
        .stApp { background: #030712 !important; overflow: hidden; }
        div[data-testid="stVerticalBlock"] > div:has(.auth-card-wrap) {
            background: rgba(8, 14, 32, 0.65) !important;
            backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px;
            padding: 40px !important; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7);
            z-index: 10; position: relative; margin-top: 10px;
        }
        .portal-banner h2 { color: #00ffcc !important; font-weight: 800 !important; text-shadow: 0 0 15px rgba(0, 255, 204, 0.3); }
        .portal-banner p { color: #94a3b8 !important; }
        label { color: #cbd5e1 !important; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        @keyframes smoothScaleUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
        .stExpander { animation: smoothScaleUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both; }
        </style>
        """, unsafe_allow_html=True)

# Portal Security Wall
if not st.session_state["authenticated"]:
    _, col_center, _ = st.columns([1, 1.3, 1])
    with col_center:
        st.markdown('<div class="auth-card-wrap"></div>', unsafe_allow_html=True)
        st.markdown('<div class="portal-banner" style="text-align: center; margin-bottom:20px;"><h2>🌱 Sandhar Energy Portal</h2><p>Ecosystem Identity Verification Matrix</p></div>', unsafe_allow_html=True)
        username = st.text_input("Matrix Operator Key", placeholder="Username ID")
        password = st.text_input("Access Authorization Token", type="password", placeholder="••••••••")
        if st.button("Initialize Energy Workspace", type="primary", use_container_width=True):
            if username == "sandhar" and password == "telemetry2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("System access codes rejected.")
    st.stop()

# Load Datasets via Cached Handlers
@st.cache_data
def load_energy_data_matrices():
    df_m = pd.read_csv(io.StringIO(MASTER_CSV_DATA.strip()))
    df_t = pd.read_csv(io.StringIO(MONTHLY_CSV_DATA.strip()))
    return df_m, df_t

df_master, df_monthly = load_energy_data_matrices()
df_fy27 = pd.read_csv(io.StringIO(FY27_CSV_DATA.strip()))

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("🔒 **Telemetry Link Stable**")
if st.sidebar.button("Log Out Context"):
    st.session_state["authenticated"] = False
    st.rerun()

st.sidebar.header("🗺️ Application Pages")
app_page = st.sidebar.radio("Navigate Workspace", ["Main Tracking Panel", "FY26-27 Analytics & Horizon Panel"])


# ================= PAGE 2: NEW ANALYTICS PANEL =================
if app_page == "FY26-27 Analytics & Horizon Panel":
    st.title("🚀 FY26-27 Next Horizon Engine")
    st.caption("Active forecasting layers and validation horizons parsed from incoming live execution spreadsheets.")
    st.markdown("---")
    
    st.subheader("📋 Infrastructure Node Matrix Evaluation Ledger (FY26-27 Data Metrics)")
    for idx, row in df_master.iterrows():
        unit_code = str(row['unit']).strip()
        apr_series = df_fy27.loc[df_fy27['Month'] == "April'26", unit_code].values
        may_series = df_fy27.loc[df_fy27['Month'] == "May'26", unit_code].values
        
        apr_val = apr_series if len(apr_series) > 0 else 0
        may_val = may_series if len(may_series) > 0 else 0
        
        with st.expander(f"🏢 Node Layer [{unit_code}] — Horizon Status Analysis"):
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("April'26 Yield Log", f"{int(apr_val):,} kWh")
            col_b.metric("May'26 Yield Log", f"{int(may_val):,} kWh")
            
            y_ratio27 = float(row['gen_kwp_27'])
            if y_ratio27 > 3.0:
                col_c.markdown(f"**Generation per KWP (FY26-27)**<br><span style='color:#10b981; font-size:24px; font-weight:bold;'>🟢 {y_ratio27} Yield</span>", unsafe_allow_html=True)
            else:
                col_c.markdown(f"**Generation per KWP (FY26-27)**<br><span style='color:#ef4444; font-size:24px; font-weight:bold;'>🔴 {y_ratio27} Yield</span>", unsafe_allow_html=True)

# ================= PAGE 1: MAIN TRACKING PANEL =================
elif app_page == "Main Tracking Panel":
    st.sidebar.header("🕹️ Selection Filters")
    selected_vertical = st.sidebar.selectbox("Business Segment", ["All Segments"] + list(df_master['vertical'].unique()), key="main_vert")
    df_filtered = df_master.copy() if selected_vertical == "All Segments" else df_master[df_master['vertical'] == selected_vertical].copy()

    target_month = st.sidebar.select_slider("Select Target Tracking Month (FY25-26)", options=list(df_monthly['Month']))

    # Metrics Summary Grid
    total_grid = df_filtered['grid_mvah'].sum()
    total_mit = df_filtered['mitigation'].sum()
    total_emi = df_filtered['emission'].sum()

    st.markdown("### 📊 Metrics Summary Grid")
    col_metric_1, col_metric_2, col_metric_3 = st.columns(3)
    col_metric_1.metric("⚡ Total Grid Sourced", f"{total_grid:,.1f} MVAh")
    col_metric_2.metric("🌱 Carbon Offset", f"{int(total_mit):,} MT CO₂")
    col_metric_3.metric("🏭 Gross Footprint", f"{int(total_emi):,} MT CO₂")

    # Excel Download Trigger (Imported logic)
    excel_data = generate_excel_report(df_filtered)
    st.download_button(
        label="📥 Download Formatted Ecosystem Executive Report (.xlsx)",
        data=excel_data,
        file_name=f"Sandhar_Energy_Report_{target_month}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.markdown("---")

    # Charts Visualizations
    st.subheader("📊 Dynamic Environmental Performance & Fleet Generation Metrics")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig_bar = px.bar(
            df_filtered, x='unit', y=['mitigation', 'emission'], barmode='group',
            title="Carbon Offset (Mitigation) vs Gross Footprint by Operational Node",
            labels={'value': 'Metric Tons (CO₂)', 'unit': 'Plant Node Code'},
            color_discrete_sequence=['#10b981', '#ef4444']
        )
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend_title_text='Metrics')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        fig_scatter = px.scatter(
            df_filtered, x='grid_mvah', y='generation_per_kwp', size='unit_lost_inefficiency',
            color='vertical', hover_name='unit', title='Generation Ratio vs Grid Sourcing (Bubble size = Inefficiency Losses)',
            labels={'grid_mvah': 'Grid Sourced (MVAh)', 'generation_per_kwp': 'Gen/KWP Ratio'}
        )
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Folium Interactive Geolocation Map
    st.subheader("🗺️ Enterprise Infrastructure Geolocation Node Overlay")
    if not df_filtered.empty:
        avg_lat, avg_lon = df_filtered['lat'].mean(), df_filtered['lon'].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5, tiles="CartoDB positron")
        
        for _, marker_row in df_filtered.iterrows():
            popup_html = f"<div><strong>Node:</strong> {marker_row['unit']}<br><strong>Location:</strong> {marker_row['location']}<br><strong>Segment:</strong> {marker_row['vertical']}<br><strong>Green Shift:</strong> {marker_row['replacement_pct']}%<br><strong>Gen Ratio:</strong> {marker_row['generation_per_kwp']}</div>"
            icon_color = "green" if float(marker_row['generation_per_kwp']) > 3.0 else "red"
            folium.Marker(
                location=[marker_row['lat'], marker_row['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"Node Layer [{marker_row['unit']}]",
                icon=folium.Icon(color=icon_color, icon="bolt", prefix="fa")
            ).add_to(m)
        st_folium(m, height=480, width=None, use_container_width=True, key="sandhar_live_map")
    else:
        st.info("No geospatial node arrays found matching filtered layers.")

    st.markdown("---")

    # Chat Assistant Console
    st.subheader("🤖 Interactive Live Data Chat Assistant")
    st.caption("Type analytical questions about your plants (e.g., 'worst plant', 'total emissions', 'highest efficiency', or 'summary') inside the console field below.")

    def evaluate_live_query(user_query, target_data):
        raw = user_query.strip().lower()
        if "worst" in raw or "inefficient" in raw or "lost" in raw:
            worst_row = target_data.loc[target_data['unit_lost_inefficiency'].idxmax()]
            return f"🚨 **Anomaly Alert:** Node **{worst_row['unit']}** ({worst_row['location']}) has the highest systematic line leakage with **{int(worst_row['unit_lost_inefficiency']):,} units** lost to engineering inefficiencies."
        elif "highest" in raw or "best" in raw or "efficient" in raw:
            best_row = target_data.loc[target_data['generation_per_kwp'].idxmax()]
            return f"🏆 **Efficiency Peak:** Node **{best_row['unit']}** has secured the highest performance threshold with a Generation/KWP ratio of **{best_row['generation_per_kwp']}**."
        elif "emission" in raw or "carbon" in raw or "footprint" in raw:
            return f"🍃 **Carbon Registry:** Total footprint is **{int(target_data['emission'].sum()):,} MT CO₂**, balanced by a mitigation offset of **{int(target_data['mitigation'].sum()):,} MT CO₂**."
        elif "summary" in raw or "overview" in raw or "stats" in raw:
            return f"📋 **Quick Status Briefing:** Evaluating **{len(target_data)} plant profiles**. Total grid demand sums to **{target_data['grid_mvah'].sum():,.2f} MVAh**."
        else:
            return "🤖 Ask about: **'worst plant'**, **'highest efficiency'**, **'total emissions'**, or a **'summary'**."

    chat_box = st.container(height=260)
    with chat_box:
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]): st.markdown(message["content"])

    with st.form(key="telemetry_chat_form", clear_on_submit=True):
        user_text = st.text_input("Query Entry Input Field:", placeholder="Type your metric query here...")
        submitted = st.form_submit_button("Ask Node Engine", use_container_width=True)

    if submitted and user_text:
        st.session_state["chat_history"].append({"role": "user", "content": user_text})
        st.session_state["chat_history"].append({"role": "assistant", "content": evaluate_live_query(user_text, df_filtered)})
        st.rerun()

    st.markdown("---")

    # Infrastructure Ledger Expanders
    st.subheader("📋 Infrastructure Node Register Ledger Details")
    for idx, row in df_filtered.iterrows():
        unit_string = str(row['unit']).strip()
        current_mon_val = 0
        if unit_string in df_monthly.columns:
            matching_rows = df_monthly.loc[df_monthly['Month'] == target_month, unit_string].values
            if len(matching_rows) > 0 and pd.notna(matching_rows):
                try: current_mon_val = float(str(matching_rows).replace(',', ''))
                except: current_mon_val = 0
                
        card_title = f"📦 [{row['unit']}] Location: {row['location']} — Selected Month ({target_month}): {int(current_mon_val):,} Generation Units"
        
        with st.expander(card_title):
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            col_f1.metric("Yearly Grid Sourcing", f"{row['grid_mvah']:,.2f} MVAh")
            col_f2.metric("Green Shift Percentage", f"{row['replacement_pct']}%")
            col_f3.metric("Diesel (DG) Sideload", f"{int(row['dg']):,} Liters")
            
            yield_ratio = float(row['generation_per_kwp'])
            if yield_ratio > 3.0:
                col_f4.markdown(f"**Generation per KWP Ratio**<br><span style='color:#10b981; font-size:24px; font-weight:bold;'>🟢 {yield_ratio} Yield</span>", unsafe_allow_html=True)
            else:
                col_f4.markdown(f"**Generation per KWP Ratio**<br><span style='color:#ef4444; font-size:24px; font-weight:bold;'>🔴 {yield_ratio} Yield</span>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            col_s1.metric("CAPEX / OPEX Capacities", f"{int(row['capex_capacity'])} / {int(row['opex_capacity'])} kWp")
            col_s2.metric("CAPEX Solar Generation", f"{row['capex_gen']:,.2f} MWh")
            col_s3.metric("OPEX Solar Generation", f"{row['opex_gen']:,.2f} MWh")
            col_s4.metric("Lost Due to Inefficiency", f"{int(row['unit_lost_inefficiency']):,} Units", delta=f"-{int(row['unit_lost_inefficiency'])} Units", delta_color="inverse")
