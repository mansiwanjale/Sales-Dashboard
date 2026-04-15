import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FlowState Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fefefe 0%, #f0f4ff 50%, #fef9f0 100%);
}

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8edf5;
}

.portal-hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 20px;
    padding: 48px 56px;
    color: white;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.portal-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,179,237,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.portal-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(246,173,85,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 48px;
    margin: 0 0 10px 0;
    letter-spacing: -1px;
}
.hero-sub {
    font-size: 17px;
    opacity: 0.75;
    font-weight: 300;
}

.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #eef2f7;
    text-align: center;
}
.kpi-label {
    font-size: 13px;
    color: #6b7a99;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 34px;
    color: #1a1a2e;
    line-height: 1;
}

.nav-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 28px 32px;
    border: 1px solid #eef2f7;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: all 0.2s;
    cursor: pointer;
    margin-bottom: 16px;
}
.nav-card:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.10);
    transform: translateY(-2px);
}
.nav-icon { font-size: 28px; margin-bottom: 8px; }
.nav-title { font-size: 17px; font-weight: 600; color: #1a1a2e; margin-bottom: 4px; }
.nav-desc { font-size: 13px; color: #6b7a99; }

.status-pill {
    display: inline-block;
    background: #e8f8f0;
    color: #1e8a4c;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 500;
}

[data-testid="stMetricValue"] { font-family: 'DM Serif Display', serif; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    df["DeliveryDays"] = (df["DeliveryDate"] - df["OrderDate"]).dt.days
    return df

df = load_data()



# Hero
st.markdown("""
<div class="portal-hero">
  <div class="hero-title">FlowState Analytics</div>
  <div class="hero-sub">Smarter Sales Intelligence · Real-time business performance at a glance</div>
</div>
""", unsafe_allow_html=True)

# KPIs
c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("📈 Total Revenue", f"₹{df['TotalPrice'].sum():,.0f}"),
    ("💰 Net Profit", f"₹{df['Profit'].sum():,.0f}"),
    ("🛒 Total Orders", f"{df['OrderID'].nunique():,}"),
    ("📦 Products", f"{df['Product'].nunique()}"),
]
for col, (label, value) in zip([c1, c2, c3, c4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Welcome + nav cards
left, right = st.columns([3, 2])

with left:
    st.markdown("### Welcome to FlowState 👋")
    st.write("""
FlowState is your **central analytics engine** for understanding business performance in real time.

Use the sidebar or cards on the right to navigate between dashboards.
    """)
    st.info(f"📅 Data covers **{df['OrderDate'].min().date()}** to **{df['OrderDate'].max().date()}**  \n🌍 **{df['Region'].nunique()} regions** · **{df['Salesperson'].nunique()} salespersons**")

with right:
    pages = [
        ("📈", "Overview", "Revenue trends, profit & key metrics", "pages/Overview.py"),
        ("📦", "Products", "Product performance & return rates", "pages/Product.py"),
        ("🌎", "Regions", "Regional sales breakdown", "pages/Regions.py"),
        ("🚢", "Shipping", "Delivery times & shipping costs", "pages/Shipping.py"),
    ]
    for icon, title, desc, page in pages:
        st.page_link(page, label=f"{icon} **{title}** — {desc}")