import tkinter as tk
from tkinter import messagebox
from data_manager import (
    load_expenses, add_expense, filter_by_category,
    filter_by_date_range, generate_summary
)


class ExpenseTrackerApp:
    """Main GUI application for the Personal Expense Tracker.
    Handles the menu buttons and displays results in a text output box."""

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("650x700")

        # Load any previously saved expenses when the app starts
        self.expenses = load_expenses()

        # --- Menu buttons ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Expense", width=18, command=self.add_expense_window).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View All", width=18, command=self.view_all).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="View by Category", width=18, command=self.view_by_category_window).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View by Date Range", width=18, command=self.view_by_date_window).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Summary Report", width=18, command=self.show_summary).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Exit", width=18, command=root.quit).grid(row=2, column=1, padx=5, pady=5)

        # --- Output area where results are displayed ---
        self.output_box = tk.Text(root, height=15, width=70, bg="white", fg="black", font=("Arial", 12))
        self.output_box.pack(pady=10)

    def display(self, text):
        """Clear the output box and show new text in it."""
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)

    # ---------- Add Expense ----------
    def add_expense_window(self):
        """Open a popup window with input fields to add a new expense."""
        win = tk.Toplevel(self.root)
        win.title("Add Expense")

        labels = ["Date (YYYY-MM-DD)", "Category", "Amount", "Description"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(win, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        def submit():
            # Read the values typed into each input field
            date, category, amount, description = [e.get() for e in entries]
            try:
                add_expense(self.expenses, date, category, amount, description)
                messagebox.showinfo("Success", "Expense added!")
                win.destroy()
            except ValueError as e:
                # Shows a friendly error instead of crashing on bad input
                messagebox.showerror("Invalid input", str(e))

        tk.Button(win, text="Save", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

    # ---------- View All ----------
    def view_all(self):
        """Display every recorded expense in the output box."""
        if not self.expenses:
            self.display("No expenses recorded yet.")
            return
        text = "\n".join(str(e) for e in self.expenses)
        self.display(text)

    # ---------- View by Category ----------
    def view_by_category_window(self):
        """Open a popup asking for a category, then display matching expenses."""
        win = tk.Toplevel(self.root)
        win.title("View by Category")
        tk.Label(win, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        entry = tk.Entry(win, width=25)
        entry.grid(row=0, column=1, padx=5, pady=5)

        def submit():
            results = filter_by_category(self.expenses, entry.get())
            text = "\n".join(str(e) for e in results) if results else "No matching expenses."
            self.display(text)
            win.destroy()

        tk.Button(win, text="Search", command=submit).grid(row=1, column=0, columnspan=2, pady=10)

    # ---------- View by Date Range ----------
    def view_by_date_window(self):
        """Open a popup asking for a start/end date, then display matching expenses."""
        win = tk.Toplevel(self.root)
        win.title("View by Date Range")
        tk.Label(win, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(win, width=25)
        start_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(win, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(win, width=25)
        end_entry.grid(row=1, column=1, padx=5, pady=5)

        def submit():
            try:
                results = filter_by_date_range(self.expenses, start_entry.get(), end_entry.get())
                text = "\n".join(str(e) for e in results) if results else "No matching expenses."
                self.display(text)
                win.destroy()
            except ValueError as e:
                # Catches invalid date formats typed by the user
                messagebox.showerror("Invalid input", str(e))

        tk.Button(win, text="Search", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

    # ---------- Summary ----------
    def show_summary(self):
        """Calculate and display the summary report (total, highest, etc.)."""
        if not self.expenses:
            self.display("No expenses recorded yet.")
            return
        summary = generate_summary(self.expenses)
        text = (
            f"Total spent: ${summary['total']:.2f}\n"
            f"Highest expense: {summary['highest']}\n"
            f"Most common category: {summary['most_common_category']}\n"
            f"Average daily spending: ${summary['average_daily']:.2f}"
        )
        self.display(text)


# --- Program entry point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()