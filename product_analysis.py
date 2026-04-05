import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Product Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("Product-Sales-Region.xlsx")

df.columns = df.columns.str.strip()

# Convert dates
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# -----------------------------
# TITLE
# -----------------------------
st.title("📦 Product Performance Dashboard")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

products = st.sidebar.multiselect(
    "Select Product(s)",
    df['Product'].unique(),
    default=df['Product'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['OrderDate'].min(), df['OrderDate'].max()]
)

# Filter data
filtered_df = df[
    (df['Product'].isin(products)) &
    (df['OrderDate'] >= pd.to_datetime(date_range[0])) &
    (df['OrderDate'] <= pd.to_datetime(date_range[1]))
]

st.write(f"### Showing data for: {', '.join(products)}")

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['TotalPrice'].sum()
total_orders = len(filtered_df)
avg_order_value = filtered_df['TotalPrice'].mean()
total_quantity = filtered_df['Quantity'].sum()

col1.metric("💰 Revenue", f"{total_revenue:,.0f}")
col2.metric("📦 Orders", total_orders)
col3.metric("📈 Avg Order Value", f"{avg_order_value:.2f}")
col4.metric("📊 Quantity Sold", total_quantity)

# -----------------------------
# SALES TREND
# -----------------------------
st.subheader("📈 Revenue Trend Over Time")

trend = filtered_df.groupby('OrderDate')['TotalPrice'].sum()
st.line_chart(trend)

# -----------------------------
# TOP PRODUCTS (MAIN CHART)
# -----------------------------
st.subheader("🏆 Top Performing Products")

top_products = filtered_df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
top_products.plot(kind='bar', ax=ax)
ax.set_ylabel("Revenue")
st.pyplot(fig)

# -----------------------------
# QUANTITY vs REVENUE
# -----------------------------
st.subheader("📊 Quantity vs Revenue Insight")

product_summary = filtered_df.groupby('Product').agg({
    'TotalPrice': 'sum',
    'Quantity': 'sum'
})

fig, ax = plt.subplots()
ax.scatter(product_summary['Quantity'], product_summary['TotalPrice'])

for i, txt in enumerate(product_summary.index):
    ax.annotate(txt, (product_summary['Quantity'][i], product_summary['TotalPrice'][i]))

ax.set_xlabel("Quantity Sold")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# -----------------------------
# DISCOUNT IMPACT ANALYSIS
# -----------------------------
st.subheader("💸 Discount Impact on Revenue")

fig, ax = plt.subplots()
ax.scatter(filtered_df['Discount'], filtered_df['TotalPrice'])
ax.set_xlabel("Discount")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("🧠 Business Insights")

best_product = filtered_df.groupby('Product')['TotalPrice'].sum().idxmax()
worst_product = filtered_df.groupby('Product')['TotalPrice'].sum().idxmin()

st.write(f"🏆 Best Performing Product: {best_product}")
st.write(f"⚠️ Lowest Performing Product: {worst_product}")

# Smart insights
if total_quantity > 1000:
    st.write("📈 High demand observed across selected products")

if avg_order_value < df['TotalPrice'].mean():
    st.write("💰 Average order value is below overall average")

st.write("📌 Recommendation:")
st.write("- Focus on high-revenue products")
st.write("- Optimize pricing and discount strategies")
st.write("- Increase sales volume for low-performing products")