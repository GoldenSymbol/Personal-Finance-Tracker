import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.externals.array_api_compat.dask.array import unstack


def plot_total_by_type(df):
    total_by_type = df.groupby('Type')['Amount'].sum()
    fig, ax = plt.subplots()
    total_by_type.plot(kind = 'bar', ax = ax, color = ['green', 'red'])
    ax.set_title("Total Income vs Expenses")
    ax.set_ylabel("Amount")
    st.pyplot(fig)

def plot_by_category(df):
    fig, ax = plt.subplots()
    ax.set_title("Transactions by Category")
    st.pyplot(fig)

def plot_monthly_summary(df):
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)
    summary = df.groupby(['Month', 'Type'])['Amount'].sum().reset_index()
    fig, ax = plt.subplots(figsize = (10,4))
    sns.lineplot(data = summary, x = 'Month', y = 'Amount', hue = 'Type', marker = 'o', ax = ax)
    ax.set_title("Monthly Summary")
    plt.xticks(rotation = 45)
    st.pyplot(fig)

def plot_monthly_income_vs_expenses(df):
    df["month"] = df["date"].dt.to_period("M").astype(str)
    grouped = df.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)

    st.subheader("Monthly Income vs Expenses")
    grouped.plot(kind = "bar", figsize = (10, 5))
    plt.xlabel("month")
    plt.ylabel("Amount")
    plt.title("Month Income vs Expenses")
    st.pyplot(plt)

def get_top_expense_category(df):
    expenses = df[df["type"] == ["Expense"]]
    if not expenses.empty:
        top_category = expenses.groupby("category")["amount"].sum().idxmax()
        total = expenses.groupby("category")["amount"].sum().max()
        st.metric("Top Expense Category", top_category, f"{total:.2f}$")

def display_total_income_expense(df):
    income = df[df["type"] == "Income"]["amount"].sum()
    expense = df[df["type"] == "Expense"]["amount"].sum()
    st.metric("Total Income", f"{income:.2f}$")
    st.metric("Total Expense", f"{expense:.2f}$")

def display_total_income_expense_ratio(df):
    income = df[df["type"] == "Income"]["amount"].sum()
    expense = df[df["type"] == "Expense"]["amount"].sum()
    if income > 0:
        ratio = (expense / income) * 100
        st.metric("Expense to Income ratio", f"{ratio:.2f}$")
