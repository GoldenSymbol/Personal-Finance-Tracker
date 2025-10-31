"""Visualization module for creating financial charts and metrics."""
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import logging

# Constants
INCOME = "Income"
EXPENSE = "Expense"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def plot_total_by_type(df: pd.DataFrame) -> None:
    """Plot total income vs expenses as a bar chart.

    Args:
        df: DataFrame containing transaction data with 'type' and 'amount' columns
    """
    try:
        total_by_type = df.groupby('type')['amount'].sum()
        fig, ax = plt.subplots()
        total_by_type.plot(kind='bar', ax=ax, color=['green', 'red'])
        ax.set_title("Total Income vs Expenses")
        ax.set_ylabel("Amount ($)")
        ax.set_xlabel("Type")
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        logger.error(f"Error plotting total by type: {e}")
        st.error("Unable to generate income vs expenses chart")


def plot_by_category(df: pd.DataFrame) -> None:
    """Plot transactions grouped by category.

    Args:
        df: DataFrame containing transaction data with 'category' and 'amount' columns
    """
    try:
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)

        if category_totals.empty:
            st.info("No category data to display")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        category_totals.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_title("Transactions by Category")
        ax.set_xlabel("Amount ($)")
        ax.set_ylabel("Category")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        logger.error(f"Error plotting by category: {e}")
        st.error("Unable to generate category chart")


def plot_monthly_summary(df: pd.DataFrame) -> None:
    """Plot monthly summary of income and expenses as a line chart.

    Args:
        df: DataFrame containing transaction data with 'date', 'type', and 'amount' columns
    """
    try:
        df_copy = df.copy()
        df_copy['Month'] = pd.to_datetime(df_copy['date']).dt.to_period('M').astype(str)
        summary = df_copy.groupby(['Month', 'type'])['amount'].sum().reset_index()

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=summary, x='Month', y='amount', hue='type', marker='o', ax=ax)
        ax.set_title("Monthly Summary")
        ax.set_ylabel("Amount ($)")
        ax.set_xlabel("Month")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        logger.error(f"Error plotting monthly summary: {e}")
        st.error("Unable to generate monthly summary chart")


def plot_monthly_income_vs_expenses(df: pd.DataFrame) -> None:
    """Plot monthly income vs expenses as a bar chart.

    Args:
        df: DataFrame containing transaction data with 'date', 'type', and 'amount' columns
    """
    try:
        df_copy = df.copy()
        df_copy["month"] = df_copy["date"].dt.to_period("M").astype(str)
        grouped = df_copy.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)

        st.subheader("Monthly Income vs Expenses")
        fig, ax = plt.subplots(figsize=(10, 5))
        grouped.plot(kind="bar", ax=ax, color=['green', 'red'])
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount ($)")
        ax.set_title("Monthly Income vs Expenses")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        logger.error(f"Error plotting monthly income vs expenses: {e}")
        st.error("Unable to generate monthly comparison chart")


def get_top_expense_category(df: pd.DataFrame) -> None:
    """Display the top expense category as a metric.

    Args:
        df: DataFrame containing transaction data with 'type', 'category', and 'amount' columns
    """
    try:
        expenses = df[df["type"] == EXPENSE]
        if not expenses.empty:
            top_category = expenses.groupby("category")["amount"].sum().idxmax()
            total = expenses.groupby("category")["amount"].sum().max()
            st.metric("Top Expense Category", top_category, f"${total:.2f}")
        else:
            st.info("No expense data available")
    except Exception as e:
        logger.error(f"Error getting top expense category: {e}")
        st.error("Unable to calculate top expense category")


def display_total_income_expense(df: pd.DataFrame) -> None:
    """Display total income and expenses as metrics.

    Args:
        df: DataFrame containing transaction data with 'type' and 'amount' columns
    """
    try:
        income = df[df["type"] == INCOME]["amount"].sum()
        expense = df[df["type"] == EXPENSE]["amount"].sum()
        net = income - expense

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"${income:.2f}")
        with col2:
            st.metric("Total Expense", f"${expense:.2f}")
        with col3:
            st.metric("Net Balance", f"${net:.2f}", delta=f"${net:.2f}")
    except Exception as e:
        logger.error(f"Error displaying total income/expense: {e}")
        st.error("Unable to calculate totals")


def display_total_income_expense_ratio(df: pd.DataFrame) -> None:
    """Display the expense to income ratio as a metric.

    Args:
        df: DataFrame containing transaction data with 'type' and 'amount' columns
    """
    try:
        income = df[df["type"] == INCOME]["amount"].sum()
        expense = df[df["type"] == EXPENSE]["amount"].sum()

        if income > 0:
            ratio = (expense / income) * 100
            st.metric("Expense to Income Ratio", f"{ratio:.2f}%")
        else:
            st.info("No income data available to calculate ratio")
    except Exception as e:
        logger.error(f"Error calculating expense ratio: {e}")
        st.error("Unable to calculate expense ratio")
