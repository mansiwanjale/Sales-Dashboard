import streamlit as st

st.set_page_config(page_title="FlowState Analytics Portal", layout="wide")

# Center-aligned landing page
st.title("FlowState Sales Analytics Portal")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Welcome to the Performance Dashboard")
    st.write("""
    This application provides deep-dive analytics into sales performance, 
    product profitability, regional trends, and operational efficiency.
    
    **Instructions:**
    * Use the sidebar to navigate between different departments.
    * Apply date filters within each page to refine your view.
    * Hover over charts to see detailed data points.
    """)
    
    if st.button("🚀 Go to Analysis"):
        st.info("Please select 'Overview' from the sidebar to begin.")

with col2:
    st.image("flowstate.png", width=200)
    st.info("System Status: Online | Data Updated: 2026")