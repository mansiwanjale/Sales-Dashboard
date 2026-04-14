import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Regional Analytics", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv")
    df.columns = df.columns.str.strip()
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df

df = load_data()

st.title("🌎 Regional & Managerial Insights")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")
selected_regions = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
selected_managers = st.sidebar.multiselect("Select Manager", df['RegionManager'].unique(), default=df['RegionManager'].unique())

mask = (df['Region'].isin(selected_regions)) & (df['RegionManager'].isin(selected_managers))
f_df = df[mask]

# ---------------- KPI ROW ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"₹{f_df['TotalPrice'].sum():,.0f}")
col2.metric("Avg Discount", f"{f_df['Discount'].mean():.1f}%")
col3.metric("Top Manager", f_df.groupby('RegionManager')['TotalPrice'].sum().idxmax())
col4.metric("Active Stores", f_df['StoreLocation'].nunique())

st.markdown("---")

# ---------------- 1. MANAGER PERFORMANCE ----------------
st.subheader("🏆 Sales by Region Manager")
man_perf = f_df.groupby('RegionManager')['TotalPrice'].sum().sort_values()

fig, ax = plt.subplots(figsize=(8, 3)) 
ax.barh(man_perf.index, man_perf.values, color='#69b3a2')
ax.set_xlabel("Total Revenue (₹)")
ax.set_ylabel("Region Manager")
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
st.pyplot(fig)

# ---------------------------------------------------------
# 2 & 3. CUSTOMER TYPE & STORE LOCATIONS (Side-by-Side)
# ---------------------------------------------------------
st.markdown("---")

# Create two columns
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("👥 Revenue by Customer Type")
    cust_data = f_df.groupby('CustomerType')['TotalPrice'].sum()
    
    # Square-ish size works best for Pie inside a column
    fig2, ax2 = plt.subplots(figsize=(4, 3)) 
    ax2.pie(
        cust_data, 
        labels=cust_data.index, 
        autopct='%1.1f%%', 
        colors=['#ff9999','#66b3ff'], 
        startangle=90,
        textprops={'fontsize': 8} # Small but readable
    )
    st.pyplot(fig2)

with col_right:
    st.subheader("📍 Top Store Locations")
    loc_data = f_df.groupby('StoreLocation')['TotalPrice'].sum().nlargest(5) # Top 5 for better fit
    
    fig3, ax3 = plt.subplots(figsize=(4, 3)) 
    ax3.bar(loc_data.index, loc_data.values, color='#4C72B0')
    
    # Proper Labels
    ax3.set_ylabel("Revenue (₹)", fontsize=8)
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Smaller text for the X-axis names
    plt.xticks(rotation=45, ha='right', fontsize=7)
    plt.yticks(fontsize=7)
    
    plt.tight_layout()
    st.pyplot(fig3)
    
# ---------------- 4. REGIONAL REVENUE HEATMAP ----------------
st.markdown("---")
st.subheader("🌡️ Regional Revenue Intensity")
heatmap_data = f_df.pivot_table(index='Region', columns='CustomerType', values='TotalPrice', aggfunc='sum')

fig4, ax4 = plt.subplots(figsize=(5, 3)) # Standardized Size
im = ax4.imshow(heatmap_data, cmap="YlGnBu", aspect='auto')
ax4.set_xticks(range(len(heatmap_data.columns)))
ax4.set_yticks(range(len(heatmap_data.index)))
ax4.set_xticklabels(heatmap_data.columns)
ax4.set_yticklabels(heatmap_data.index)
ax4.set_xlabel("Customer Category")
ax4.set_ylabel("Region")
plt.colorbar(im, label="Revenue (₹)")
st.pyplot(fig4)

# ---------------- 5. PROMOTION EFFECTIVENESS ----------------
st.markdown("---")
st.subheader("🎁 Promotion Effectiveness")
if 'Promotion' in f_df.columns:
    promo_data = f_df.groupby('Promotion')['TotalPrice'].mean().sort_values(ascending=False)
    
    fig5, ax5 = plt.subplots(figsize=(6, 3)) # Standardized Size
    ax5.bar(promo_data.index, promo_data.values, color='#e67e22')
    ax5.set_xlabel("Promotion Type")
    ax5.set_ylabel("Avg Order Value (₹)")
    ax5.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    for i, v in enumerate(promo_data.values):
        ax5.text(i, v, f"₹{v:,.0f}", ha='center', va='bottom', fontsize=8)
        
    st.pyplot(fig5)
else:
    st.warning("Promotion column not found.")

# ---------------- DATA VIEW ----------------
with st.expander("🔍 Detailed Regional Records"):
    st.dataframe(f_df)