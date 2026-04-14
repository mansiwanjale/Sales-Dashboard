import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< HEAD

# PAGE CONFIG
st.set_page_config(page_title="Product Dashboard", layout="wide")

# LOAD DATA
df = pd.read_excel("Product-Sales-Region.xlsx")
df.columns = df.columns.str.strip()
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# TITLE
st.title("📦 Product Performance Dashboard")

# SIDEBAR FILTERS
=======
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
>>>>>>> 4213a7ee8f302673c4901ea05696ed64bff8138d
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

<<<<<<< HEAD
=======
# Filter data
>>>>>>> 4213a7ee8f302673c4901ea05696ed64bff8138d
filtered_df = df[
    (df['Product'].isin(products)) &
    (df['OrderDate'] >= pd.to_datetime(date_range[0])) &
    (df['OrderDate'] <= pd.to_datetime(date_range[1]))
]

st.write(f"### Showing data for: {', '.join(products)}")

# -----------------------------
<<<<<<< HEAD
# 1. REVENUE TREND OVER TIME
=======
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
>>>>>>> 4213a7ee8f302673c4901ea05696ed64bff8138d
# -----------------------------
st.subheader("📈 Revenue Trend Over Time")

trend = filtered_df.groupby('OrderDate')['TotalPrice'].sum()
st.line_chart(trend)

# -----------------------------
<<<<<<< HEAD
# 2. TOP PERFORMING PRODUCTS
=======
# TOP PRODUCTS (MAIN CHART)
>>>>>>> 4213a7ee8f302673c4901ea05696ed64bff8138d
# -----------------------------
st.subheader("🏆 Top Performing Products")

top_products = filtered_df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)

<<<<<<< HEAD
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(top_products.index, top_products.values, color='steelblue')
ax.set_xlabel("Product")
ax.set_ylabel("Revenue")
ax.set_title("Top Performing Products")
plt.xticks(rotation=30, ha='right')

for bar, val in zip(bars, top_products.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + top_products.values.max() * 0.01,
            f"{val:,.0f}", ha='center', fontsize=9)

plt.tight_layout()
st.pyplot(fig)

# -----------------------------
# 3. REVENUE BY PRODUCT - HORIZONTAL BAR
# -----------------------------
st.subheader("📊 Revenue by Product (Horizontal Bar)")

rev_by_product = filtered_df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(rev_by_product.index, rev_by_product.values, color='darkcyan')
ax.set_xlabel("Revenue")
ax.set_ylabel("Product")
ax.set_title("Revenue by Product")

for bar, val in zip(bars, rev_by_product.values):
    ax.text(bar.get_width() + rev_by_product.values.max() * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,.0f}", va='center', fontsize=9)

plt.tight_layout()
st.pyplot(fig)

# -----------------------------
# 4. REGION x PRODUCT HEATMAP
# -----------------------------
st.subheader("🗺️ Region × Product Revenue Heatmap")

if 'Region' in filtered_df.columns:
    heatmap_data = filtered_df.pivot_table(
        index='Region',
        columns='Product',
        values='TotalPrice',
        aggfunc='sum',
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(heatmap_data.values, aspect='auto', cmap='YlOrRd')

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(heatmap_data.index, fontsize=9)
    ax.set_title("Revenue Heatmap: Region × Product")
    plt.colorbar(im, ax=ax, label="Revenue")

    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            ax.text(j, i, f"{heatmap_data.values[i, j]:,.0f}",
                    ha='center', va='center', fontsize=7, color='black')

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("⚠️ 'Region' column not found in data.")

# -----------------------------
# 5. PAYMENT METHOD ANALYSIS
# -----------------------------
st.subheader("💳 Payment Method Analysis")

if 'PaymentMethod' in filtered_df.columns:
    payment_revenue = filtered_df.groupby('PaymentMethod')['TotalPrice'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(payment_revenue.index, payment_revenue.values,
                  color=['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2'])
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue by Payment Method")
    plt.xticks(rotation=30, ha='right')

    for bar, val in zip(bars, payment_revenue.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + payment_revenue.values.max() * 0.01,
                f"{val:,.0f}", ha='center', fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("⚠️ 'PaymentMethod' column not found in data.")

# -----------------------------
# 6. RETURN RATE BY PRODUCT
# -----------------------------
st.subheader("🔄 Return Rate by Product")

if 'Returned' in filtered_df.columns:
    return_data = filtered_df.groupby('Product').agg(
        TotalOrders=('Returned', 'count'),
        TotalReturned=('Returned', 'sum')
    )
    return_data['ReturnRate(%)'] = (
        return_data['TotalReturned'] / return_data['TotalOrders'] * 100
    ).round(2)
    return_data = return_data.sort_values('ReturnRate(%)', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(
        return_data.index,
        return_data['ReturnRate(%)'],
        color=['#d9534f' if r > 20 else '#5cb85c' for r in return_data['ReturnRate(%)']]
    )
    ax.set_xlabel("Product")
    ax.set_ylabel("Return Rate (%)")
    ax.set_title("Return Rate by Product")
    ax.axhline(
        y=return_data['ReturnRate(%)'].mean(),
        color='orange', linestyle='--',
        label=f"Avg: {return_data['ReturnRate(%)'].mean():.1f}%"
    )
    ax.legend()
    plt.xticks(rotation=30, ha='right')

    for bar, val in zip(bars, return_data['ReturnRate(%)']):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{val}%", ha='center', fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(return_data.reset_index())
else:
    st.warning("⚠️ 'Returned' column not found in data.")
=======
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
>>>>>>> 4213a7ee8f302673c4901ea05696ed64bff8138d
