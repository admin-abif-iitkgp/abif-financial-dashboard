# pages/4_Tutorial.py
import streamlit as st

st.set_page_config(page_title="Tutorial", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] li:first-child {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Financial Analysis Tutorial")

st.header("How to Use This Platform")

with st.expander("1. Entering Financial Data"):
    st.write("""
    1. Navigate to the Financial Dashboard
    2. Input your financial metrics in the provided form
    3. Click 'Calculate Financial Ratios' to generate analysis
    4. View results in tables and visualizations
    """)

with st.expander("2. Understanding the Results"):
    st.write("""
    The analysis provides four categories of ratios:
    - Profitability Ratios: Measure company's ability to generate profit
    - Liquidity Ratios: Assess ability to meet short-term obligations
    - Efficiency Ratios: Evaluate operational efficiency
    - Solvency Ratios: Analyze long-term financial stability
    """)

with st.expander("3. Using Advanced Features"):
    st.write("""
    - Save data for historical comparison
    - View trends over time
    - Export reports for further analysis
    - Compare with industry benchmarks
    """)

