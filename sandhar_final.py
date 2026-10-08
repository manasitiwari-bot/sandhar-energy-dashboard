import streamlit as st
import pandas as pd
import io
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Automotive Energy Portal",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for Light Presentation Theme
st.markdown("""
    <style>
    @keyframes fadeInScale {
        0% { opacity: 0; transform: scale(0.98) translateY(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        animation: fadeInScale 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }

    .ticker-wrap {
        width: 100%;
        background: #ffffff;
        border-left: 5px solid #0284c7;
        border: 1px solid #e2e8f0;
        border-left-width: 5px;
        padding: 14px 20px;
        border-radius: 10px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .ticker-text {
        font-size: 0.95rem;
        color: #334155;
        font-weight: 500;
    }

    .highlight {
        color: #0284c7;
        font-weight: 700;
    }
    
    h1, h2, h3 {
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Raw Dataset (Automotive Business Segment Only)
raw_csv = """Business Vertical,Unit Code,Contract Load (KVA),Capex (KWp),Opex (KWp),Capex & Opex (KWh),Yearly Grid Consumption (KVAh),Total Units Generation Green Energy (KWh),Green Energy Capacity (KWp)
Automotive Business,SAD & SPB,1300,138,218,143033,5144314,1566133,1306
Automotive Business,SAG & SEG & SRD,600,33,0,33878,2345225,707978,483
Automotive Business,SAH,1250,251,129,271338,6249956,271338,380
Automotive Business,SAB,470,0,340,442802,2028994,1656182,1150
Automotive Business,SAP,120,0,0,0,98516,0,0
Automotive Business,SHP,800,400,262,524545,950145,524545,662
Automotive Business,SAT,195,0,0,0,515518,0,0
"""

df = pd.read_csv(io.StringIO(raw_csv.strip()))

# Calculations
df['CAPEX Solar Gen (KWh)'] = df.apply(
    lambda r: (r['Capex (KWp)'] / (r['Capex (KWp)'] + r['Opex (KWp)'])) * r['Capex & Opex (KWh)'] 
    if (r['Capex (KWp)'] + r['Opex (KWp)']) > 0 else 0, axis=1
)
df['OPEX Solar Gen (KWh)'] = df['Capex & Opex (KWh)'] - df['CAPEX Solar Gen (KWh)']

# Replacement % = Green Gen / (Grid + Green Gen) * 100
df['Replacement %'] = df.apply(
    lambda r: (r['Total Units Generation Green Energy (KWh)'] / (r['Yearly Grid Consumption (KVAh)'] + r['Total Units Generation Green Energy (KWh)'])) * 100
    if (r['Yearly Grid Consumption (KVAh)'] + r['Total Units Generation Green Energy (KWh)']) > 0 else 0, axis=1
)

# Carbon Metrics (Factor: 0.82 kg CO2 per kWh -> converted to Metric Tons MT)
df['Carbon Offset (MT CO2)'] = (df['Total Units Generation Green Energy (KWh)'] * 0.82) / 1000
df['Gross Footprint (MT CO2)'] = (df['Yearly Grid Consumption (KVAh)'] * 0.82) / 1000

# 3. Header & Live Ticker
st.title("⚡ Sandhar Group — Automotive Division")
st.markdown(f"""
<div class="ticker-wrap">
    <span class="ticker-text">
        🏎️ <b>Automotive Segment Overview:</b> Evaluating <span class="highlight">7 Operational Units</span> | Avg Green Shift: <span class="highlight">{df['Replacement %'].mean():.1f}%</span> | Total Carbon Offset: <span class="highlight">{df['Carbon Offset (MT CO2)'].sum():,.0f} MT CO₂</span>
    </span>
</div>
""", unsafe_allow_html=True)

# 4. KPI Scorecards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Grid Consumption", f"{df['Yearly Grid Consumption (KVAh)'].sum():,.0f} KVAh")
col2.metric("CAPEX Solar Gen", f"{df['CAPEX Solar Gen (KWh)'].sum():,.0f} KWh")
col3.metric("OPEX Solar Gen", f"{df['OPEX Solar Gen (KWh)'].sum():,.0f} KWh")
col4.metric("Green Shift %", f"{(df['Total Units Generation Green Energy (KWh)'].sum() / (df['Yearly Grid Consumption (KVAh)'].sum() + df['Total Units Generation Green Energy (KWh)'].sum())) * 100:.1f}%")
col5.metric("Carbon Offset", f"{df['Carbon Offset (MT CO2)'].sum():,.0f} MT CO₂")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Charts Side-by-Side
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📊 Plant-Wise Energy Comparison")
    chart_df = df.melt(
        id_vars=['Unit Code'],
        value_vars=['CAPEX Solar Gen (KWh)', 'OPEX Solar Gen (KWh)', 'Yearly Grid Consumption (KVAh)'],
        var_name='Energy Stream',
        value_name='Volume'
    )

    fig1 = px.bar(
        chart_df,
        x='Unit Code',
        y='Volume',
        color='Energy Stream',
        barmode='group',
        labels={'Unit Code': 'Plant Node Code', 'Volume': 'Units (KWh / KVAh)'},
        color_discrete_map={
            'CAPEX Solar Gen (KWh)': '#0d9488',         # Clean Teal
            'OPEX Solar Gen (KWh)': '#64748b',          # Neutral Slate Gray
            'Yearly Grid Consumption (KVAh)': '#0284c7'  # Executive Steel Blue
        },
        template="plotly_white"
    )
    fig1.update_layout(height=420, paper_bgcolor='#f8fafc', plot_bgcolor='#ffffff', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=""))
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.subheader("🌱 Carbon Mitigation vs Gross Emissions")
    carbon_df = df.melt(
        id_vars=['Unit Code'],
        value_vars=['Carbon Offset (MT CO2)', 'Gross Footprint (MT CO2)'],
        var_name='Carbon Metric',
        value_name='Metric Tons CO2'
    )

    fig2 = px.bar(
        carbon_df,
        x='Unit Code',
        y='Metric Tons CO2',
        color='Carbon Metric',
        barmode='group',
        labels={'Unit Code': 'Plant Node Code', 'Metric Tons CO2': 'MT CO₂'},
        color_discrete_map={
            'Carbon Offset (MT CO2)': '#10b981',    # Emerald Green
            'Gross Footprint (MT CO2)': '#94a3b8'   # Muted Grey
        },
        template="plotly_white"
    )
    fig2.update_layout(height=420, paper_bgcolor='#f8fafc', plot_bgcolor='#ffffff', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=""))
    st.plotly_chart(fig2, use_container_width=True)

# 6. Operational Ledger Table
st.markdown("---")
st.subheader("📋 Operational Node Energy & Carbon Ledger")

display_df = df[[
    'Unit Code', 'CAPEX Solar Gen (KWh)', 'OPEX Solar Gen (KWh)', 
    'Yearly Grid Consumption (KVAh)', 'Replacement %', 
    'Carbon Offset (MT CO2)', 'Gross Footprint (MT CO2)'
]].copy()

display_df.columns = [
    'Plant Node', 'CAPEX Solar (KWh)', 'OPEX Solar (KWh)', 
    'Grid Consumption (KVAh)', 'Replacement %', 
    'Carbon Offset (MT CO₂)', 'Gross Footprint (MT CO₂)'
]

st.dataframe(
    display_df.style.format({
        'CAPEX Solar (KWh)': '{:,.0f}',
        'OPEX Solar (KWh)': '{:,.0f}',
        'Grid Consumption (KVAh)': '{:,.0f}',
        'Replacement %': '{:.1f}%',
        'Carbon Offset (MT CO₂)': '{:,.1f}',
        'Gross Footprint (MT CO₂)': '{:,.1f}'
    }),
    use_container_width=True,
    hide_index=True
)
