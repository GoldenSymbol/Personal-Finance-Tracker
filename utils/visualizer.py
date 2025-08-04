import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

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