import streamlit as st
import pandas as pd
import os
from utils.data_handler import load_data, save_transactions
from utiles.visualizer import generate_summary, plot_category_pie

st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
st.title("Personal Finance Tracker")

data_file = "data/transactions.CSV"
df = load_data(data_file)

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

st.header("Summary")
summary = generate_summary(df)
st.write(summary)

st.header("Spending Breakdown by Category")
plot_category_pie(df)

