import streamlit as st
import pandas as pd
import os
from utils.data_handler import load_data, save_transactions
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

data_file = "data/transactions.CSV"
df = load_data(data_file)
df["date"] = pd.to_datetime(df["date"])

st.header("Add New Transaction")
with st.form("transactions form"):
    amount = st.number_input("Amount", format("%.2f"))
    category = st.text_input("Category (Groceries, rent, salary, e.g.)")
    transaction_type = st.selectbox("Type", ["Income", "Expense"])
    date = st.date_input("Date")
    submitted = st.form_submit_button("Add Transaction")

    if  submitted:
        save_transactions(data_file, amount, category, transaction_type, date)
        st.success("Transaction added successfully !")

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

st.header("Filter Transactions by Date Range")

strat_data = st.date_input("Start Date", value = df["date"].min())
end_date = st.date_input("End Date", value = df["date"].max())

if strat_data > end_date:
    st.error("Start date must be before the ends date.")
else:
    filtered_df = df[(df["date"] >= pd.to_datetime(strat_data)) & (df["date"] <= pd.to_datetime(end_date))]
    st.subheader("Filtered Transactions")
    st.dataframe(filtered_df)

