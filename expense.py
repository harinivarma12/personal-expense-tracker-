from datetime import datetime


class Expense:
    """Represents a single expense entry with date, category, amount, and description."""

    def __init__(self, date, category, amount, description):
        # Validate and store each field when the object is created
        self.date = self._validate_date(date)
        self.category = category
        self.amount = self._validate_amount(amount)
        self.description = description

    # ---------- Validation helpers ----------
    @staticmethod
    def _validate_date(date_str):
        """Ensure the date is in YYYY-MM-DD format, raise an error if not."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
        return date_str

    @staticmethod
    def _validate_amount(amount):
        """Ensure the amount is a positive number, raise an error if not."""
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"Amount must be a number: {amount}")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return amount

    # ---------- Getters ----------
    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def get_amount(self):
        return self.amount

    def get_description(self):
        return self.description

    # ---------- Setters ----------
    def set_date(self, date):
        self.date = self._validate_date(date)

    def set_category(self, category):
        self.category = category

    def set_amount(self, amount):
        self.amount = self._validate_amount(amount)

    def set_description(self, description):
        self.description = description

    # ---------- Conversion methods (for saving/loading from JSON) ----------
    def to_dict(self):
        """Convert this expense to a dictionary, used when saving to the JSON file."""
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Expense object from a dictionary, used when loading from the JSON file."""
        return cls(data["date"], data["category"], data["amount"], data["description"])

    def __str__(self):
        """Defines how an Expense prints as readable text (used in View All, filters, etc.)."""
        return f"{self.date} | {self.category:<15} | ${self.amount:>8.2f} | {self.description}"