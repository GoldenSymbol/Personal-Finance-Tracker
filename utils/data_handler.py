"""Data handler module for managing CSV file operations."""
from typing import Optional
import pandas as pd
import os
import logging

# Constants
DATA_FILE = "data.csv"
INCOME = "Income"
EXPENSE = "Expense"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_data_file() -> None:
    """Initialize the data file if it doesn't exist.

    Creates a new CSV file with the required columns if the file is not found.
    """
    try:
        if not os.path.exists(DATA_FILE):
            df = pd.DataFrame(columns=["date", "category", "amount", "type"])
            df.to_csv(DATA_FILE, index=False)
            logger.info(f"Created new data file: {DATA_FILE}")
    except Exception as e:
        logger.error(f"Error initializing data file: {e}")
        raise


def load_data() -> pd.DataFrame:
    """Load data from the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing all transactions.
        Returns empty DataFrame if file is corrupted or can't be read.
    """
    try:
        initialize_data_file()
        df = pd.read_csv(DATA_FILE)
        logger.info(f"Loaded {len(df)} records from {DATA_FILE}")
        return df
    except pd.errors.EmptyDataError:
        logger.warning(f"Data file {DATA_FILE} is empty")
        return pd.DataFrame(columns=["date", "category", "amount", "type"])
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["date", "category", "amount", "type"])


def add_record(date: str, category: str, amount: float, type_: str) -> bool:
    """Add a new transaction record to the CSV file.

    Args:
        date: Transaction date
        category: Transaction category (e.g., 'Groceries', 'Salary')
        amount: Transaction amount (must be positive)
        type_: Transaction type (Income or Expense)

    Returns:
        bool: True if record was added successfully, False otherwise
    """
    try:
        # Validate inputs
        if not category or not category.strip():
            logger.error("Category cannot be empty")
            return False

        if amount <= 0:
            logger.error("Amount must be positive")
            return False

        if type_ not in [INCOME, EXPENSE]:
            logger.error(f"Type must be '{INCOME}' or '{EXPENSE}'")
            return False

        initialize_data_file()
        df = load_data()
        new_record = {
            "date": date,
            "category": category.strip(),
            "amount": amount,
            "type": type_
        }
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        logger.info(f"Added new record: {new_record}")
        return True
    except Exception as e:
        logger.error(f"Error adding record: {e}")
        return False


def get_summary() -> pd.DataFrame:
    """Get a summary of transactions grouped by category.

    Returns:
        pd.DataFrame: DataFrame with columns ['category', 'total']
    """
    try:
        df = load_data()
        if df.empty:
            return pd.DataFrame(columns=["category", "total"])
        return df.groupby("category")["amount"].sum().reset_index(name="total")
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return pd.DataFrame(columns=["category", "total"])
