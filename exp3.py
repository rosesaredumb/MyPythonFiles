from datetime import datetime
from json_functions import json_funcs
import re
from globals import expenses_db_json_path, clear_console
from typing import Literal


class ExpenseTracker:
    def __init__(self):
        self.file_name = expenses_db_json_path
        self.json_handler = json_funcs()
        self.expenses = self.load_expenses()
        self.categories = self.get_all_categories()  # Initialize categories list
        self.input_bulletin = ">>>"
        self.response_bulletin = "--"
        self.error_bulletin = "!!"

    def mprint(self, sentence: str, type: Literal[1, 2, 3] = 1) -> str:
        if type not in {1, 2, 3}:
            raise ValueError("Type must be '1', '2', or '3'")
        if type == 1:
            x = str(input(f"\n{self.input_bulletin}{sentence}"))
            return x
        elif type == 2:
            print(f"\n{self.response_bulletin}{sentence}")
            return ""
        elif type == 3:
            print(f"\n{self.error_bulletin}{sentence}")
            return ""

    def load_expenses(self):
        """Load expenses from the JSON file."""
        data = self.json_handler.read_json(self.file_name)
        if data is None:
            return []
        return data

    def save_expenses(self):
        """Save expenses to the JSON file after sorting."""
        self.expenses.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))
        self.json_handler.write_json(self.expenses, self.file_name)

    def validate_date(self, date_input):
        """Validate and auto-correct date input to 'dd/mm/yyyy'."""
        try:
            if not date_input.strip():
                day = datetime.now().day
                month = datetime.now().month
                year = datetime.now().year
            else:
                date_parts = [
                    int(part) for part in re.split(r"[-/\\' ;]", date_input)
                    if part.isdigit()
                ]
                if len(date_parts) == 1:  # Day only
                    day = date_parts[0]
                    month = datetime.now().month
                    year = datetime.now().year
                elif len(date_parts) == 2:  # Day and month
                    day, month = date_parts
                    year = datetime.now().year
                elif len(date_parts) == 3:  # Day, month, and year
                    day, month, year = date_parts
                    if year < 100:  # Convert two-digit year
                        year += 2000
                else:
                    return None
            full_date = f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}"
            datetime.strptime(full_date, "%d/%m/%Y")  # Validate date
            return full_date
        except (ValueError, IndexError):
            return None

    def validate_amount(self, amount):
        """Validate and format the amount."""
        try:
            return round(float(amount), 2)
        except ValueError:
            return None

    def get_all_categories(self):
        """Get all unique categories from expenses."""
        categories = set()
        for expense in self.expenses:
            if expense["category"]:  # Ensure category is not None or empty
                categories.add(expense["category"].lower())
        return sorted(categories)

    def add_expense(self, date, amount, category, reason):
        """Add a new expense entry."""
        expense = {
            "date": date,          # Validated date passed as argument
            "amount": amount,      # Validated amount passed as argument
            "category": category,  # Category can be None or valid input
            "reason": reason       # Reason can be None or valid input
        }
        self.expenses.append(expense)
        self.save_expenses()
        self.mprint("Expense added successfully!", 2)
        print(f"Date: {date}\nAmount: {amount}\nCategory: {category or '>no category<'}\nReason: {reason or '>no reason<'}")

    def view_expenses(self, num_expenses=None):
        """
        View the specified number of latest expenses or all expenses if none specified.
        :param num_expenses: Number of latest expenses to display (default: 10 if not provided).
        """
        if not self.expenses:
            print("No expenses recorded yet.")
        else:
            num_expenses = num_expenses or 10  # Default to 10 if no value is provided
            print(f"Displaying the last {num_expenses} expenses:")
            print(f"{'Date':<10} {'Amount':>10}    {'Category':<20} {'Reason':<30}")
            print("-" * 80)  # Separator line
            for expense in self.expenses[-num_expenses:]:
                date = expense["date"]
                amount = f"{expense['amount']:.2f}"
                category = expense["category"] if expense["category"] else ">no category<"
                reason = expense["reason"] if expense["reason"] else ">no reason<"
                print(f"{date:<10} {amount:>10}    {category:<20} {reason:<30}")

    def delete_expense(self, index):
        """Delete an expense by index."""
        try:
            del self.expenses[index - 1]
            self.save_expenses()
            self.categories = self.get_all_categories()  # Refresh categories
            self.mprint("Expense deleted successfully!", 2)
        except IndexError:
            self.mprint("Invalid index. Please try again.", 3)

    def get_current_month_expenses_by_category(self):
        """Calculate the total expenses for the current month and group them by category."""
        current_month = datetime.now().month
        current_year = datetime.now().year
        category_expenses = {}

        # Filter expenses for the current month and group them by category
        for expense in self.expenses:
            expense_date = datetime.strptime(expense["date"], "%d/%m/%Y")
            if expense_date.month == current_month and expense_date.year == current_year:
                category = expense["category"] or ">no category<"  # Replace None or empty category
                category_expenses[category] = category_expenses.get(category, 0) + expense["amount"]

        # Calculate the total sum of current month's expenses
        total_sum = sum(category_expenses.values())

        # Sort the categories
        sorted_categories = sorted(category_expenses.items())

        # Display the results
        print("Expense breakdown for the current month:\n")
        print(f"{'Category':<20}  {'Amount':>10}")
        print("-" * 60)
        for category, amount in sorted_categories:
            print(f"{category:<20}  {amount:>10}")
        print("-" * 60)
        print(f"{'Total':<20}  {total_sum:>10}")

        return total_sum, dict(sorted_categories)

    def select_category(self):
        """Allow the user to select an existing category or create a new one."""
        while True:
            if not self.categories:
                category_input = self.mprint(
                    "\nNo categories available. "
                    "Enter 0 to create a new category / Press -Enter- to assign no category: ").strip()
                if category_input == '0':
                    category = self.mprint("Enter the new category: ").strip().lower()
                    if category:
                        if category not in self.categories:
                            self.categories.append(category)
                            self.mprint(f"Category '{category}' created!", 2)
                            return category
                        else:
                            self.mprint("Category already exists.", 2)
                    else:
                        self.mprint("Category cannot be empty. Try again.", 3)
                elif category_input == '':
                    return None
                else:
                    self.mprint("Invalid choice. Please try again.")
            else:
                category_input = input(
                    f"\nExisting categories:\n{''.join([f'{idx}. {cat}\n' for idx, cat in enumerate(self.categories, 1)])}"
                    f"Select category by entering number (1 - {len(self.categories)}) / "
                    "Enter 0 to create a new category / Press -Enter- to assign no category: ").strip()
                if category_input == '0':
                    category = input("Enter the new category: ").strip().lower()
                    if category:
                        if category not in self.categories:
                            self.categories.append(category)
                            print(f"Category '{category}' created!")
                            return category
                        else:
                            print("Category already exists.")
                    else:
                        print("Category cannot be empty. Try again.")
                elif category_input == '':
                    return None       
                else:
                    try:
                        category_index = int(category_input)
                        if 1 <= category_index <= len(self.categories):
                            return self.categories[category_index - 1]
                        else:
                            print("Invalid choice. Try again.")
                    except ValueError:
                        print("Invalid input. Try again.")

    def get_monthly_expenses(self, month_year_input: str = ""):
        """
        Get the total expenses and expenses grouped by category for a specific month and year.
        If no input is provided, use the current month and year.
        :param month_year_input: Input in formats like 'mm/yyyy', 'mm yy', 'mm,yy', 'mm' (current year assumed).
        :return: Total expenses and a dictionary of expenses grouped by category.
        """
        try:
            # Default to current month and year if no input is provided
            if not month_year_input.strip():
                month = datetime.now().month
                year = datetime.now().year
            else:
                # Split input using any non-digit character as a delimiter
                parts = [int(part) for part in re.split(r"[^\d]", month_year_input) if part.isdigit()]

                # Determine month and year based on input length
                if len(parts) == 1:  # Only month provided
                    month = parts[0]
                    year = datetime.now().year  # Default to current year
                elif len(parts) == 2:  # Month and year provided
                    month, year = parts
                    if year < 100:  # Convert two-digit year to four-digit year
                        year += 2000
                else:
                    raise ValueError("Invalid input format. Provide 'mm/yyyy', 'mm yy', 'mm,yy', or 'mm'.")

                # Validate month
                if not (1 <= month <= 12):
                    raise ValueError("Invalid month value. Must be between 1 and 12.")

            # Initialize category-wise expenses dictionary
            category_expenses = {}

            # Calculate total and category-wise expenses
            total_expenses = 0.0
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%d/%m/%Y")
                if expense_date.month == month and expense_date.year == year:
                    total_expenses += expense["amount"]
                    category = expense["category"] or ">no category<"  # Replace None or empty category
                    category_expenses[category] = category_expenses.get(category, 0) + expense["amount"]

            # Round the total expenses to 2 decimal places
            total_expenses = round(total_expenses, 2)

            sorted_categories = sorted(category_expenses.items())
            # Display results
            print(f"Expense breakdown for {str(month).zfill(2)}/{year}:\n")
            print(f"{'Category':<20}  {'Amount':>10}")
            print("-" * 60)
            for category, amount in sorted_categories:
                print(f"{category:<20}  {amount:>10.2f}")
            print("-" * 60)
            print(f"{'Total':<20}  {total_expenses:>10.2f}")

            return total_expenses, dict(sorted_categories)

        except (ValueError, IndexError):
            self.mprint("Invalid input format! Please provide 'mm/yyyy', 'mm yy', 'mm,yy', or 'mm'.", 3)
            return 0.0, {}

    def get_total_entries(self):
        """
        Display the total number of expense entries stored in the tracker.
        """
        total_entries = len(self.expenses)
        print(f"Total number of expense entries: {total_entries}")
        return total_entries

    def delete_recent_entry(self):
        """
        Delete an expense from the most recent 10 entries.
        """
        # Check if there are any expenses
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        # Get the last 10 entries
        recent_expenses = self.expenses[-10:]

        # Display the recent 10 entries
        print("\nMost Recent 10 Entries (or fewer):")
        print(f"{'Index':<6} {'Date':<10} {'Amount':>10}    {'Category':<20} {'Reason':<30}")
        print("-" * 80)
        for i, expense in enumerate(recent_expenses, start=1):
            date = expense["date"]
            amount = f"{expense['amount']:.2f}"
            category = expense["category"] if expense["category"] else ">no category<"
            reason = expense["reason"] if expense["reason"] else ">no reason<"
            print(f"{i:<6} {date:<10} {amount:>10}    {category:<20} {reason:<30}")
        print("-" * 80)

        # Ask the user to select an entry to delete
        while True:
            try:
                index = int(input("Enter the index of the entry to delete (1-10) or 0 to cancel: ").strip())
                if index == 0:
                    print("Deletion canceled.")
                    return
                if 1 <= index <= len(recent_expenses):
                    # Calculate the actual index in the full expenses list
                    actual_index = len(self.expenses) - len(recent_expenses) + (index - 1)
                    deleted_expense = self.expenses.pop(actual_index)
                    self.save_expenses()
                    print(f"Deleted entry: Date: {deleted_expense['date']}, Amount: {deleted_expense['amount']}")
                    return
                else:
                    print(f"Invalid index! Enter a number between 1 and {len(recent_expenses)}.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")

    def run(self):
        print("Welcome to the Expense Tracker!")
        while True:
            print("\n0. Exit")
            print("1. Add a new expense")
            print("2. View all expenses")
            print("3. Delete an expense")
            print("4. View total expenses for a specific month")
            choice = input("Enter your choice: ").strip()
            clear_console()

            if choice == "0":
                self.mprint("Exiting the Expense Tracker. Goodbye!", 2)
                break
                
            elif choice == "1":
                while True:
                    date_input = str(self.mprint("Enter the date (dd/mm/yyyy) or press Enter for today: ")).strip()
                    corrected_date = self.validate_date(date_input)
                    if corrected_date:
                        self.mprint(f"Date set as: {corrected_date}", 2)
                        break
                    self.mprint("Invalid date format! Please try again.", 3)

                while True:
                    amount = str(self.mprint("Enter the amount: ")).strip()
                    formatted_amount = self.validate_amount(amount)
                    if formatted_amount:
                        self.mprint(f"Amount set as: {formatted_amount}", 2)
                        break
                    self.mprint("Invalid amount! Please enter a valid number.", 3)

                category = self.select_category()
                self.mprint(f"Category set as: {category or '>no category<'}", 2)
                
                reason = str(self.mprint("Enter the reason / Press -Enter- to assign no reason: ")).strip() or None
                self.mprint(f"Reason set as: {reason or '>no reason<'}", 2)

                self.add_expense(corrected_date, formatted_amount, category, reason)
                
            elif choice == "2":
                while True:
                    try:
                        num_expenses = str(self.mprint("Enter the number of latest expenses to view (or press Enter for default 10): ")).strip()
                        clear_console()
                        num_expenses = int(num_expenses) if num_expenses else 10
                        if num_expenses > 0:
                            self.view_expenses(num_expenses)
                            break
                        else:
                            self.mprint("Please enter a positive number.", 3)
                    except ValueError:
                        self.mprint("Invalid input! Please enter a valid number.", 3)
                        
            elif choice == "3":
                self.delete_recent_entry()
                    
            elif choice == "4":
                month_year = str(self.mprint("Enter the month and year (e.g., '2', '12-22', '03 2023', '4/2024'): ")).strip()
                clear_console()
                self.get_monthly_expenses(month_year)

            elif choice == "5":
                self.get_total_entries()
                
            
            else:
                self.mprint("Invalid choice! Please try again.", 3)


if __name__ == "__main__":
    tracker = ExpenseTracker()
    try:
        tracker.json_handler.ensure_json_file(tracker.file_name, [])
    except Exception as e:
        print(f"Error creating JSON file: {e}")
        exit(1)
    tracker.run()