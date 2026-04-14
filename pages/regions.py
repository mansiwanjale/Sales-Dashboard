import streamlit as st
import plotly.express as px
from data_clean import load_data

st.set_page_config(layout="wide")
df = load_data()

st.title("🌎 Regional Performance")
reg_sales = df.groupby('Region')['TotalPrice'].sum().reset_index()
fig_reg = px.pie(reg_sales, values='TotalPrice', names='Region', hole=0.4, title="Sales Share by Region")
st.plotly_chart(fig_reg, use_container_width=True)

st.subheader("Regional Manager Performance")
st.bar_chart(df.groupby('RegionManager')['TotalPrice'].sum())