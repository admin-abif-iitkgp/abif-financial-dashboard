import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


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


def display_financial_period_results(
    revenue,
    operating_profit,
    ebit,
    cogs,
    net_profit,
    interest_expense,
    pbit,
    total_assets,
    current_assets,
    liquid_current_assets,
    cash,
    average_inventory,
    total_equity,
    current_liabilities,
    cash_equivalents,
    average_accounts_receivable,
    average_accounts_payable,
    total_debt,
    shareholders_equity,
    capital_employed,
    average_assets,
    average_total_assets,
    net_sales,
    net_credit_sales,
    net_annual_sales,
    net_credit_purchases,
    average_working_capital,
):
    try:
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
