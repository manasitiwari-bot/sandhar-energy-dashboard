import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Energy Dashboard",
    page_icon="🌱",
    layout="wide"
)

# --- DIRECT INDUSTRIAL RAW DATA INJECTION ---
raw_plant_records = [
    {"Unit Name": "SAG", "Vertical": "Automotive Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 3245, "May Gen": 3120, "April Gen/KWP": 3.3, "May Gen/KWP": 3.0, "Unit Loss Inefficiency": 2689},
    {"Unit Name": "SCD", "Vertical": "Plastic Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 9079, "May Gen": 10500, "April Gen/KWP": 2.8, "May Gen/KWP": 3.1, "Unit Loss Inefficiency": 10602},
    {"Unit Name": "SEB", "Vertical": "Sheet Metal & Allied Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 16958, "May Gen": 19259, "April Gen/KWP": 4.3, "May Gen/KWP": 4.7, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SAD", "Vertical": "Automotive Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 40627, "May Gen": 42113, "April Gen/KWP": 3.9, "May Gen/KWP": 3.9, "Unit Loss Inefficiency": 13290},
    {"Unit Name": "SCR", "Vertical": "Casting Machining & Tooling Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 16232, "May Gen": 17607, "April Gen/KWP": 3.9, "May Gen/KWP": 4.1, "Unit Loss Inefficiency": 4024},
    {"Unit Name": "STPL", "Vertical": "Casting Machining & Tooling Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 27557, "May Gen": 29168, "April Gen/KWP": 4.5, "May Gen/KWP": 4.6, "Unit Loss Inefficiency": 0},
    {"Unit Name": "ACM", "Vertical": "Casting Machining & Tooling Business", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 1742, "May Gen": 2089, "April Gen/KWP": 1.2, "May Gen/KWP": 1.3, "Unit Loss Inefficiency": 9888},
    {"Unit Name": "CORP", "Vertical": "Corp. Office", "Location": "Gurugram", "lat": 28.4595, "lon": 77.0266, "April Gen": 3696, "May Gen": 3900, "April Gen/KWP": 3.4, "May Gen/KWP": 3.5, "Unit Loss Inefficiency": 2281},
    {"Unit Name": "SASPL", "Vertical": "Corp. Office", "Location": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569, "April Gen": 14271, "May Gen": 14504, "April Gen/KWP": 3.7, "May Gen/KWP": 3.7, "Unit Loss Inefficiency": 6070},
    {"Unit Name": "SHP", "Vertical": "Automotive Business", "Location": "Rajasthan", "lat": 27.0238, "lon": 74.2179, "April Gen": 3704, "May Gen": 3946, "April Gen/KWP": 4.9, "May Gen/KWP": 5.1, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SAH", "Vertical": "Automotive Business", "Location": "Uttarakhand", "lat": 30.0668, "lon": 79.0193, "April Gen": 0, "May Gen": 0, "April Gen/KWP": 0.0, "May Gen/KWP": 0.0, "Unit Loss Inefficiency": 41156},
    {"Unit Name": "SCH", "Vertical": "Casting Machining & Tooling Business", "Location": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569, "April Gen": 31789, "May Gen": 34594, "April Gen/KWP": 2.6, "May Gen/KWP": 2.8, "Unit Loss Inefficiency": 43640},
    {"Unit Name": "SIO", "Vertical": "Automotive Business", "Location": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569, "April Gen": 38692, "May Gen": 44353, "April Gen/KWP": 4.9, "May Gen/KWP": 5.5, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SCA", "Vertical": "Casting Machining & Tooling Business", "Location": "Karnataka", "lat": 15.3173, "lon": 75.7139, "April Gen": 17552, "May Gen": 18785, "April Gen/KWP": 2.3, "May Gen/KWP": 2.4, "Unit Loss Inefficiency": 32256},
    {"Unit Name": "SAB", "Vertical": "Automotive Business", "Location": "Karnataka", "lat": 15.3173, "lon": 75.7139, "April Gen": 18763, "May Gen": 19767, "April Gen/KWP": 4.8, "May Gen/KWP": 4.9, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SCY", "Vertical": "Sheet Metal & Allied Business", "Location": "Karnataka", "lat": 15.3173, "lon": 75.7139, "April Gen": 35156, "May Gen": 35751, "April Gen/KWP": 3.5, "May Gen/KWP": 3.4, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SIP", "Vertical": "Cabin & Fabrication Division", "Location": "Pune", "lat": 18.5204, "lon": 73.8567, "April Gen": 10373, "May Gen": 9605, "April Gen/KWP": 2.8, "May Gen/KWP": 2.5, "Unit Loss Inefficiency": 6401},
    {"Unit Name": "SIA", "Vertical": "Cabin & Fabrication Division", "Location": "Karnataka", "lat": 15.3173, "lon": 75.7139, "April Gen": 5437, "May Gen": 6270, "April Gen/KWP": 1.6, "May Gen/KWP": 1.8, "Unit Loss Inefficiency": 12562},
    {"Unit Name": "SKC", "Vertical": "Casting Machining & Tooling Business", "Location": "Pune", "lat": 18.5204, "lon": 73.8567, "April Gen": 44884, "May Gen": 45175, "April Gen/KWP": 4.4, "May Gen/KWP": 4.3, "Unit Loss Inefficiency": 0},
    {"Unit Name": "SHN", "Vertical": "Sheet Metal & Allied Business", "Location": "Tamil Nadu", "lat": 11.1271, "lon": 78.6569, "April Gen": 85838, "May Gen": 81833, "April Gen/KWP": 4.5, "May Gen/KWP": 4.2, "Unit Loss Inefficiency": 0}
]

df_plants = pd.DataFrame(raw_plant_records)

# --- INITIAL SYSTEM STATES ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Telemetry engine initialized. Search across business verticals or query plant metrics."}
    ]

# --- SIDEBAR INTERFACE CONTROL PANEL ---
st.sidebar.title("🌱 Sandhar Control Panel")
month_select = st.sidebar.radio("Select Target Month Context", ["April", "May"])

st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Segment Controls")
verticals_list = ["All Verticals"] + list(df_plants["Vertical"].unique())
selected_vertical = st.sidebar.selectbox("Business Segment Filter", verticals_list)

if selected_vertical == "All Verticals":
    df_filtered = df_plants.copy()
else:
    df_filtered = df_plants[df_plants["Vertical"] == selected_vertical].copy()

# Chatbot Core
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Dashboard Core Intelligence")

def process_chat_query(user_query):
    q = user_query.upper()
    if "BEST" in q or "HIGHEST" in q:
        col = f"{month_select} Gen/KWP"
        best_row = df_filtered.loc[df_filtered[col].idxmax()]
        return f"🏆 Node **{best_row['Unit Name']}** achieved the highest Generation/KWP ratio of **{best_row[col]}** for {month_select}."
    elif "WORST" in q or "LOWEST" in q:
        col = f"{month_select} Gen/KWP"
        active_plants = df_filtered[df_filtered[col] > 0]
        if active_plants.empty: return "No active generation detected."
        worst_row = active_plants.loc[active_plants[col].idxmin()]
        return f"⚠️ Optimization Alert: Node **{worst_row['Unit Name']}** logged the lowest active performance ratio of **{worst_row[col]}**."
    elif "LOSS" in q or "LEAKAGE" in q:
        total_loss = df_filtered["Unit Loss Inefficiency"].sum()
        return f"📉 Selection analysis shows a total of **{int(total_loss):,} units** logged under line inefficiency logs."
    else:
        return "🤖 Context ready. Ask me about 'best performing plant' or 'operational line losses'."

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
st.caption(f"Visualizing telemetry logs for **{selected_vertical}** during **{month_select}**.")
st.markdown("---")

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

if not df_filtered.empty:
    st.subheader(f"📈 Comparative Power Yield Grid — {month_select}")
    fig_gen = px.bar(
        df_filtered, x="Unit Name", y=f"{month_select} Gen",
        color="Vertical", title="Total Generated Units per Selected Node Cluster (kWh)",
        color_discrete_sequence=px.colors.qualitative.Safe, text_auto=True
    )
    fig_gen.update_layout(height=400)
    st.plotly_chart(fig_gen, use_container_width=True)

    st.subheader("🗺️ Asset Distribution Node Map")
    df_filtered["Map_Marker_Size"] = df_filtered[f"{month_select} Gen"] + 1000 
    fig_global_map = px.scatter_mapbox(
        df_filtered, lat="lat", lon="lon", size="Map_Marker_Size", color="Vertical",
        hover_name="Unit Name", hover_data=["Location", f"{month_select} Gen"],
        zoom=3.5, height=400, color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_global_map.update_layout(mapbox_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_global_map, use_container_width=True)

st.markdown("---")
st.subheader("📋 Core Plant Node Metrics Ledger")
st.markdown("💡 Rules: `Ratio >= 3.0` 🟢 **Optimal** | `Ratio < 3.0` 🔴 **Under Threshold**")

if df_filtered.empty:
    st.warning("No plant nodes match selection filters.")
else:
    for i in range(0, len(df_filtered), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(df_filtered):
                row = df_filtered.iloc[i + j]
                ratio_val = row[f"{month_select} Gen/KWP"]
                gen_val = row[f"{month_select} Gen"]
                loss_val = row["Unit Loss Inefficiency"]
                
                with cols[j]:
                    if ratio_val >= 3.0:
                        border_color = "#10b981"
                        status_badge = f"<span style='color:{border_color}; font-weight:bold;'>🟢 {ratio_val} (Optimal)</span>"
                    else:
                        border_color = "#ef4444"
                        status_badge = f"<span style='color:{border_color}; font-weight:bold;'>🔴 {ratio_val} (Low)</span>"
                    
                    st.markdown(f"""
                    <div style="border: 2px solid {border_color}; border-radius: 12px; padding: 15px; margin-bottom: 15px; background-color: rgba(255,255,255,0.02);">
                        <h4 style="margin: 0 0 4px 0; color: #f1f5f9;">🏢 Plant: {row['Unit Name']}</h4>
                        <p style="margin: 0 0 8px 0; font-size: 11px; color: #64748b; text-transform: uppercase;"><b>{row['Vertical']}</b></p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Location:</b> {row['Location']}</p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Generation:</b> {int(gen_val):,} kWh</p>
                        <p style="margin: 4px 0; font-size: 13px; color: #94a3b8;"><b>Loss:</b> {int(loss_val):,} Units</p>
                        <p style="margin: 8px 0 0 0; font-size: 14px;"><b>KWP Ratio:</b> {status_badge}</p>
                    </div>
                    """, unsafe_allow_html=True)
