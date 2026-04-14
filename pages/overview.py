import streamlit as st
import plotly.express as px
from data_clean import load_data

st.set_page_config(layout="wide")
df = load_data()

st.title("📊 Business Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['TotalPrice'].sum():,.1f}K")
col2.metric("Total Profit", f"${df['Profit'].sum():,.1f}K")
col3.metric("Total Orders", f"{df['OrderID'].nunique():,}")
col4.metric("Avg Profit Margin", f"{df['ProfitMargin'].mean()*100:.2f}%")

st.subheader("Total Sales Trend")
sales_trend = df.groupby(df['OrderDate'].dt.to_period('M'))['TotalPrice'].sum().reset_index()
sales_trend['OrderDate'] = sales_trend['OrderDate'].astype(str)
fig = px.line(sales_trend, x='OrderDate', y='TotalPrice', template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)