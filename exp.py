from datetime import datetime
from json_functions import json_funcs
import re
from globals import expenses_db_json_path


class ExpenseTracker:
    def __init__(self):
        self.file_name = expenses_db_json_path
        self.json_handler = json_funcs()
        self.expenses = self.load_expenses()

    def load_expenses(self):
        """Load expenses from the JSON file."""
        data = self.json_handler.read_json(self.file_name)
        if data is None:
            return []
        return data

    def save_expenses(self):
        """Save expenses to the JSON file."""
        self.json_handler.write_json(self.expenses, self.file_name)

    def validate_date(self, date_input):
        """Validate the date format and auto-correct short formats like '2' to '02/current_month/current_year'."""
        try:
            if date_input.strip():  # Ensure input is not empty
                # Extract numeric parts from the input
                date_parts = [int(part) for part in re.split(r"[-/\\' ;]", date_input) if part.isdigit()]

                # Handle different cases of input
                if len(date_parts) == 1:  # Single digit input (day only)
                    day = date_parts[0]
                    month = datetime.now().month
                    year = datetime.now().year
                elif len(date_parts) == 2:  # Day and month provided
                    day, month = date_parts
                    year = datetime.now().year
                elif len(date_parts) == 3:  # Day, month, and year provided
                    day, month, year = date_parts
                    if year < 100:  # Expand two-digit year to four-digit year
                        year += 2000 if year <= 99 else 0
                else:
                    return None  # Invalid format if more than 3 parts

                # Construct and validate the full date
                full_date = f"{str(day).zfill(2)}/{str(month).zfill(2)}/{year}"
                datetime.strptime(full_date, "%d/%m/%Y")  # Ensure it's a valid date
                return full_date  # Return corrected date
            else:
                return None  # Empty input is invalid
        except (ValueError, IndexError):
            return None  # Return None for invalid date inputs

    def validate_amount(self, amount):
        """Validate the amount."""
        try:
            float(amount)
            return True
        except ValueError:
            return False

    def add_expense(self, date, amount, category, reason):
        """Add a new expense entry."""
        if not self.validate_date(date):
            print("Invalid date format! Please try again.")
            return
        if not self.validate_amount(amount):
            print("Invalid amount! Please enter a number.")
            return
        if not category or not reason:
            print("Please enter a category and reason.")
            return

        expense = {
            "date": date,
            "amount": round(float(amount), 2),
            "category": category,
            "reason": reason
        }
        self.expenses.append(expense)
        self.save_expenses()
        print("Expense added successfully!")

    def view_expenses(self):
        """View all expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
        else:
            for index, expense in enumerate(self.expenses):
                print(f"{index+1}. {expense}")

    def delete_expense(self, index):
        """Delete an expense by index."""
        try:
            del self.expenses[index-1]
            self.save_expenses()
            print("Expense deleted successfully!")
        except IndexError:
            print("Invalid index. Please try again.")

    

    def run(self):
        print("Welcome to the Expense Tracker!")
        while True:
            print("\n0. Exit")
            print("1. Add a new expense")
            print("2. View all expenses")
            print("3. Delete an expense")
            choice = input("Enter your choice: ")

            if choice == "0":
                print("Exiting the Expense Tracker. Goodbye!")
                break
                
            elif choice == "1":
                date_input = input("Enter the date (dd/mm/yyyy) or press Enter for today: ").strip()
                corrected_date = self.validate_date(date_input)
                if not corrected_date:
                    print("Invalid date format! Please try again.")
                else:
                    print(f"Corrected date: {corrected_date}")
                amount = input("Enter the amount: ")
                category = input("Enter the category (e.g., food, phone, etc.): ")
                reason = input("Enter the reason: ")
                self.add_expense(corrected_date, amount, category, reason)

            elif choice == "2":
                self.view_expenses()

            elif choice == "3":
                self.view_expenses()
                index = int(input("Enter the index of the expense to delete: "))
                self.delete_expense(index)

            

            

            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    try:
        tracker.json_handler.ensure_json_file(tracker.file_name, [])
    except Exception as e:
        print(f"Error creating JSON file: {e}")
        exit(1)
    tracker.run()