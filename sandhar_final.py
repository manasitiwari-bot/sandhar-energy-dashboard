import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Dashboard",
    page_icon="🌱",
    layout="wide"
)

# --- LIVE HARDCODED DATASET (From uploaded images) ---
@st.cache_data
def load_comprehensive_plant_matrices():
    # Structural arrays built cleanly to eliminate dictionary syntax bugs
    unit_names = ["SAG", "SCD", "SEB", "SAD", "SCR", "STPL", "ACM", "CORP", "SASPL", "SHP", "SAH", "SCH", "SIO", "SCA", "SAB", "SCY", "SIP", "SIA", "SKC", "SHN"]
    
    verticals = [
        "Automotive Business", "Plastic Business", "Sheet Metal & Allied Business", "Automotive Business",
        "Casting Machining & Tooling Business", "Casting Machining & Tooling Business", "Casting Machining & Tooling Business",
        "Corp. Office", "Corp. Office", "Automotive Business", "Automotive Business", "Casting Machining & Tooling Business",
        "Automotive Business", "Casting Machining & Tooling Business", "Automotive Business", "Sheet Metal & Allied Business",
        "Cabin & Fabrication Division", "Cabin & Fabrication Division", "Casting Machining & Tooling Business", "Sheet Metal & Allied Business"
    ]
    
    locations = ["Gurugram", "Gurugram", "Gurugram", "Gurugram", "Gurugram", "Gurugram", "Gurugram", "Gurugram", "Tamil Nadu", "Rajasthan", "Uttarakhand", "Tamil Nadu", "Tamil Nadu", "Karnataka", "Karnataka", "Karnataka", "Pune", "Karnataka", "Pune", "Tamil Nadu"]
    lats = [28.4595, 28.4595, 28.4595, 28.4595, 28.4595, 28.4595, 28.4595, 28.4595, 11.1271, 27.0238, 30.0668, 11.1271, 11.1271, 15.3173, 15.3173, 15.3173, 18.5204, 15.3173, 18.5204, 11.1271]
    lons = [77.0266, 77.0266, 77.0266, 77.0266, 77.0266, 77.0266, 77.0266, 77.0266, 78.6569, 74.2179, 79.0193, 78.6569, 78.6569, 75.7139, 75.7139, 75.7139, 73.8567, 75.7139, 73.8567, 78.6569]
    
    capex =
    opex =
    
    apr_gen =
    may_gen =
    
    apr_kwp = [3.3, 2.8, 4.3, 3.9, 3.9, 4.5, 1.2, 3.4, 3.7, 4.9, 0.0, 2.6, 4.9, 2.3, 4.8, 3.5, 2.8, 1.6, 4.4, 4.5]
    may_kwp = [3.0, 3.1, 4.7, 3.9, 4.1, 4.6, 1.3, 3.5, 3.7, 5.1, 0.0, 2.8, 5.5, 2.4, 4.9, 3.4, 2.5, 1.8, 4.3, 4.2]
    
    losses =

    df = pd.DataFrame({
        "Unit Name": unit_names,
        "Vertical": verticals,
        "Location": locations,
        "lat": lats,
        "lon": lons,
        "CAPEX capacity": capex,
        "OPEX capacity": opex,
        "April Gen": apr_gen,
        "May Gen": may_gen,
        "April Gen/KWP": apr_kwp,
        "May Gen/KWP": may_kwp,
        "Unit Loss Inefficiency": losses
    })
    return df

df_plants = load_comprehensive_plant_matrices()

# --- INITIAL SYSTEM STATES ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Telemetry tracking engine initialized. Search across business verticals or query plant efficiency statistics."}
    ]

# --- SIDEBAR INTERFACE CONTROL PANEL ---
st.sidebar.title("🌱 Sandhar Control Panel")

# Month Selector
month_select = st.sidebar.radio("Select Target Month Context", ["April", "May"])

# Vertical Filter Page Integration
st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Segment Controls")
verticals_list = ["All Verticals"] + list(df_plants["Vertical"].unique())
selected_vertical = st.sidebar.selectbox("Business Segment Filter", verticals_list)

# Filter Data Layer
if selected_vertical == "All Verticals":
    df_filtered = df_plants.copy()
else:
    df_filtered = df_plants[df_plants["Vertical"] == selected_vertical].copy()

# Chatbot Context Engine Link
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Dashboard Core Intelligence")

def process_chat_query(user_query):
    q = user_query.upper()
    if "BEST" in q or "HIGHEST" in q:
        col = f"{month_select} Gen/KWP"
        best_row = df_filtered.loc[df_filtered[col].idxmax()]
        return f"🏆 Within the selected segment, plant node **{best_row['Unit Name']}** achieved the highest Generation/KWP ratio of **{best_row[col]}** for {month_select}."
    elif "WORST" in q or "LOWEST" in q:
        col = f"{month_select} Gen/KWP"
        active_plants = df_filtered[df_filtered[col] > 0]
        if active_plants.empty: return "No active generation detected for this selection filter."
        worst_row = active_plants.loc[active_plants[col].idxmin()]
        return f"⚠️ Optimization Alert: Plant node **{worst_row['Unit Name']}** logged the lowest active performance in {month_select} with a ratio of **{worst_row[col]}**."
    elif "LOSS" in q or "LEAKAGE" in q:
        total_loss = df_filtered["Unit Loss Inefficiency"].sum()
        return f"📉 Segment evaluation shows a total of **{int(total_loss):,} units** lost due to layout or plant operational inefficiencies."
    else:
        return "🤖 Context ready. Query me for things like: 'best performing plant' or 'operational line losses'."

# Display sidebar history
for msg in st.session_state["chat_history"]:
    with st.sidebar.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.sidebar.chat_input("Query active workspace view..."):
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    with st.sidebar.chat_message("user"):
        st.write(prompt)
        
    response = process_chat_query(prompt)
    st.session_state["chat_history"].append({"role": "assistant", "content": response})
    st.rerun()


# ================= MAIN DASHBOARD INTERFACE =================
st.title("📊 Sandhar Plant Energy Ecosystem Tracker")
st.caption(f"Visualizing live telemetry logs for **{selected_vertical}** during **{month_select}**.")
st.markdown("---")

# 1. SUMMARY KPI MATRIX CARDS
if not df_filtered.empty:
    total_month_gen = df_filtered[f"{month_select} Gen"].sum()
    total_lost_units = df_filtered["Unit Loss Inefficiency"].sum()
    avg_kwp_ratio = df_filtered[f"{month_select} Gen/KWP"].mean()
else:
    total_month_gen, total_lost_units, avg_kwp_ratio = 0, 0, 0

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
col_kpi1.metric(f"Total Production ({month_select})", f"{int(total_month_gen):,} kWh")
col_kpi2.metric("Systemic Inefficiency Loss", f"{int(total_lost_units):,} Units", delta="Leakage Log", delta_color="inverse")
col_kpi3.metric(f"Average Gen / KWP ({month_select})", f"{avg_kwp_ratio:.2f}")

st.markdown("---")

# 2. GENERATION BAR CHART
if not df_filtered.empty:
    st.subheader(f"📈 Comparative Power Yield Grid — {month_select}")
    fig_gen = px.bar(
        df_filtered, x="Unit Name", y=f"{month_select} Gen",
        color="Vertical", title=f"Total Generated Units per Selected Node Cluster (`kWh`)",
        color_discrete_sequence=px.colors.qualitative.Safe, text_auto=True
    )
    fig_gen.update_layout(height=400)
    st.plotly_chart(fig_gen, use_container_width=True)

# 3. GEOSPATIAL MAP SEGMENT
if not df_filtered.empty:
    st.subheader("🗺️ Telepatial Asset Distribution Node Map")
    # Dynamic scaling based on production metrics
    df_filtered["Map_Marker_Size"] = df_filtered[f"{month_select} Gen"] + 1000 
    fig_global_map = px.scatter_mapbox(
        df_filtered, lat="lat", lon="lon", size="Map_Marker_Size", color="Vertical",
        hover_name="Unit Name", hover_data=["Location", f"{month_select} Gen", "Unit Loss Inefficiency"],
        zoom=4.0, height=420, color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_global_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_global_map, use_container_width=True)

st.markdown("---")

# 4. CONDITIONAL FORMATTING GENERATION MATRIX LIST
st.subheader("📋 Core Plant Node Metrics Ledger")
st.markdown("💡 **Format Matrix Rules**: `Ratio >= 3.0` 🟢 **High Yield Performance** | `Ratio < 3.0` 🔴 **Under Threshold Status**")

if df_filtered.empty:
    st.warning("No plant nodes match the selected filtering combinations.")
else:
    # Group plant matrix grid layouts cleanly into rows of 4
    for i in range(0, len(df_filtered), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(df_filtered):
                row = df_filtered.iloc[i + j]
                ratio_val = row[f"{month_select} Gen/KWP"]
                gen_val = row[f"{month_select} Gen"]
                loss_val = row["Unit Loss Inefficiency"]
                
                with cols[j]:
                    # Strict validation rule processing (3.0 or higher is Green, under 3.0 is Red)
                    if ratio_val >= 3.0:
                        border_color = "#10b981"  # Emerald Green
                        status_badge = f"<span style='color:{border_color}; font-weight:bold;'>🟢 {ratio_val} (Optimal)</span>"
                    else:
                        border_color = "#ef4444"  # Crimson Red
                        status_badge = f"<span style='color:{border_color}; font-weight:bold;'>🔴 {ratio_val} (Low Performance)</span>"
                    
                    st.markdown(f"""
                    <div style="border: 2px solid {border_color}; border-radius: 12px; padding: 15px; margin-bottom: 15px; background-color: rgba(255,255,255,0.02);">
                        <h4 style="margin: 0 0 4px 0; color: #f1f5f9;">🏢 Plant Node: {row['Unit Name']}</h4>
                        <p style="margin: 0 0 8px 0; font-size: 11px; color: #64748b; text-transform: uppercase;"><b>{row['Vertical']}</b></p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Location:</b> {row['Location']}</p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Generation:</b> {int(gen_val):,} kWh</p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Loss Track:</b> {int(loss_val):,} Units</p>
                        <p style="margin: 8px 0 0 0; font-size: 14px;"><b>KWP Ratio:</b> {status_badge}</p>
                    </div>
                    """, unsafe_allow_html=True)
