# pages/6_Financial_Guide.py
import streamlit as st

st.set_page_config(page_title="Financial Guide", layout="wide")

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] li:first-child {
            display: none;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Financial Metrics and Ratios Guide")

# Income Statement Metrics
st.header("Income Statement Metrics")
income_metrics = {
    "Revenue": "Total income generated from business operations",
    "Operating Profit": "Profit from core business operations (EBIT)",
    "EBIT": "Earnings Before Interest and Taxes",
    "COGS": "Cost of Goods Sold - Direct costs of producing goods",
    "Net Profit": "Final profit after all expenses and taxes",
    "Interest Expense": "Cost of borrowing money",
    "PBIT": "Profit Before Interest and Taxes",
}

for metric, description in income_metrics.items():
    with st.expander(metric):
        st.write(description)

# Balance Sheet Metrics
st.header("Balance Sheet Metrics")
balance_metrics = {
    "Total Assets": "Sum of all company assets",
    "Current Assets": "Assets convertible to cash within one year",
    "Liquid Current Assets": "Highly liquid assets excluding inventory",
    "Cash": "Immediately available funds",
    "Average Inventory": "Mean value of inventory over a period",
    "Total Equity": "Shareholders' stake in the company",
    "Current Liabilities": "Debts due within one year",
    "Cash Equivalents": "Short-term, highly liquid investments",
    "Total Debt": "Sum of all company debts",
    "Shareholders' Equity": "Net worth of the company to shareholders",
    "Capital Employed": "Total assets minus current liabilities",
}

for metric, description in balance_metrics.items():
    with st.expander(metric):
        st.write(description)

# Financial Ratios
st.header("Understanding Financial Ratios")

# Profitability Ratios
st.subheader("Profitability Ratios")
profitability = {
    "Gross Profit Margin": {
        "Formula": "(Revenue - COGS) / Revenue × 100",
        "Use": "Measures efficiency in converting revenue into profit",
        "Good Range": "20-30% (industry dependent)",
    },
    "Operating Profit Margin": {
        "Formula": "Operating Profit / Revenue × 100",
        "Use": "Shows operational efficiency",
        "Good Range": "10-20%",
    },
    "Net Profit Margin": {
        "Formula": "Net Profit / Revenue × 100",
        "Use": "Overall profitability including all costs",
        "Good Range": "5-20%",
    },
}

for ratio, details in profitability.items():
    with st.expander(ratio):
        st.write("**Formula:**", details["Formula"])
        st.write("**Use:**", details["Use"])
        st.write("**Target Range:**", details["Good Range"])

# Efficiency Ratios
st.subheader("Efficiency Ratios")
efficiency = {
    "Inventory Turnover": {
        "Formula": "COGS / Average Inventory",
        "Use": "How quickly inventory is sold",
        "Good Range": "4-6 times per year",
    },
    "Asset Turnover": {
        "Formula": "Net Sales / Average Total Assets",
        "Use": "Efficiency of asset use in generating sales",
        "Good Range": "Above 1",
    },
}

for ratio, details in efficiency.items():
    with st.expander(ratio):
        st.write("**Formula:**", details["Formula"])
        st.write("**Use:**", details["Use"])
        st.write("**Target Range:**", details["Good Range"])

st.header("Best Practices")
with st.expander("Tips for Financial Analysis"):
    st.write(
        """
    1. Regular Monitoring: Track ratios monthly or quarterly
    2. Industry Comparison: Compare with industry standards
    3. Trend Analysis: Look for patterns over time
    4. Holistic View: Consider multiple ratios together
    5. Context Matters: Consider economic and market conditions
    """
    )

with st.expander("Common Mistakes to Avoid"):
    st.write(
        """
    1. Focusing on single metrics in isolation
    2. Ignoring industry specifics
    3. Not considering seasonal variations
    4. Overlooking non-financial factors
    5. Making decisions based on outdated data
    """
    )
