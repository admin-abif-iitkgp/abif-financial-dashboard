import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def load_preset_data():
    return {
        # Income Statement Metrics
        "revenue": 1000000.0,
        "operating_profit": 250000.0,
        "ebit": 200000.0,
        "cogs": 600000.0,
        "net_profit": 180000.0,
        "interest_expense": 20000.0,
        "pbit": 220000.0,
        # Balance Sheet Metrics
        "total_assets": 2000000.0,
        "current_assets": 800000.0,
        "liquid_current_assets": 500000.0,
        "cash": 300000.0,
        "average_inventory": 200000.0,
        "total_equity": 1200000.0,
        "current_liabilities": 400000.0,
        "cash_equivalents": 100000.0,
        "average_accounts_receivable": 150000.0,
        "average_accounts_payable": 120000.0,
        "total_debt": 800000.0,
        "shareholders_equity": 1200000.0,
        "capital_employed": 1600000.0,
        "average_assets": 1900000.0,
        "average_total_assets": 1900000.0,
        # Sales Metrics
        "net_sales": 1000000.0,
        "net_credit_sales": 800000.0,
        "net_annual_sales": 1000000.0,
        "net_credit_purchases": 600000.0,
        "average_working_capital": 400000.0,
    }


st.set_page_config(page_title="Financial Dashboard", layout="wide")

# Hide "app" from sidebar
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


def format_number(value):
    return "{:,.2f}".format(value)


def create_gauge_chart(value, title, min_val=0, max_val=100):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [min_val, max_val]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, max_val / 3], "color": "lightgray"},
                    {"range": [max_val / 3, 2 * max_val / 3], "color": "gray"},
                ],
            },
        )
    )
    fig.update_layout(height=200)
    return fig


st.title("Financial Dashboard")
st.markdown("---")

if st.button("Load Preset Data"):
    preset_data = load_preset_data()
    st.session_state.update(preset_data)
    st.success("Preset data loaded successfully!")


# Input Form
with st.form("financial_metrics_form"):
    st.header("Enter Financial Metrics")

    # Income Statement Metrics
    st.subheader("Income Statement Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        revenue = st.number_input(
            "Revenue",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("revenue", 0.0),
        )
        operating_profit = st.number_input(
            "Operating Profit",
            format="%f",
            value=st.session_state.get("operating_profit", 0.0),
        )
        ebit = st.number_input(
            "EBIT", format="%f", value=st.session_state.get("ebit", 0.0)
        )

    with col2:
        cogs = st.number_input(
            "Cost of Goods Sold (COGS)",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("cogs", 0.0),
        )
        net_profit = st.number_input(
            "Net Profit", format="%f", value=st.session_state.get("net_profit", 0.0)
        )
        interest_expense = st.number_input(
            "Interest Expense",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("interest_expense", 0.0),
        )

    with col3:
        pbit = st.number_input(
            "PBIT", format="%f", value=st.session_state.get("pbit", 0.0)
        )

    # Balance Sheet Metrics
    st.subheader("Balance Sheet Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        total_assets = st.number_input(
            "Total Assets",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("total_assets", 0.0),
        )
        current_assets = st.number_input(
            "Current Assets",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("current_assets", 0.0),
        )
        liquid_current_assets = st.number_input(
            "Liquid Current Assets",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("liquid_current_assets", 0.0),
        )
        cash = st.number_input(
            "Cash", min_value=0.0, format="%f", value=st.session_state.get("cash", 0.0)
        )
        average_inventory = st.number_input(
            "Average Inventory",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_inventory", 0.0),
        )

    with col2:
        total_equity = st.number_input(
            "Total Equity",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("total_equity", 0.0),
        )
        current_liabilities = st.number_input(
            "Current Liabilities",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("current_liabilities", 0.0),
        )
        cash_equivalents = st.number_input(
            "Cash Equivalents",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("cash_equivalents", 0.0),
        )
        average_accounts_receivable = st.number_input(
            "Average Accounts Receivable",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_accounts_receivable", 0.0),
        )
        average_accounts_payable = st.number_input(
            "Average Accounts Payable",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_accounts_payable", 0.0),
        )

    with col3:
        total_debt = st.number_input(
            "Total Debt",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("total_debt", 0.0),
        )
        shareholders_equity = st.number_input(
            "Shareholders' Equity",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("shareholders_equity", 0.0),
        )
        capital_employed = st.number_input(
            "Capital Employed",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("capital_employed", 0.0),
        )
        average_assets = st.number_input(
            "Average Assets",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_assets", 0.0),
        )
        average_total_assets = st.number_input(
            "Average Total Assets",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_total_assets", 0.0),
        )

    # Sales Metrics
    st.subheader("Sales Metrics")
    col1, col2 = st.columns(2)

    with col1:
        net_sales = st.number_input(
            "Net Sales",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("net_sales", 0.0),
        )
        net_credit_sales = st.number_input(
            "Net Credit Sales",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("net_credit_sales", 0.0),
        )
        net_annual_sales = st.number_input(
            "Net Annual Sales",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("net_annual_sales", 0.0),
        )

    with col2:
        net_credit_purchases = st.number_input(
            "Net Credit Purchases",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("net_credit_purchases", 0.0),
        )
        average_working_capital = st.number_input(
            "Average Working Capital",
            min_value=0.0,
            format="%f",
            value=st.session_state.get("average_working_capital", 0.0),
        )

    submitted = st.form_submit_button("Calculate Financial Ratios")

# Analysis Section (shown only after form submission)
if submitted:
    try:
        st.markdown("---")
        st.header("Financial Analysis Results")

        # Calculate all ratios (same calculations as before)
        profitability_ratios = {
            "Gross Profit Margin": (
                ((revenue - cogs) / revenue * 100) if revenue != 0 else 0
            ),
            "Operating Profit Margin": (
                (operating_profit / revenue * 100) if revenue != 0 else 0
            ),
            "Net Profit Margin": (net_profit / revenue * 100) if revenue != 0 else 0,
            "Return on Assets": (
                (net_profit / average_assets * 100) if average_assets != 0 else 0
            ),
            "Return on Capital Employed": (
                (pbit / capital_employed * 100) if capital_employed != 0 else 0
            ),
            "Return on Equity": (
                (net_profit / shareholders_equity * 100)
                if shareholders_equity != 0
                else 0
            ),
        }

        liquidity_ratios = {
            "Current Ratio": (
                current_assets / current_liabilities if current_liabilities != 0 else 0
            ),
            "Quick Ratio": (
                liquid_current_assets / current_liabilities
                if current_liabilities != 0
                else 0
            ),
            "Cash Ratio": (
                (cash + cash_equivalents) / current_liabilities
                if current_liabilities != 0
                else 0
            ),
        }

        efficiency_ratios = {
            "Accounts Receivable Turnover": (
                net_credit_sales / average_accounts_receivable
                if average_accounts_receivable != 0
                else 0
            ),
            "Accounts Payable Turnover": (
                net_credit_purchases / average_accounts_payable
                if average_accounts_payable != 0
                else 0
            ),
            "Assets Turnover": (
                net_sales / average_total_assets if average_total_assets != 0 else 0
            ),
            "Capital Turnover": (
                net_sales / capital_employed if capital_employed != 0 else 0
            ),
            "Inventory Turnover": (
                cogs / average_inventory if average_inventory != 0 else 0
            ),
            "Working Capital Turnover": (
                net_annual_sales / average_working_capital
                if average_working_capital != 0
                else 0
            ),
        }

        solvency_ratios = {
            "Debt Ratio": total_debt / total_assets if total_assets != 0 else 0,
            "Equity Ratio": total_equity / total_assets if total_assets != 0 else 0,
            "Debt to Equity": total_debt / total_equity if total_equity != 0 else 0,
            "Interest Coverage": (
                ebit / interest_expense if interest_expense != 0 else 0
            ),
        }

        # Display Ratios in two columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Profitability Ratios")
            prof_df = pd.DataFrame(
                list(profitability_ratios.items()), columns=["Ratio", "Value"]
            )
            prof_df["Value"] = prof_df["Value"].round(2).astype(str) + "%"
            st.dataframe(prof_df, use_container_width=True, hide_index=True)

            st.subheader("Solvency Ratios")
            solv_df = pd.DataFrame(
                list(solvency_ratios.items()), columns=["Ratio", "Value"]
            )
            solv_df["Value"] = solv_df["Value"].round(2)
            st.dataframe(solv_df, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("Efficiency Ratios")
            eff_df = pd.DataFrame(
                list(efficiency_ratios.items()), columns=["Ratio", "Value"]
            )
            eff_df["Value"] = eff_df["Value"].round(2)
            st.dataframe(eff_df, use_container_width=True, hide_index=True)

            st.subheader("Liquidity Ratios")
            liq_df = pd.DataFrame(
                list(liquidity_ratios.items()), columns=["Ratio", "Value"]
            )
            liq_df["Value"] = liq_df["Value"].round(2)
            st.dataframe(liq_df, use_container_width=True, hide_index=True)

        # Visualizations
        st.markdown("---")
        st.header("Ratio Visualizations")

        # Gauge charts
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(
                create_gauge_chart(
                    profitability_ratios["Net Profit Margin"], "Net Profit Margin (%)"
                ),
                use_container_width=True,
            )

        with col2:
            st.plotly_chart(
                create_gauge_chart(
                    liquidity_ratios["Current Ratio"] * 100,
                    "Current Ratio",
                    max_val=300,
                ),
                use_container_width=True,
            )

        with col3:
            st.plotly_chart(
                create_gauge_chart(
                    solvency_ratios["Debt to Equity"] * 100,
                    "Debt to Equity Ratio",
                    max_val=200,
                ),
                use_container_width=True,
            )

        # Additional charts
        st.plotly_chart(
            px.bar(
                prof_df, x="Ratio", y="Value", title="Profitability Ratios Comparison"
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            px.line_polar(
                eff_df,
                r="Value",
                theta="Ratio",
                line_close=True,
                title="Efficiency Ratios Overview",
            ),
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"An error occurred while calculating ratios: {str(e)}")
        st.error("Please check your input values and try again.")
