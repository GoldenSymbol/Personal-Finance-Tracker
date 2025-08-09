import pandas as pd
import os

DATA_FILE= "data.csv"

def initialize_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns = ["date", "category", "amount" ,"type"])
        df.to_csv(DATA_FILE, index = False)

def load_data():
    initialize_data_file()
    return pd.read_csv(DATA_FILE)

def add_record(date, category, amount, type_):
    initialize_data_file()
    df = load_data()
    new_record = {"date": date, "category": category, "amount": amount, "type": type_}
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index = True)
    df.to_csv(DATA_FILE, index = False)

def get_summary():
    df = load_data()
    if df.empty:
        return pd.DataFrame(columns = ["category", "total"])
    return df.gruopby("category")["amount"].sum().reset_index(name = "total")
