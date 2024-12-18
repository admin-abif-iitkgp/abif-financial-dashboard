# pages/2_Advanced_Financial_Dashboard.py
import streamlit as st
from utils.auth import auth
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from utils.db import financial_data, users
from utils.results import display_financial_period_results
import pandas as pd
import math

st.set_page_config(page_title="Advanced Financial Dashboard", layout="wide")
auth()

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


def generate_options(duration_type):
    current_date = datetime.now()
    options = []

    if duration_type == "Monthly":
        for i in range(12):
            date = current_date - timedelta(days=30 * i)
            options.append(date.strftime("%b %Y"))
    elif duration_type == "Quarterly":
        for i in range(4):
            date = current_date - timedelta(days=90 * i)
            quarter = (date.month - 1) // 3 + 1
            fiscal_year = date.year if date.month > 3 else date.year - 1
            options.append(f"FY {fiscal_year}-{str(fiscal_year + 1)[-2:]} Q{quarter}")
    elif duration_type == "Annually":
        for i in range(5):
            date = current_date - timedelta(days=365 * i)
            fiscal_year = date.year if date.month > 3 else date.year - 1
            options.append(f"FY {fiscal_year}-{str(fiscal_year + 1)[-2:]}")

    return options


def generate_date_range(duration, duration_type):
    today = date.today()
    if duration_type == "Monthly":
        start_date = datetime.strptime(duration, "%b %Y").date().replace(day=1)
        end_date = start_date + relativedelta(months=1, days=-1)
    elif duration_type == "Quarterly":
        year, quarter = duration.split(" Q")
        year = int(year.split("-")[0])
        quarter = int(quarter)
        start_date = date(year, 3 * quarter - 2, 1)
        end_date = start_date + relativedelta(months=3, days=-1)
    elif duration_type == "Annually":
        year = int(duration.split("-")[0])
        start_date = date(year, 4, 1)
        end_date = date(year + 1, 3, 31)
    else:
        raise ValueError("Invalid duration type")

    return start_date, end_date


def save_financial_data(username, duration, duration_type, metrics):
    start_date, end_date = generate_date_range(duration, duration_type)
    data = {
        "username": username,
        "duration": duration,  # e.g., "Jan 2024" or "FY 2023-24 Q4"
        "duration_type": duration_type,  # "Monthly", "Quarterly", or "Annually"
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "data": {
            # Income Statement Metrics
            "revenue": metrics["revenue"],
            "operating_profit": metrics["operating_profit"],
            "ebit": metrics["ebit"],
            "cogs": metrics["cogs"],
            "net_profit": metrics["net_profit"],
            "interest_expense": metrics["interest_expense"],
            "pbit": metrics["pbit"],
            # Balance Sheet Metrics
            "total_assets": metrics["total_assets"],
            "current_assets": metrics["current_assets"],
            "liquid_current_assets": metrics["liquid_current_assets"],
            "cash": metrics["cash"],
            "average_inventory": metrics["average_inventory"],
            "total_equity": metrics["total_equity"],
            "current_liabilities": metrics["current_liabilities"],
            "cash_equivalents": metrics["cash_equivalents"],
            "average_accounts_receivable": metrics["average_accounts_receivable"],
            "average_accounts_payable": metrics["average_accounts_payable"],
            "total_debt": metrics["total_debt"],
            "shareholders_equity": metrics["shareholders_equity"],
            "capital_employed": metrics["capital_employed"],
            "average_assets": metrics["average_assets"],
            "average_total_assets": metrics["average_total_assets"],
            # Sales Metrics
            "net_sales": metrics["net_sales"],
            "net_credit_sales": metrics["net_credit_sales"],
            "net_annual_sales": metrics["net_annual_sales"],
            "net_credit_purchases": metrics["net_credit_purchases"],
            "average_working_capital": metrics["average_working_capital"],
        },
    }

    try:
        # Insert the document into MongoDB
        financial_data.insert_one(data)
        return True, "Data saved successfully"
    except Exception as e:
        return False, f"Error saving data: {str(e)}"


@st.dialog("Add Financial Data", width="large")
def add_financial_data():
    col1, col2 = st.columns(2)
    with col1:
        duration_type = st.selectbox(
            "Choose Duration Type",
            ("Monthly", "Quarterly", "Annually"),
            key="dialog_duration_type",
        )

    with col2:
        duration_options = generate_options(duration_type)
        selected_duration = st.selectbox(
            "Select Period", duration_options, key="dialog_selected_duration"
        )

    st.markdown("---")

    # Financial Metrics Input
    st.subheader("Financial Metrics")

    # Income Statement Metrics
    with st.expander("Income Statement Metrics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            revenue = st.number_input("Revenue", min_value=0.0, format="%f")
            operating_profit = st.number_input("Operating Profit", format="%f")
            ebit = st.number_input("EBIT", format="%f")
            cogs = st.number_input(
                "Cost of Goods Sold (COGS)", min_value=0.0, format="%f"
            )
        with col2:
            net_profit = st.number_input("Net Profit", format="%f")
            interest_expense = st.number_input(
                "Interest Expense", min_value=0.0, format="%f"
            )
            pbit = st.number_input("PBIT", format="%f")

    # Balance Sheet Metrics
    with st.expander("Balance Sheet Metrics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            total_assets = st.number_input("Total Assets", min_value=0.0, format="%f")
            current_assets = st.number_input(
                "Current Assets", min_value=0.0, format="%f"
            )
            liquid_current_assets = st.number_input(
                "Liquid Current Assets", min_value=0.0, format="%f"
            )
            cash = st.number_input("Cash", min_value=0.0, format="%f")
            average_inventory = st.number_input(
                "Average Inventory", min_value=0.0, format="%f"
            )
        with col2:
            total_equity = st.number_input("Total Equity", min_value=0.0, format="%f")
            current_liabilities = st.number_input(
                "Current Liabilities", min_value=0.0, format="%f"
            )
            cash_equivalents = st.number_input(
                "Cash Equivalents", min_value=0.0, format="%f"
            )
            average_accounts_receivable = st.number_input(
                "Average Accounts Receivable", min_value=0.0, format="%f"
            )
            average_accounts_payable = st.number_input(
                "Average Accounts Payable", min_value=0.0, format="%f"
            )
        with col3:
            total_debt = st.number_input("Total Debt", min_value=0.0, format="%f")
            shareholders_equity = st.number_input(
                "Shareholders' Equity", min_value=0.0, format="%f"
            )
            capital_employed = st.number_input(
                "Capital Employed", min_value=0.0, format="%f"
            )
            average_assets = st.number_input(
                "Average Assets", min_value=0.0, format="%f"
            )
            average_total_assets = st.number_input(
                "Average Total Assets", min_value=0.0, format="%f"
            )

    # Sales Metrics
    with st.expander("Sales Metrics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            net_sales = st.number_input("Net Sales", min_value=0.0, format="%f")
            net_credit_sales = st.number_input(
                "Net Credit Sales", min_value=0.0, format="%f"
            )
            net_annual_sales = st.number_input(
                "Net Annual Sales", min_value=0.0, format="%f"
            )
        with col2:
            net_credit_purchases = st.number_input(
                "Net Credit Purchases", min_value=0.0, format="%f"
            )
            average_working_capital = st.number_input(
                "Average Working Capital", min_value=0.0, format="%f"
            )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", type="secondary", use_container_width=True):
            st.rerun()
    with col2:
        save_btn = st.button("Save", type="primary", use_container_width=True)

    if save_btn:
        metrics = {
            "revenue": revenue,
            "operating_profit": operating_profit,
            "ebit": ebit,
            "cogs": cogs,
            "net_profit": net_profit,
            "interest_expense": interest_expense,
            "pbit": pbit,
            "total_assets": total_assets,
            "current_assets": current_assets,
            "liquid_current_assets": liquid_current_assets,
            "cash": cash,
            "average_inventory": average_inventory,
            "total_equity": total_equity,
            "current_liabilities": current_liabilities,
            "cash_equivalents": cash_equivalents,
            "average_accounts_receivable": average_accounts_receivable,
            "average_accounts_payable": average_accounts_payable,
            "total_debt": total_debt,
            "shareholders_equity": shareholders_equity,
            "capital_employed": capital_employed,
            "average_assets": average_assets,
            "average_total_assets": average_total_assets,
            "net_sales": net_sales,
            "net_credit_sales": net_credit_sales,
            "net_annual_sales": net_annual_sales,
            "net_credit_purchases": net_credit_purchases,
            "average_working_capital": average_working_capital,
        }

        success, message = save_financial_data(
            username=st.session_state.user["username"],
            duration=selected_duration,
            duration_type=duration_type,
            metrics=metrics,
        )

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

@st.dialog("Add Financial Data", width="large")
def admin_add_financial_data(username):
    col1, col2 = st.columns(2)
    with col1:
        duration_type = st.selectbox(
            "Choose Duration Type",
            ("Monthly", "Quarterly", "Annually"),
            key="dialog_duration_type",
        )

    with col2:
        duration_options = generate_options(duration_type)
        selected_duration = st.selectbox(
            "Select Period", duration_options, key="dialog_selected_duration"
        )

    st.markdown("---")

    # Financial Metrics Input
    st.subheader("Financial Metrics")

    # Income Statement Metrics
    with st.expander("Income Statement Metrics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            revenue = st.number_input("Revenue", min_value=0.0, format="%f")
            operating_profit = st.number_input("Operating Profit", format="%f")
            ebit = st.number_input("EBIT", format="%f")
            cogs = st.number_input(
                "Cost of Goods Sold (COGS)", min_value=0.0, format="%f"
            )
        with col2:
            net_profit = st.number_input("Net Profit", format="%f")
            interest_expense = st.number_input(
                "Interest Expense", min_value=0.0, format="%f"
            )
            pbit = st.number_input("PBIT", format="%f")

    # Balance Sheet Metrics
    with st.expander("Balance Sheet Metrics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            total_assets = st.number_input("Total Assets", min_value=0.0, format="%f")
            current_assets = st.number_input(
                "Current Assets", min_value=0.0, format="%f"
            )
            liquid_current_assets = st.number_input(
                "Liquid Current Assets", min_value=0.0, format="%f"
            )
            cash = st.number_input("Cash", min_value=0.0, format="%f")
            average_inventory = st.number_input(
                "Average Inventory", min_value=0.0, format="%f"
            )
        with col2:
            total_equity = st.number_input("Total Equity", min_value=0.0, format="%f")
            current_liabilities = st.number_input(
                "Current Liabilities", min_value=0.0, format="%f"
            )
            cash_equivalents = st.number_input(
                "Cash Equivalents", min_value=0.0, format="%f"
            )
            average_accounts_receivable = st.number_input(
                "Average Accounts Receivable", min_value=0.0, format="%f"
            )
            average_accounts_payable = st.number_input(
                "Average Accounts Payable", min_value=0.0, format="%f"
            )
        with col3:
            total_debt = st.number_input("Total Debt", min_value=0.0, format="%f")
            shareholders_equity = st.number_input(
                "Shareholders' Equity", min_value=0.0, format="%f"
            )
            capital_employed = st.number_input(
                "Capital Employed", min_value=0.0, format="%f"
            )
            average_assets = st.number_input(
                "Average Assets", min_value=0.0, format="%f"
            )
            average_total_assets = st.number_input(
                "Average Total Assets", min_value=0.0, format="%f"
            )

    # Sales Metrics
    with st.expander("Sales Metrics", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            net_sales = st.number_input("Net Sales", min_value=0.0, format="%f")
            net_credit_sales = st.number_input(
                "Net Credit Sales", min_value=0.0, format="%f"
            )
            net_annual_sales = st.number_input(
                "Net Annual Sales", min_value=0.0, format="%f"
            )
        with col2:
            net_credit_purchases = st.number_input(
                "Net Credit Purchases", min_value=0.0, format="%f"
            )
            average_working_capital = st.number_input(
                "Average Working Capital", min_value=0.0, format="%f"
            )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", type="secondary", use_container_width=True):
            st.rerun()
    with col2:
        save_btn = st.button("Save", type="primary", use_container_width=True)

    if save_btn:
        metrics = {
            "revenue": revenue,
            "operating_profit": operating_profit,
            "ebit": ebit,
            "cogs": cogs,
            "net_profit": net_profit,
            "interest_expense": interest_expense,
            "pbit": pbit,
            "total_assets": total_assets,
            "current_assets": current_assets,
            "liquid_current_assets": liquid_current_assets,
            "cash": cash,
            "average_inventory": average_inventory,
            "total_equity": total_equity,
            "current_liabilities": current_liabilities,
            "cash_equivalents": cash_equivalents,
            "average_accounts_receivable": average_accounts_receivable,
            "average_accounts_payable": average_accounts_payable,
            "total_debt": total_debt,
            "shareholders_equity": shareholders_equity,
            "capital_employed": capital_employed,
            "average_assets": average_assets,
            "average_total_assets": average_total_assets,
            "net_sales": net_sales,
            "net_credit_sales": net_credit_sales,
            "net_annual_sales": net_annual_sales,
            "net_credit_purchases": net_credit_purchases,
            "average_working_capital": average_working_capital,
        }

        success, message = save_financial_data(
            username=username,
            duration=selected_duration,
            duration_type=duration_type,
            metrics=metrics,
        )

        if success:
            st.success(message)
            st.rerun()
        else:
            st.error(message)


def process_financial_data(data_list):
    processed_data = []
    for entry in data_list:
        # Create a base dictionary with non-data fields
        row = {
            "Period": entry["duration"],
            "Type": entry["duration_type"],
            "Date Range": f"{entry['start_date']} to {entry['end_date']}",
        }

        # Add all metrics from the data dictionary
        for key, value in entry["data"].items():
            # Convert snake_case to Title Case for better display
            display_key = " ".join(word.capitalize() for word in key.split("_"))
            row[display_key] = value

        processed_data.append(row)

    # Create DataFrame and set display options
    df = pd.DataFrame(processed_data)

    # Format numeric columns
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: "{:,.2f}".format(x))

    return df


if st.session_state.authenticated:
    st.title("Advanced Financial Dashboard")
    st.write("Welcome to the advanced financial dashboard!")
    st.markdown("---")
    if st.session_state.user_role == "admin":
        user_list = list(users.find({"role": {"$ne": "admin"}}, {"password": 0}))
        col1, col2 = st.columns(2)
        with col1:
            selected_user = st.selectbox(
                "Select User",
                [user["username"] for user in user_list],
                key="user_select",
            )
        if st.button("Add Financial Data"):
            admin_add_financial_data(selected_user)
        if selected_user:
            user_financial_data = financial_data.find({"username": selected_user})
            data_list = list(user_financial_data)
            preview_data = None
            num_rows = math.ceil(len(data_list) / 6)
            for row in range(num_rows):
                cols = st.columns(6)
                for i in range(6):
                    index = row * 6 + i
                    if index < len(data_list):
                        data = data_list[index]
                        with cols[i]:
                            if st.button(
                                f"{data['duration_type']} - {data['duration']}",
                                key=f"btn_{index}",
                                use_container_width=True,
                            ):
                                preview_data = data

            df = process_financial_data(data_list)
            st.dataframe(df, hide_index=True, use_container_width=True)

            if preview_data:
                st.markdown("---")
                st.header(
                    f"Financial Analysis Results for {preview_data['duration_type']} - {preview_data['duration']}"
                )
                display_financial_period_results(**preview_data["data"])
    elif st.session_state.user_role == "user":
        if st.button("Add Financial Data"):
            add_financial_data()

        user_financial_data = financial_data.find(
            {"username": st.session_state.user["username"]}
        )
        data_list = list(user_financial_data)
        preview_data = None
        num_rows = math.ceil(len(data_list) / 6)
        for row in range(num_rows):
            cols = st.columns(6)
            for i in range(6):
                index = row * 6 + i
                if index < len(data_list):
                    data = data_list[index]
                    with cols[i]:
                        if st.button(
                            f"{data['duration_type']} - {data['duration']}",
                            key=f"btn_{index}",
                            use_container_width=True,
                        ):
                            preview_data = data

        df = process_financial_data(data_list)
        st.dataframe(df, hide_index=True, use_container_width=True)

        if preview_data:
            st.markdown("---")
            st.header(
                f"Financial Analysis Results for {preview_data['duration_type']} - {preview_data['duration']}"
            )
            display_financial_period_results(**preview_data["data"])

else:
    st.title("Advanced Financial Dashboard")
    st.write("Please login to access Advanced Financial Dashboard.")
