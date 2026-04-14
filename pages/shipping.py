import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Shipping Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv")
    df.columns = df.columns.str.strip()

    # Convert dates
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    df["DeliveryDate"] = pd.to_datetime(df["DeliveryDate"])

    # Create Delivery Days (IMPORTANT)
    df["DeliveryDays"] = (df["DeliveryDate"] - df["OrderDate"]).dt.days

    return df

df = load_data()

# ---------------- TITLE ----------------
st.title("🚢 Shipping Analytics Dashboard")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

products = st.sidebar.multiselect(
    "Select Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["OrderDate"].min(), df["OrderDate"].max()]
)

# ---------------- FILTER ----------------
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Product"].isin(products)) &
    (df["OrderDate"] >= pd.to_datetime(date_range[0])) &
    (df["OrderDate"] <= pd.to_datetime(date_range[1]))
]

# ---------------- KPI ----------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Total Revenue", f"₹{filtered_df['TotalPrice'].sum():,.0f}")
col3.metric("Avg Delivery Time", f"{filtered_df['DeliveryDays'].mean():.2f} Days")
col4.metric("Avg Shipping Cost", f"₹{filtered_df['ShippingCost'].mean():.2f}")

# ---------------- 1. SHIPPING COST TREND ----------------
st.subheader("📈 Shipping Cost Trend")

trend = filtered_df.groupby("OrderDate")["ShippingCost"].sum()
st.line_chart(trend)

# ---------------- 2. DELIVERY TIME BY REGION ----------------
st.subheader("🚚 Delivery Time by Region")

delay_region = filtered_df.groupby("Region")["DeliveryDays"].mean()

fig, ax = plt.subplots()
ax.bar(delay_region.index, delay_region.values)
ax.set_ylabel("Days")
ax.set_title("Average Delivery Time by Region")

for i, v in enumerate(delay_region.values):
    ax.text(i, v, f"{v:.1f}", ha='center')

st.pyplot(fig)

# ---------------- 3. SHIPPING COST BY PRODUCT ----------------
st.subheader("📦 Shipping Cost by Product")

cost_product = filtered_df.groupby("Product")["ShippingCost"].sum().sort_values()

fig, ax = plt.subplots()
ax.barh(cost_product.index, cost_product.values)
ax.set_title("Shipping Cost Distribution")

st.pyplot(fig)

# ---------------- 4. PAYMENT ANALYSIS ----------------
st.subheader("💳 Payment Method Distribution")

payment = filtered_df["PaymentMethod"].value_counts()

fig, ax = plt.subplots()
ax.pie(payment.values, labels=payment.index, autopct="%1.1f%%")

st.pyplot(fig)

# ---------------- 5. RETURN RATE ----------------
st.subheader("🔄 Return Rate Analysis")

return_data = filtered_df.groupby("Product").agg(
    total=("Returned", "count"),
    returned=("Returned", "sum")
)

return_data["ReturnRate (%)"] = (
    return_data["returned"] / return_data["total"] * 100
)

fig, ax = plt.subplots()
ax.bar(return_data.index, return_data["ReturnRate (%)"])
ax.set_ylabel("%")
ax.set_title("Return Rate by Product")

for i, v in enumerate(return_data["ReturnRate (%)"]):
    ax.text(i, v, f"{v:.1f}%", ha='center')

st.pyplot(fig)
st.dataframe(return_data)

# ---------------- BONUS (VERY IMPRESSIVE) ----------------
st.subheader("🏆 Top Salespersons (Order Count)")

sales_data = filtered_df["Salesperson"].value_counts()

st.bar_chart(sales_data)

# ---------------- RAW DATA ----------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df)
