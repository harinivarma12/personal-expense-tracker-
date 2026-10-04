import json
import os
from datetime import datetime
from expense import Expense

DATA_FILE = "expenses.json"


def load_expenses():
    """Load all expenses from the JSON file into a list of Expense objects.
    If the file doesn't exist or is empty, start with an empty list."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return [Expense.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError) as e:
        # Handles a corrupted or badly formatted JSON file gracefully
        print(f"Warning: could not read {DATA_FILE} ({e}). Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save the current list of Expense objects to the JSON file,
    so data persists the next time the program runs."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=2)
    except IOError as e:
        print(f"Error saving expenses: {e}")


def add_expense(expenses, date, category, amount, description):
    """Create a new Expense, validate it, add it to the list, and save to file."""
    new_expense = Expense(date, category, amount, description)
    expenses.append(new_expense)
    save_expenses(expenses)
    return new_expense


def filter_by_category(expenses, category):
    """Return only expenses matching the given category (case-insensitive)."""
    return [e for e in expenses if e.category.lower() == category.lower()]


def filter_by_date_range(expenses, start_date, end_date):
    """Return expenses with a date between start_date and end_date (inclusive)."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    result = []
    for e in expenses:
        e_date = datetime.strptime(e.date, "%Y-%m-%d")
        if start <= e_date <= end:
            result.append(e)
    return result


def generate_summary(expenses):
    """Calculate and return summary statistics: total spent, highest expense,
    most common category, and average daily spending."""
    if not expenses:
        return {
            "total": 0,
            "highest": None,
            "most_common_category": None,
            "average_daily": 0,
        }

    # Total spending across all expenses
    total = sum(e.amount for e in expenses)

    # Single highest expense by amount
    highest = max(expenses, key=lambda e: e.amount)

    # Count how many times each category appears, then find the most frequent
    category_counts = {}
    for e in expenses:
        category_counts[e.category] = category_counts.get(e.category, 0) + 1
    most_common_category = max(category_counts, key=category_counts.get)

    # Average spending per unique day (total divided by number of distinct dates)
    unique_days = {e.date for e in expenses}
    average_daily = total / len(unique_days) if unique_days else 0

    return {
        "total": total,
        "highest": highest,
        "most_common_category": most_common_category,
        "average_daily": average_daily,
    }