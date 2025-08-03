import pandas as pd
import os

def load_data(filepath):
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=["Amount", "Category", "Type", "Date"])

def save_transactions(filepath, amount, category, transaction_type, date):
    new_data = pd.DataFrame([{
        "Amount": amount,
        "Category": category,
        "Type": transaction_type,
        "Date": date
    }])

    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(filepath, index=False)