import streamlit as st
import pandas as pd
import io
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Automotive Energy Dashboard",
    page_icon="⚡",
    layout="wide"
)

# 2. Raw Dataset Embed (Automotive Business Filtered + Cleaned)
raw_csv = """Business Vertical,Unit Code,Contract Load (KVA),Capex (KWp),Opex (KWp),Open Access (KWp),Capex & Opex (KWh),Open Access (KWh),Yearly Grid Consumption (KVAh),Total Units Generation Green Energy (KWh),Green Energy Capacity (KWp)
Automotive Business,SAD & SPB,1300,138,218,950,143033,1423100,5144314,1566133,1306
Automotive Business,SAG & SEG & SRD,600,33,0,450,33878,674100,2345225,707978,483
Automotive Business,SAH,1250,251,129,0,271338,0,6249956,271338,380
Automotive Business,SAB,470,0,340,810,442802,1213380,2028994,1656182,1150
Automotive Business,SAP,120,0,0,0,0,0,98516,0,0
Automotive Business,SHP,800,400,262,0,524545,0,950145,524545,662
Automotive Business,SAT,195,0,0,0,0,0,515518,0,0
"""

df = pd.read_csv(io.StringIO(raw_csv.strip()))

# Calculate CAPEX and OPEX Generation ratios accurately
df['CAPEX Solar Gen (KWh)'] = df.apply(
    lambda r: (r['Capex (KWp)'] / (r['Capex (KWp)'] + r['Opex (KWp)'])) * r['Capex & Opex (KWh)'] 
    if (r['Capex (KWp)'] + r['Opex (KWp)']) > 0 else 0, axis=1
)
df['OPEX Solar Gen (KWh)'] = df['Capex & Opex (KWh)'] - df['CAPEX Solar Gen (KWh)']

# 3. Header & Top Metrics
st.title("⚡ Sandhar Energy Management Portal")
st.markdown("### 🏎️ Automotive Business Segment Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Grid Consumption", f"{df['Yearly Grid Consumption (KVAh)'].sum():,.0f} KVAh")
col2.metric("CAPEX + OPEX Solar Gen", f"{df['Capex & Opex (KWh)'].sum():,.0f} KWh")
col3.metric("Open Access Green Energy", f"{df['Open Access (KWh)'].sum():,.0f} KWh")

st.markdown("---")

# 4. Plant Comparison Graph (Clean & Professional Colors)
st.subheader("📊 Automotive Plants: CAPEX Gen vs OPEX Gen vs Grid Consumption")

chart_df = df.melt(
    id_vars=['Unit Code'],
    value_vars=['CAPEX Solar Gen (KWh)', 'OPEX Solar Gen (KWh)', 'Yearly Grid Consumption (KVAh)'],
    var_name='Energy Stream',
    value_name='Volume'
)

fig = px.bar(
    chart_df,
    x='Unit Code',
    y='Volume',
    color='Energy Stream',
    barmode='group',
    title="Energy Comparison per Operational Unit",
    labels={'Unit Code': 'Plant Node Code', 'Volume': 'Units (KWh / KVAh)'},
    color_discrete_map={
        'CAPEX Solar Gen (KWh)': '#3B82F6',        # Slate Blue
        'OPEX Solar Gen (KWh)': '#10B981',         # Mint Teal
        'Yearly Grid Consumption (KVAh)': '#F59E0B' # Warm Amber
    },
    template="plotly_dark"
)

fig.update_layout(
    height=500, 
    xaxis_tickangle=0,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# 5. Data Ledger Table
st.markdown("---")
st.subheader("📋 Plant Ledger")
st.dataframe(
    df[['Unit Code', 'CAPEX Solar Gen (KWh)', 'OPEX Solar Gen (KWh)', 'Yearly Grid Consumption (KVAh)', 'Total Units Generation Green Energy (KWh)']],
    use_container_width=True,
    hide_index=True
)
