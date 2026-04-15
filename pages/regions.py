import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pages.style_utils import DAY_STYLE, PALETTE, BG, TEXT, apply_style

st.set_page_config(page_title="Regions · FlowState", layout="wide")
st.markdown(DAY_STYLE, unsafe_allow_html=True)
apply_style()

# ✅ Force clean white background + fix card spacing
st.markdown("""
<style>
body, .stApp {
    background-color: white !important;
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

# ✅ Standard bigger size
CHART_SIZE = (9, 4.5)

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    df["ProfitMargin"] = df["Profit"] / df["TotalPrice"]
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("**Filters**")
    regions = st.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))
    date_range = st.date_input("Date Range", [df["OrderDate"].min(), df["OrderDate"].max()])

fdf = df[
    df["Region"].isin(regions) &
    (df["OrderDate"] >= pd.to_datetime(date_range[0])) &
    (df["OrderDate"] <= pd.to_datetime(date_range[1]))
]

# Header
st.markdown("""
<div class="page-header">
  <div class="page-title">🌎 Regional Performance</div>
  <div class="page-sub">Sales breakdown by region, manager performance, and regional trends</div>
</div>
""", unsafe_allow_html=True)

# KPI cards (light)
c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("Total Revenue", f"₹{fdf['TotalPrice'].sum():,.0f}"),
    ("Total Profit", f"₹{fdf['Profit'].sum():,.0f}"),
    ("Regions", f"{fdf['Region'].nunique()}"),
    ("Avg Margin", f"{fdf['ProfitMargin'].mean()*100:.1f}%"),
]

KPI_COLORS = ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5"]

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
    st.markdown('<div class="chart-card"><b>📊 Sales Share by Region</b>', unsafe_allow_html=True)

    reg_sales = fdf.groupby("Region")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    wedges, texts, autotexts = ax.pie(
        reg_sales["TotalPrice"],
        labels=reg_sales["Region"],
        autopct="%1.1f%%",
        colors=PALETTE[:len(reg_sales)],
        wedgeprops=dict(width=0.5)
    )

    for at in autotexts:
        at.set_color("white")

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><b>🏆 Revenue by Region</b>', unsafe_allow_html=True)

    reg_bar = fdf.groupby("Region")["TotalPrice"].sum().sort_values().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.barh(reg_bar["Region"], reg_bar["TotalPrice"], color=PALETTE[:len(reg_bar)])

    for bar, val in zip(bars, reg_bar["TotalPrice"]):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f"₹{val:,.0f}", va="center")

    ax.set_xlabel("Revenue")
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><b>📈 Monthly Revenue by Region</b>', unsafe_allow_html=True)

    trend = fdf.groupby(["Month", "Region"])["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    for i, region in enumerate(trend["Region"].unique()):
        rdf = trend[trend["Region"] == region]
        ax.plot(rdf["Month"], rdf["TotalPrice"], label=region)

    ax.set_ylabel("Revenue")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><b>👤 Region Manager Performance</b>', unsafe_allow_html=True)

    mgr = fdf.groupby("RegionManager")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.barh(mgr["RegionManager"], mgr["TotalPrice"], color=PALETTE[2])

    for bar, val in zip(bars, mgr["TotalPrice"]):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f"₹{val/1000:.0f}K", va="center")

    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- HEATMAP ----------
st.markdown('<div class="chart-card"><b>🗺️ Product Mix by Region</b>', unsafe_allow_html=True)

heat = fdf.pivot_table(index="Region", columns="Product", values="TotalPrice", aggfunc="sum", fill_value=0)
fig, ax = plt.subplots(figsize=(12, 4))

sns.heatmap(heat, annot=True, fmt=".0f", cmap="Blues", ax=ax)

st.pyplot(fig)
plt.close()
st.markdown('</div>', unsafe_allow_html=True)

# ---------- SUMMARY ----------
st.markdown('<div class="chart-card"><b>📋 Regional Summary</b>', unsafe_allow_html=True)

summary = fdf.groupby("Region").agg(
    Revenue=("TotalPrice","sum"),
    Profit=("Profit","sum"),
    Orders=("OrderID","count"),
    AvgMargin=("ProfitMargin","mean"),
    Customers=("CustomerName","nunique")
).reset_index()

summary["Revenue"] = summary["Revenue"].map("₹{:,.0f}".format)
summary["Profit"] = summary["Profit"].map("₹{:,.0f}".format)
summary["AvgMargin"] = (summary["AvgMargin"]*100).round(1).astype(str) + "%"

st.dataframe(summary, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)