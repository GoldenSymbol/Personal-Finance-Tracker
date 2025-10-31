"""Personal Finance Tracker - Main Streamlit Application."""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.data_handler import load_data, add_record
from utils.visualizer import (
    plot_by_category,
    plot_total_by_type,
    plot_monthly_summary,
    plot_monthly_income_vs_expenses,
    get_top_expense_category,
    display_total_income_expense,
    display_total_income_expense_ratio
)

# Page configuration
st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
st.title("Personal Finance Tracker")

# LOAD DATA
df = load_data()

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# HANDLE EMPTY DATASET SAFELY
if not df.empty and "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ADD NEW TRANSACTION
st.header("Add New Transaction")
with st.form("transactions_form"):
    amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f", step=0.01)
    category = st.text_input("Category (e.g., Groceries, Rent, Salary)", max_chars=50)
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    date = st.date_input("Date", value=datetime.today(), max_value=datetime.today())
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        # Validation
        if not category or not category.strip():
            st.error("Please enter a category.")
        elif amount <= 0:
            st.error("Amount must be greater than zero.")
        else:
            # Add the record
            success = add_record(date, category.strip(), amount, transaction_type)
            if success:
                st.success("Transaction added successfully!")
                st.rerun()
            else:
                st.error("Failed to add transaction. Please try again.")

# SUMMARY & VISUALIZATIONS
st.header("Summary")
if not df.empty:
    plot_total_by_type(df)
    plot_by_category(df)
    plot_monthly_summary(df)
    plot_monthly_income_vs_expenses(df)
    st.subheader("Smart Financial Insights")
    display_total_income_expense(df)
    get_top_expense_category(df)
    display_total_income_expense_ratio(df)
else:
    st.info("No data to visualize yet. Add your first transaction above!")

# FILTER BY DATE RANGE
st.header("Filter Transactions by Date Range")
if not df.empty:
    start_date = st.date_input("Start Date", value=df["date"].min().date())
    end_date = st.date_input("End Date", value=df["date"].max().date())

    if start_date > end_date:
        st.error("Start date must be before the end date.")
    else:
        filtered_df = df[
            (df["date"] >= pd.to_datetime(start_date)) &
            (df["date"] <= pd.to_datetime(end_date))
        ]
        st.subheader("Filtered Transactions")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No transactions found in the selected date range.")
else:
    st.info("No transactions available to filter.")
