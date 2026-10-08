import streamlit as st
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sandhar Energy Management Portal",
    page_icon="⚡",
    layout="wide"
)

# Bypass auth by default so app renders instantly
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

# -----------------------------------------------------------------------------
# 2. LOAD DATASET FROM NEW SHEET
# -----------------------------------------------------------------------------
@st.cache_data
def load_new_energy_matrix():
    raw_csv = """Business Vertical,Unit Code,Contract Load (KVA),Capex (KWp),Opex (KWp),Open Access (KWp),Capex & Opex (KWh),Open Access (KWh),Yearly Grid Consumption (KVAh),Total Units Generation Green Energy (KWh),Green Energy Capacity (KWp)
Automotive Business,SAD & SPB,1300,138,218,950,143033,1423100,5144314,1566133,1306
Automotive Business,SAG & SEG & SRD,600,33,0,450,33878,674100,0,707978,483
Automotive Business,SAH,1250,251,129,0,271338,0,6249956,271338,380
Automotive Business,SAB,470,0,340,810,442802,1213380,2028994,1656182,1150
Automotive Business,SAESPL,0,0,0,0,0,0,0,0,0
Automotive Business,SAP,120,0,0,0,0,0,98516,0,0
Automotive Business,SHP,800,400,262,0,524545,0,950145,524545,662
Automotive Business,SAT,195,0,0,0,0,0,515518,0,0
Sheet Metal & Allied Business,SEB & SAESPL,800,50,300,0,364741,0,2940138,364741,350
Sheet Metal & Allied Business,SCK,950,0,0,1222,0,1830556,3089595,1830556,1222
Sheet Metal & Allied Business,SCY,750,0,634,0,883541,0,2689597,883541,634
Sheet Metal & Allied Business,SEK / SMA-PLT / MFG,1600,0,0,2434,0,3646132,5170330,3646132,2434
Sheet Metal & Allied Business,SMD,99,0,0,0,0,0,308388,0,0
Sheet Metal & Allied Business,SEH / SCG,400,0,0,0,0,0,891140,0,427
Sheet Metal & Allied Business,SMN,80,0,0,0,0,0,139210,0,0
Sheet Metal & Allied Business,SMO,0,0,0,0,23029,0,1641744,23029,0
Sheet Metal & Allied Business,SHN / SCN,650,0,624,0,398942,0,2257322,398942,624
Casting Machining & Tooling Business,ACM (SCM),650,127,0,400,122960,599200,3419576,722160,527
Casting Machining & Tooling Business,ACR (SCR),2100,50,0,2430,8865,3640140,12040981,3649005,2480
Casting Machining & Tooling Business,ATPL (STPL),205,36,0,0,33266,0,453030,33266,36
Casting Machining & Tooling Business,SMK,900,0,0,1617,0,2422266,3882610,2422266,1617
Casting Machining & Tooling Business,ACA (SCA),600,115,0,1617,88659,2422266,3652400,2510925,1732
Casting Machining & Tooling Business,SKC,560,0,604,0,381131,0,2022556,381131,604
Casting Machining & Tooling Business,SMT,1200,0,0,1765,0,2643970,5110672,2643970,1765
Casting Machining & Tooling Business,ADH (SCH),2400,0,336,3795,1434144,5684910,13731825,7119054,4131
Casting Machining & Tooling Business,ACO (SCO),1000,0,0,850,0,1273300,274368,1273300,850
Casting Machining & Tooling Business,ACH,3500,0,0,4050,3979800,6066900,18864562,10046700,6998
Cabin & Fabrication Division,SIA,550,115,0,0,29610,0,1997840,29610,115
Cabin & Fabrication Division,SID,750,0,0,0,0,0,1568476,0,0
Cabin & Fabrication Division,SIP,650,0,717,0,891451,0,191883,891451,717
Cabin & Fabrication Division,SIJ,800,0,0,0,0,0,3132454,0,0
Cabin & Fabrication Division,SIO,600,0,125,0,110985,0,150803,110985,125
Corp. Office,CORP,310,25,0,0,33483,0,245015,33483,25
Corp. Office,SASPL,250,150,0,0,66246,0,157164,66246,150
Joint Venture Business,JSW,0,0,0,0,0,0,102080,0,0
Joint Venture Business,SHG / SHT,301,0,0,0,0,0,533451,0,0
Joint Venture Business,SHA,50,0,0,0,0,0,48971,0,0
Joint Venture Business,JWS,0,0,0,0,0,0,101507,0,0
Joint Venture Business,SAM,350,0,0,0,0,0,490180,0,0
Joint Venture Business,SHC,360,0,0,0,0,0,792536,0,0
Plastic Business,SCD,600,0,550,0,237971,823900,2664678,1061871,792
"""
    return pd.read_csv(io.StringIO(raw_csv.strip()))

df = load_new_energy_matrix()

# Calculate CAPEX and OPEX Generations explicitly from capacity proportions
df['Capex_Gen_kWh'] = df.apply(
    lambda r: (r['Capex (KWp)'] / (r['Capex (KWp)'] + r['Opex (KWp)'])) * r['Capex & Opex (KWh)'] 
    if (r['Capex (KWp)'] + r['Opex (KWp)']) > 0 else 0, axis=1
)
df['Opex_Gen_kWh'] = df['Capex & Opex (KWh)'] - df['Capex_Gen_kWh']

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.title("⚡ Navigation & Filters")
selected_vertical = st.sidebar.selectbox(
    "Select Business Vertical",
    ["All Verticals"] + list(df['Business Vertical'].unique())
)

if selected_vertical != "All Verticals":
    filtered_df = df[df['Business Vertical'] == selected_vertical].copy()
else:
    filtered_df = df.copy()

# Remove aggregate zero-rows for cleaner charts
filtered_df = filtered_df[filtered_df['Unit Code'].str.contains("Total") == False]

# -----------------------------------------------------------------------------
# 4. DASHBOARD HEADER & KPI CARDS
# -----------------------------------------------------------------------------
st.title("🌱 Sandhar Group - Energy Generation & Grid Sourcing Matrix")
st.caption("Live comparison showing CAPEX Generation, OPEX Generation, and Yearly Grid Sourcing across plant nodes.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Grid Sourced", f"{filtered_df['Yearly Grid Consumption (KVAh)'].sum():,.0f} KVAh")
kpi2.metric("Total Green Energy", f"{filtered_df['Total Units Generation Green Energy (KWh)'].sum():,.0f} KWh")
kpi3.metric("CAPEX & OPEX Generation", f"{filtered_df['Capex & Opex (KWh)'].sum():,.0f} KWh")
kpi4.metric("Open Access Green Power", f"{filtered_df['Open Access (KWh)'].sum():,.0f} KWh")

st.divider()

# -----------------------------------------------------------------------------
# 5. MAIN GRAPH: CAPEX VS OPEX VS GRID CONSUMPTION COMPARISON
# -----------------------------------------------------------------------------
st.subheader("📊 Plant-Wise Comparison: CAPEX Gen vs OPEX Gen vs Grid Consumption")

# Reshape data into long format for grouped Plotly bar chart
chart_df = filtered_df.melt(
    id_vars=['Unit Code', 'Business Vertical'],
    value_vars=['Capex_Gen_kWh', 'Opex_Gen_kWh', 'Yearly Grid Consumption (KVAh)'],
    var_name='Energy Source',
    value_name='Energy (KWh/KVAh)'
)

# Clean labels for chart legend
label_map = {
    'Capex_Gen_kWh': 'CAPEX Solar Gen (KWh)',
    'Opex_Gen_kWh': 'OPEX Solar Gen (KWh)',
    'Yearly Grid Consumption (KVAh)': 'Yearly Grid Consumption (KVAh)'
}
chart_df['Energy Source'] = chart_df['Energy Source'].map(label_map)

fig_grouped = px.bar(
    chart_df,
    x='Unit Code',
    y='Energy (KWh/KVAh)',
    color='Energy Source',
    barmode='group',
    title=f"Energy Profile Comparison across Plants ({selected_vertical})",
    labels={'Unit Code': 'Plant Node Code', 'Energy (KWh/KVAh)': 'Energy Volume'},
    color_discrete_map={
        'CAPEX Solar Gen (KWh)': '#10b981',
        'OPEX Solar Gen (KWh)': '#3b82f6',
        'Yearly Grid Consumption (KVAh)': '#ef4444'
    },
    template="plotly_dark"
)

fig_grouped.update_layout(
    xaxis_tickangle=-45,
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_grouped, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 6. DETAILED DATA LEDGER TABLE
# -----------------------------------------------------------------------------
st.subheader("📋 Operational Node Energy Ledger")

display_cols = [
    'Business Vertical', 'Unit Code', 'Contract Load (KVA)', 
    'Capex_Gen_kWh', 'Opex_Gen_kWh', 'Open Access (KWh)', 
    'Yearly Grid Consumption (KVAh)', 'Total Units Generation Green Energy (KWh)'
]

table_df = filtered_df[display_cols].copy()
table_df.columns = [
    'Vertical', 'Node', 'Contract (KVA)', 
    'CAPEX Gen (KWh)', 'OPEX Gen (KWh)', 'Open Access (KWh)', 
    'Grid Consumption (KVAh)', 'Total Green Units (KWh)'
]

st.dataframe(
    table_df.style.format({
        'Contract (KVA)': '{:,.0f}',
        'CAPEX Gen (KWh)': '{:,.0f}',
        'OPEX Gen (KWh)': '{:,.0f}',
        'Open Access (KWh)': '{:,.0f}',
        'Grid Consumption (KVAh)': '{:,.0f}',
        'Total Green Units (KWh)': '{:,.0f}'
    }),
    use_container_width=True,
    hide_index=True
)
