import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pages.style_utils import DAY_STYLE, PALETTE, BG, TEXT, apply_style

st.set_page_config(page_title="Overview · FlowState", layout="wide")
st.markdown(DAY_STYLE, unsafe_allow_html=True)
apply_style()

# 🔥 Fix chart-card spacing issue completely
st.markdown("""
<style>
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

# ✅ Bigger consistent chart size
CHART_SIZE = (9, 4.5)

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    df["ProfitMargin"] = df["Profit"] / df["TotalPrice"]
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    df["Year"] = df["OrderDate"].dt.year
    return df

df = load_data()

# Sidebar filters
with st.sidebar:
    st.markdown("**Filters**")
    regions = st.multiselect("Region", df["Region"].unique(), default=list(df["Region"].unique()))
    years = st.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

fdf = df[df["Region"].isin(regions) & df["Year"].isin(years)]

# Header
st.markdown("""
<div class="page-header">
  <div class="page-title">📈 Business Overview</div>
  <div class="page-sub">Real-time analysis of sales performance, revenue trends, and profit metrics</div>
</div>
""", unsafe_allow_html=True)

# KPI cards
c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("Total Revenue", f"₹{fdf['TotalPrice'].sum():,.0f}"),
    ("Net Profit", f"₹{fdf['Profit'].sum():,.0f}"),
    ("Total Orders", f"{fdf['OrderID'].nunique():,}"),
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
    st.markdown('<div class="chart-card"><b>📈 Monthly Revenue Trend</b>', unsafe_allow_html=True)

    trend = fdf.groupby("Month")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    sns.lineplot(data=trend, x="Month", y="TotalPrice", color=PALETTE[0], linewidth=2.5, ax=ax)
    ax.fill_between(trend["Month"], trend["TotalPrice"], alpha=0.12, color=PALETTE[0])

    ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    plt.xticks(rotation=35)

    ax.grid(axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><b>🎯 Profit Distribution</b>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=CHART_SIZE)

    sns.kdeplot(data=fdf, x="Profit", fill=True, color=PALETTE[1], alpha=0.6, linewidth=2, ax=ax)

    ax.set_xlabel("Profit (₹)")
    ax.set_ylabel("Density")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><b>📦 Top Products by Revenue</b>', unsafe_allow_html=True)

    top = fdf.groupby("Product")["TotalPrice"].sum().nlargest(10).reset_index().sort_values("TotalPrice")
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.barh(top["Product"], top["TotalPrice"], color=PALETTE[0])

    for bar, val in zip(bars, top["TotalPrice"]):
        ax.text(bar.get_width() + top["TotalPrice"].max()*0.01,
                bar.get_y() + bar.get_height()/2,
                f"₹{val:,.0f}", va="center", fontsize=8)

    ax.set_xlabel("Revenue (₹)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><b>🗺️ Revenue by Region</b>', unsafe_allow_html=True)

    reg = fdf.groupby("Region")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    wedges, texts, autotexts = ax.pie(
        reg["TotalPrice"],
        labels=reg["Region"],
        autopct="%1.1f%%",
        colors=PALETTE[:len(reg)],
        wedgeprops=dict(width=0.5),
        pctdistance=0.75
    )

    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(9)

    ax.set_facecolor(BG)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 3 ----------
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="chart-card"><b>📊 Revenue by Year</b>', unsafe_allow_html=True)

    yr = fdf.groupby("Year")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    bars = ax.bar(yr["Year"].astype(str), yr["TotalPrice"], color=PALETTE[2])

    for bar, val in zip(bars, yr["TotalPrice"]):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + yr["TotalPrice"].max()*0.01,
                f"₹{val/1000:.0f}K", ha="center", fontsize=9)

    ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card"><b>🏅 Top Salesperson Revenue</b>', unsafe_allow_html=True)

    sp = fdf.groupby("Salesperson")["TotalPrice"].sum().nlargest(8).reset_index()
    fig, ax = plt.subplots(figsize=CHART_SIZE)

    sns.barplot(data=sp, x="Salesperson", y="TotalPrice", palette=PALETTE[:len(sp)], ax=ax)

    ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30)

    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)