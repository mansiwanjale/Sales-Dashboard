import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pages.style_utils import DAY_STYLE, PALETTE, BG, TEXT, apply_style

st.set_page_config(page_title="Products · FlowState", layout="wide")
st.markdown(DAY_STYLE, unsafe_allow_html=True)
apply_style()

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    df["ProfitMargin"] = df["Profit"] / df["TotalPrice"]
    return df

df = load_data()

with st.sidebar:
    st.markdown("**Filters**")
    products = st.multiselect("Product", df["Product"].unique(), default=list(df["Product"].unique()))
    date_range = st.date_input("Date Range", [df["OrderDate"].min(), df["OrderDate"].max()])

fdf = df[
    df["Product"].isin(products) &
    (df["OrderDate"] >= pd.to_datetime(date_range[0])) &
    (df["OrderDate"] <= pd.to_datetime(date_range[1]))
]

st.markdown("""
<div class="page-header">
  <div class="page-title">📦 Product Performance</div>
  <div class="page-sub">Deep dive into product revenue, profitability, heatmaps, and return rates</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("Products", f"{fdf['Product'].nunique()}"),
    ("Total Revenue", f"₹{fdf['TotalPrice'].sum():,.0f}"),
    ("Avg Margin", f"{fdf['ProfitMargin'].mean()*100:.1f}%"),
    ("Total Units", f"{fdf['Quantity'].sum():,.0f}"),
]
for col, (label, val) in zip([c1, c2, c3, c4], kpis):
    with col:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Row 1: Top products bar + Revenue trend
col1, col2 = st.columns([5, 5])

with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">🏆 Top Products by Revenue</div>', unsafe_allow_html=True)
    top = fdf.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(top["Product"], top["TotalPrice"], color=PALETTE[:len(top)], edgecolor="none")
    for bar, val in zip(bars, top["TotalPrice"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + top["TotalPrice"].max()*0.01,
                f"₹{val/1000:.0f}K", ha="center", fontsize=8)
    ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.set_xlabel("")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">📈 Revenue Trend Over Time</div>', unsafe_allow_html=True)
    trend = fdf.groupby("OrderDate")["TotalPrice"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(data=trend, x="OrderDate", y="TotalPrice", color=PALETTE[0], linewidth=2, ax=ax)
    ax.fill_between(trend["OrderDate"], trend["TotalPrice"], alpha=0.1, color=PALETTE[0])
    ax.set_xlabel("")
    ax.set_ylabel("Revenue (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Heatmap Region x Product
st.markdown('<div class="chart-card"><div class="chart-title">🗺️ Region × Product Revenue Heatmap</div>', unsafe_allow_html=True)
if "Region" in fdf.columns:
    heat = fdf.pivot_table(index="Region", columns="Product", values="TotalPrice", aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=(14, max(3, len(heat)*0.8)))
    sns.heatmap(
        heat, annot=True, fmt=".0f", cmap="Blues",
        linewidths=0.5, linecolor="#eef2f7",
        ax=ax, cbar_kws={"shrink": 0.6},
        annot_kws={"size": 8}
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=30, ha="right", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
st.markdown('</div>', unsafe_allow_html=True)

# Row 3: Payment Method + Return Rate
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">💳 Revenue by Payment Method</div>', unsafe_allow_html=True)
    if "PaymentMethod" in fdf.columns:
        pm = fdf.groupby("PaymentMethod")["TotalPrice"].sum().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots(figsize=(7, 3.8))
        bars = ax.bar(pm["PaymentMethod"], pm["TotalPrice"], color=PALETTE[:len(pm)], edgecolor="none")
        for bar, val in zip(bars, pm["TotalPrice"]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + pm["TotalPrice"].max()*0.01,
                    f"₹{val/1000:.0f}K", ha="center", fontsize=9)
        ax.set_ylabel("Revenue (₹)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}K"))
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">🔄 Return Rate by Product</div>', unsafe_allow_html=True)
    if "Returned" in fdf.columns:
        ret = fdf.groupby("Product").agg(Total=("Returned","count"), Returned=("Returned","sum")).reset_index()
        ret["ReturnRate"] = ret["Returned"] / ret["Total"] * 100
        avg_rate = ret["ReturnRate"].mean()
        ret = ret.sort_values("ReturnRate", ascending=False)
        fig, ax = plt.subplots(figsize=(7, 3.8))
        colors = [PALETTE[1] if r > avg_rate else PALETTE[2] for r in ret["ReturnRate"]]
        bars = ax.bar(ret["Product"], ret["ReturnRate"], color=colors, edgecolor="none")
        ax.axhline(avg_rate, color=PALETTE[0], linestyle="--", linewidth=1.5, label=f"Avg {avg_rate:.1f}%")
        ax.legend(fontsize=9)
        for bar, val in zip(bars, ret["ReturnRate"]):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f"{val:.1f}%", ha="center", fontsize=8)
        ax.set_ylabel("Return Rate (%)")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        plt.xticks(rotation=30, ha="right", fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

# Profitability table
st.markdown('<div class="chart-card"><div class="chart-title">📋 Detailed Product Profitability Report</div>', unsafe_allow_html=True)
prof = fdf.groupby("Product").agg(
    TotalRevenue=("TotalPrice", "sum"),
    TotalProfit=("Profit", "sum"),
    AvgMargin=("ProfitMargin", "mean"),
    Orders=("OrderID", "count"),
    Units=("Quantity", "sum")
).reset_index()
prof["AvgMargin"] = (prof["AvgMargin"] * 100).round(2).astype(str) + "%"
prof["TotalRevenue"] = prof["TotalRevenue"].map("₹{:,.0f}".format)
prof["TotalProfit"] = prof["TotalProfit"].map("₹{:,.0f}".format)
st.dataframe(prof.rename(columns={"TotalRevenue":"Revenue","TotalProfit":"Profit","AvgMargin":"Avg Margin","Orders":"Orders","Units":"Units"}), use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
