import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pages.style_utils import DAY_STYLE, PALETTE, BG, TEXT, apply_style

st.set_page_config(page_title="Shipping · FlowState", layout="wide")
st.markdown(DAY_STYLE, unsafe_allow_html=True)
apply_style()

# 🎨 Shipping page background (light blue theme)
st.markdown("""
<style>
.stApp {
    background: white;
}

.chart-card {
    padding: 16px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    height: auto !important;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

CHART_SIZE = (9, 4.5)

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    df["DeliveryDays"] = (df["DeliveryDate"] - df["OrderDate"]).dt.days
    df["FastDelivery"] = df["DeliveryDays"] <= 3
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("**Filters**")
    regions = st.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))
    products = st.multiselect("Product", df["Product"].unique(), default=list(df["Product"].unique()))
    date_range = st.date_input("Date Range", [df["OrderDate"].min(), df["OrderDate"].max()])

fdf = df[
    df["Region"].isin(regions) &
    df["Product"].isin(products) &
    (df["OrderDate"] >= pd.to_datetime(date_range[0])) &
    (df["OrderDate"] <= pd.to_datetime(date_range[1]))
]

# Header
st.markdown("""
<div class="page-header">
  <div class="page-title">🚢 Shipping Analytics</div>
  <div class="page-sub">Delivery efficiency, shipping costs, and operational performance metrics</div>
</div>
""", unsafe_allow_html=True)

# KPI cards (light)
c1, c2, c3, c4 = st.columns(4)

fast_pct = fdf["FastDelivery"].mean() * 100

kpis = [
    ("Total Orders", f"{len(fdf):,}"),
    ("Avg Delivery Time", f"{fdf['DeliveryDays'].mean():.2f} days"),
    ("Fast Deliveries (≤3d)", f"{fast_pct:.1f}%"),
    ("Avg Shipping Cost", f"₹{fdf['ShippingCost'].mean():.2f}"),
]

KPI_COLORS = ["#E0F2FE", "#E8F5E9", "#FFF7ED", "#F3E8FF"]

for i, (col, (label, val)) in enumerate(zip([c1, c2, c3, c4], kpis)):
    with col:
        st.markdown(f'''
        <div style="
            background:{KPI_COLORS[i]};
            padding:16px;
            border-radius:12px;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
            <div style="font-size:13px; color:#555;">{label}</div>
            <div style="font-size:22px; font-weight:600; color:#111;">{val}</div>
        </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- ROW 1 ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card"><b>📈 Shipping Cost Trend</b>', unsafe_allow_html=True)

    trend = fdf.groupby("OrderDate")["ShippingCost"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    sns.lineplot(data=trend, x="OrderDate", y="ShippingCost", color=PALETTE[1], ax=ax)
    ax.fill_between(trend["OrderDate"], trend["ShippingCost"], alpha=0.1, color=PALETTE[1])

    ax.set_ylabel("Shipping Cost (₹)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><b>📦 Delivery Days Distribution</b>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=CHART_SIZE)

    sns.histplot(data=fdf, x="DeliveryDays", kde=True, color=PALETTE[0], bins=15, ax=ax)
    ax.axvline(3, color=PALETTE[1], linestyle="--")

    ax.set_xlabel("Delivery Days")
    ax.set_ylabel("Orders")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><b>🚚 Avg Delivery Time by Region</b>', unsafe_allow_html=True)

    delay = fdf.groupby("Region")["DeliveryDays"].mean().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.bar(delay["Region"], delay["DeliveryDays"], color=PALETTE[:len(delay)])

    for bar, val in zip(bars, delay["DeliveryDays"]):
        ax.text(bar.get_x() + bar.get_width()/2, val, f"{val:.1f}d", ha="center")

    ax.set_ylabel("Avg Days")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><b>💰 Shipping Cost by Product</b>', unsafe_allow_html=True)

    cp = fdf.groupby("Product")["ShippingCost"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.barh(cp["Product"], cp["ShippingCost"], color=PALETTE[2])

    for bar, val in zip(bars, cp["ShippingCost"]):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f"₹{val:,.0f}", va="center")

    ax.set_xlabel("Shipping Cost")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 3 ----------
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="chart-card"><b>💳 Payment Method Mix</b>', unsafe_allow_html=True)

    pay = fdf["PaymentMethod"].value_counts().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    ax.pie(pay["count"], labels=pay["PaymentMethod"], autopct="%1.1f%%", colors=PALETTE[:len(pay)])

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card"><b>🏆 Top Salespersons</b>', unsafe_allow_html=True)

    sp = fdf["Salesperson"].value_counts().reset_index().head(10)
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.barh(sp["Salesperson"], sp["count"], color=PALETTE[3])

    for bar, val in zip(bars, sp["count"]):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, str(val), va="center")

    ax.set_xlabel("Orders")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RETURN RATE ----------
st.markdown('<div class="chart-card"><b>🔄 Return Rate by Product</b>', unsafe_allow_html=True)

if "Returned" in fdf.columns:
    ret = fdf.groupby("Product").agg(
        TotalOrders=("Returned","count"),
        TotalReturned=("Returned","sum")
    ).reset_index()

    ret["ReturnRate (%)"] = (ret["TotalReturned"] / ret["TotalOrders"] * 100).round(2)

    fig, ax = plt.subplots(figsize=(10, 4))

    bars = ax.bar(ret["Product"], ret["ReturnRate (%)"], color=PALETTE[1])

    ax.set_ylabel("Return Rate (%)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=25)

    st.pyplot(fig)
    st.dataframe(ret, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Raw data
with st.expander("📄 View Raw Data"):
    st.dataframe(fdf, use_container_width=True)