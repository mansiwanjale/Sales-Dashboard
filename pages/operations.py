import streamlit as st
from data_clean import load_data

st.set_page_config(layout="wide")
df = load_data()

st.title("⚙️ Operational Efficiency")
avg_ship = df['ShippingDuration'].mean()
st.metric("Avg Order-to-Ship Time", f"{avg_ship:.2f} Days")

st.subheader("Salesperson Leaderboard")
st.bar_chart(df.groupby('Salesperson')['TotalPrice'].count())