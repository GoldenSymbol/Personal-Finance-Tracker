<img width="1536" height="1024" alt="ChatGPT Image Aug 3, 2025, 07_08_31 PM" src="https://github.com/user-attachments/assets/117de34b-17c6-47e4-a9b0-8271979906c9" />

---

# Personal Finance Tracker

A simple and lightweight application built with Streamlit that allows users to log income and expenses, store them in a CSV file, and later visualize and analyze their financial activity.

---

## Project Overview

**Goal**: Help individuals track their daily finances by recording transactions and storing them persistently.

This project is ideal for students and junior developers seeking hands-on experience with:
- Streamlit (for UI)
- Pandas (for data manipulation)
- File handling with CSV
- Modular Python structure

---

## Features Implemented

- Upload and display a simple UI  
- Add new transactions (amount, category, type, date)
  <img width="1204" height="778" alt="צילום מסך 2025-09-02 201025" src="https://github.com/user-attachments/assets/fa2c1935-33e5-4fde-9b6c-fa10192a94da" />
- Save transactions to a persistent CSV file  
- Load saved transactions on app startup  

---

## Project Structure

Personal-Finance-Tracker/
│
├── app.py # Main Streamlit application
├── transactions.csv # File storing all income/expense entries
└── utils/    
              ├── init.py
              └── data_handler.py # Load/save logic for CSV file

---

## Technologies Used

- Python 3.10+
- Streamlit
- Pandas
- CSV file I/O

---

## Use The App

- Fill in transaction details.
- Click "Add Transaction".
- All data is saved to transactions.csv.

---

## Next Step

- Add data visualization with charts
- Add filtering by category or date
- Add monthly summary dashboard
