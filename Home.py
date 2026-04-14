import streamlit as st
import pandas as pd

st.sidebar.title(" FlowState Portal")
st.sidebar.image("flowstate.png", width=220)

# Page config
st.set_page_config(
    page_title="FlowState Analytics Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    return df

df = load_data()






# ---------------- MAIN HOME ---------------- #

st.title("FlowState Analytics Portal")
st.markdown("### Smarter Sales Intelligence Starts Here")
st.markdown("---")

# Top REAL metrics
col1, col2, col3, col4 = st.columns(4)

total_sales = df["TotalPrice"].sum()
total_orders = df["OrderID"].nunique()
total_products = df["Product"].nunique()
regions = df["Region"].nunique()

col1.metric("📈 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("🛒 Orders", f"{total_orders:,}")
col3.metric("📦 Products", f"{total_products}")
col4.metric("🌍 Regions", f"{regions}")

st.markdown("---")

# Layout
left, right = st.columns([2, 1])

with left:
    st.header("Welcome to FlowState 👋")
    st.write("""
    FlowState is your **central analytics engine** for understanding business performance in real time.

    🔍 Track sales trends across regions  
    💰 Analyze product profitability  
    📦 Monitor operational efficiency  
    ⚡ Make faster, data-driven decisions  

    Everything you need — in one clean dashboard.
    """)

    st.markdown("###  Get Started")

    if st.button("Go to Dashboard"):
        st.switch_page("pages/overview.py")

with right:
    st.image("flowstate.png", width=220)

    st.markdown("### 🟢 System Status")
    st.success("All Systems Operational")

    st.markdown("### 🕒 Last Data Update")
    st.info(f"{df['OrderDate'].max().date()}")

st.markdown("---")

st.caption("FlowState Analytics © 2026 | Built for performance insights")