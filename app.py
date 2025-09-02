import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

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

st.set_page_config(page_title = "Personal Finance Tracker", layout = "centered")
st.title("Personal Finance Tracker")

# LOAD DATA
df = load_data()
st.write("columns in CSV:", df.columns.tolist())
df.columns = df.columns.str.strip().str.lower()
st.write("columns after normalization:", df.columns.tolist())

# HANDLE EMPTY DATASET SAFELY
if not df.empty and "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ADD NEW TRANSACTION
st.header("Add New Transaction")
with st.form("transactions form"):
    amount = st.number_input("amount", format = "%.2f")
    category = st.text_input("category (Groceries, rent, salary, etc.)")
    transaction_type = st.selectbox("type", ["Income", "Expense"])
    date = st.date_input("date")
    submitted = st.form_submit_button("Add Transaction")

    if  submitted:
        add_record(date, category, amount, transaction_type)
        st.success("Transaction added successfully !")

# SUMMARY & VISUALIZATIONS
st.subheader("Summary")
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
    st.info("No data to visualize yet.")

# FILTER BY DATE RANGE
st.header("Filter Transactions by Date Range")
start_date, end_date = None, None
if not df.empty:  
    start_date = st.date_input("Start Date", value = df["date"].min().date())
    end_date = st.date_input("End Date", value = df["date"].max().date())

if start_date > end_date:
    st.error("Start date must be before the ends date.")
else:
    filtered_df = df[
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]
    st.subheader("Filtered Transaction")
    st.dataframe(filtered_df)
