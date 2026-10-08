import streamlit as st
import pandas as pd
import io
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Sandhar Executive Energy Portal",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for Animations, Glassmorphism, and Presentation Styling
st.markdown("""
    <style>
    /* Smooth entrance animation for presentation feel */
    @keyframes fadeInScale {
        0% { opacity: 0; transform: scale(0.98) translateY(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Executive Glass Cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        animation: fadeInScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        backdrop-filter: blur(12px);
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Animated Ticker Bar */
    .ticker-wrap {
        width: 100%;
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #0d9488;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 24px;
        animation: fadeInScale 0.4s ease-out;
    }

    .ticker-text {
        font-size: 0.95rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    .highlight {
        color: #38bdf8;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Raw Dataset (Automotive Segment Cleaned Data)
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

# Calculate CAPEX and OPEX Generation ratios
df['CAPEX Solar Gen (KWh)'] = df.apply(
    lambda r: (r['Capex (KWp)'] / (r['Capex (KWp)'] + r['Opex (KWp)'])) * r['Capex & Opex (KWh)'] 
    if (r['Capex (KWp)'] + r['Opex (KWp)']) > 0 else 0, axis=1
)
df['OPEX Solar Gen (KWh)'] = df['Capex & Opex (KWh)'] - df['CAPEX Solar Gen (KWh)']

# 3. Header & Live Ticker
st.title("⚡ Sandhar Group — Automotive Division")
st.markdown("""
<div class="ticker-wrap">
    <span class="ticker-text">
        📡 <b>Live Performance Summary:</b> Evaluating <span class="highlight">7 Key Operational Assets</span> | Highest Grid Sourcing: <span class="highlight">SAH Node</span> | Total Green Power Offset: <span class="highlight">4,726,176 KWh</span>
    </span>
</div>
""", unsafe_allow_html=True)

# 4. KPI Scorecards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Grid Consumption", f"{df['Yearly Grid Consumption (KVAh)'].sum():,.0f} KVAh")
col2.metric("CAPEX Solar Gen", f"{df['CAPEX Solar Gen (KWh)'].sum():,.0f} KWh")
col3.metric("OPEX Solar Gen", f"{df['OPEX Solar Gen (KWh)'].sum():,.0f} KWh")
col4.metric("Open Access Green", f"{df['Open Access (KWh)'].sum():,.0f} KWh")

st.markdown("<br>", unsafe_allow_html=True)

# 5. Side-by-Side Graph with Neutral Tones
st.subheader("📊 Plant-Level Energy Sourcing & Generation Profile")

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
    labels={'Unit Code': 'Plant Node Code', 'Volume': 'Units (KWh / KVAh)'},
    color_discrete_map={
        'CAPEX Solar Gen (KWh)': '#0d9488',         # Cool Sage Green
        'OPEX Solar Gen (KWh)': '#64748b',          # Neutral Steel Slate
        'Yearly Grid Consumption (KVAh)': '#3b82f6'  # Executive Steel Blue
    },
    template="plotly_dark"
)

# Smooth hover templates and chart layout tweaks
fig.update_traces(
    hovertemplate="<b>%{x}</b><br>%{fullData.name}: <b>%{y:,.0f}</b><extra></extra>"
)

fig.update_layout(
    height=480,
    xaxis_tickangle=0,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        title_text=""
    ),
    font=dict(family="Inter, sans-serif", color="#e2e8f0")
)

st.plotly_chart(fig, use_container_width=True)

# 6. Executive Summary Table
st.markdown("---")
st.subheader("📋 Operational Node Ledger")

display_df = df[['Unit Code', 'CAPEX Solar Gen (KWh)', 'OPEX Solar Gen (KWh)', 'Yearly Grid Consumption (KVAh)', 'Total Units Generation Green Energy (KWh)']].copy()
display_df.columns = ['Plant Node', 'CAPEX Solar (KWh)', 'OPEX Solar (KWh)', 'Grid Consumption (KVAh)', 'Total Green Energy (KWh)']

st.dataframe(
    display_df.style.format({
        'CAPEX Solar (KWh)': '{:,.0f}',
        'OPEX Solar (KWh)': '{:,.0f}',
        'Grid Consumption (KVAh)': '{:,.0f}',
        'Total Green Energy (KWh)': '{:,.0f}'
    }),
    use_container_width=True,
    hide_index=True
)
