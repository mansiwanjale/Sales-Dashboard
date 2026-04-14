import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Executive Sales Dashboard", layout="wide")

# Custom styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    path = "C:/Users/Admin/Desktop/BTech/TY Btech Sem 6/Assignments/DE/Product_Sales/Sales-Dashboard/Product_Sales.csv"
    df = pd.read_csv(path, parse_dates=["OrderDate", "DeliveryDate"])

    # Calculations
    df["Profit"] = df["TotalPrice"] * 0.2
    df["ProfitMargin"] = df["Profit"] / df["TotalPrice"]

    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[df["Region"].isin(region_filter)]

# --- HEADER ---
st.title("📊 Business Intelligence Overview")
st.markdown("Real-time analysis of sales performance and product metrics.")

# Metrics
m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Revenue", f"₹{filtered_df['TotalPrice'].sum():,.0f}")
m2.metric("Net Profit", f"₹{filtered_df['Profit'].sum():,.0f}")
m3.metric("Total Orders", f"{filtered_df['OrderID'].nunique():,}")
m4.metric("Avg Margin", f"{filtered_df['ProfitMargin'].mean()*100:.1f}%")

st.markdown("---")

# --- ROW 1 ---
row1_1, row1_2 = st.columns((6, 4))

with row1_1:
    st.subheader("📈 Monthly Revenue Trend")

    sales_trend = filtered_df.groupby(
        filtered_df['OrderDate'].dt.to_period('M')
    )['TotalPrice'].sum().reset_index()

    sales_trend['OrderDate'] = sales_trend['OrderDate'].astype(str)

    fig_line = px.area(
        sales_trend,
        x='OrderDate',
        y='TotalPrice'
    )

    st.plotly_chart(fig_line, use_container_width=True)

with row1_2:
    st.subheader("🎯 Profit Distribution")

    fig_sns, ax = plt.subplots()
    sns.kdeplot(data=filtered_df, x="Profit", fill=True, ax=ax)
    sns.despine()

    st.pyplot(fig_sns)

# --- ROW 2 ---
row2_1, row2_2 = st.columns(2)

with row2_1:
    st.subheader("📦 Top Products by Revenue")

    top_prods = filtered_df.groupby("Product")["TotalPrice"].sum().nlargest(10).reset_index()

    fig_bar = px.bar(
        top_prods,
        x="TotalPrice",
        y="Product",
        orientation='h'
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with row2_2:
    st.subheader("🗺️ Sales by Region")

    region_sales = filtered_df.groupby("Region")["TotalPrice"].sum().reset_index()

    fig_pie = px.pie(
        region_sales,
        values="TotalPrice",
        names="Region",
        hole=0.4
    )

    st.plotly_chart(fig_pie, use_container_width=True)