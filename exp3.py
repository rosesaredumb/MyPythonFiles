from datetime import datetime
from json_functions import json_funcs
import re
from globals import expenses_db_json_path


class ExpenseTracker:
    def __init__(self):
        self.file_name = expenses_db_json_path
        self.json_handler = json_funcs()
        self.expenses = self.load_expenses()
        self.categories = self.get_all_categories()  # Initialize categories list

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
            return f"{float(amount):.2f}"
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
        print("Expense added successfully!")

    def view_expenses(self):
        """View all expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
        else:
            for index, expense in enumerate(self.expenses):
                category = expense["category"] if expense["category"] else ">no category<"
                reason = expense["reason"] if expense["reason"] else ">no reason<"
                print(f"{index+1}. Date: {expense['date']}, Amount: {expense['amount']}, "
                      f"Category: {category}, Reason: {reason}")

    def delete_expense(self, index):
        """Delete an expense by index."""
        try:
            del self.expenses[index - 1]
            self.save_expenses()
            self.categories = self.get_all_categories()  # Refresh categories
            print("Expense deleted successfully!")
        except IndexError:
            print("Invalid index. Please try again.")

    def select_category(self):
        """Allow the user to select an existing category or create a new one."""
        while True:
            if not self.categories:
                category_input = input(
                    "\nNo categories available. "
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
                    print("Invalid choice. Please try again.")
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

    def run(self):
        print("Welcome to the Expense Tracker!")
        while True:
            print("\n0. Exit")
            print("1. Add a new expense")
            print("2. View all expenses")
            print("3. Delete an expense")
            choice = input("Enter your choice: ").strip()

            if choice == "0":
                print("Exiting the Expense Tracker. Goodbye!")
                break
                
            elif choice == "1":
                while True:
                    date_input = input("Enter the date (dd/mm/yyyy) or press Enter for today: ").strip()
                    corrected_date = self.validate_date(date_input)
                    if corrected_date:
                        
                        break
                    print("Invalid date format! Please try again.")

                while True:
                    amount = input("Enter the amount: ").strip()
                    formatted_amount = self.validate_amount(amount)
                    if formatted_amount:
                        break
                    print("Invalid amount! Please enter a valid number.")

                category = self.select_category()
                reason = input("Enter the reason: ").strip() or None

                self.add_expense(corrected_date, formatted_amount, category, reason)
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.view_expenses()
                try:
                    index = int(input("Enter the index of the expense to delete: ").strip())
                    self.delete_expense(index)
                except ValueError:
                    print("Invalid input. Please enter a number.")
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