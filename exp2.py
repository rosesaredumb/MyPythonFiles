from datetime import datetime
from json_functions import json_funcs
import re
from globals import expenses_db_json_path


class ExpenseTracker:
    def __init__(self):
        self.file_name = expenses_db_json_path
        self.json_handler = json_funcs()
        self.expenses = self.load_expenses()
        self.categories = self.get_all_categories(
        )  # Initialize categories list

    
    def sort_expenses_by_date(self):
        """Sort the expenses from oldest to newest date."""
        def parse_date(date_str):
            return datetime.strptime(date_str, "%d/%m/%Y")

        # Sort the expenses list by the 'date' field
        self.expenses.sort(key=lambda expense: parse_date(expense['date']))
        print("Expenses sorted by date (oldest to newest).")
        self.save_expenses()

    
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
            if not date_input.strip(
            ):  # If the input is empty, return today's date
                # Get today's date
                day = datetime.now().day
                month = datetime.now().month
                year = datetime.now().year
            else:
                # Extract numeric parts from the input
                date_parts = [
                    int(part) for part in re.split(r"[-/\\' ;]", date_input)
                    if part.isdigit()
                ]
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
            datetime.strptime(full_date,
                              "%d/%m/%Y")  # Ensure it's a valid date
            return full_date  # Return corrected date
        except (ValueError, IndexError):
            return None  # Return None for invalid date inputs

    def validate_amount(self, amount):
        """Validate the amount."""
        try:
            return f"{float(amount):.2f}"
        except ValueError:
            return None

    def get_all_categories(self):
        """Get all unique categories from expenses."""
        categories = set()
        for expense in self.expenses:
            if expense["category"]:  # Ensure category is not None or empty
                categories.add(expense["category"].lower()
                               )  # Normalize category to lowercase
        return sorted(categories)

    def add_expense(self, date, amount, category, reason):
        """Add a new expense entry."""
        if not self.validate_date(date):
            print("Invalid date format! Please try again.")
            return

        expense = {
            "date": date,
            "amount": amount,
            "category": category,
            "reason": reason
        }
        self.expenses.append(expense)
        self.sort_expenses_by_date()
        self.categories = self.get_all_categories()  # Refresh categories after adding expense
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
            del self.expenses[index - 1]
            self.sort_expenses_by_date()
            self.categories = self.get_all_categories(
            )  # Refresh categories after deleting expense
            print("Expense deleted successfully!")
        except IndexError:
            print("Invalid index. Please try again.")

    def select_category(self):
        """Allow the user to select an existing category or create a new one."""
        while True:  # Loop until a valid choice is made
            if not self.categories:
                print("")
                category_input = input(
                    "\nNo categories available."
                    "\nEnter 0 to create a new category / Press -Enter- to assign no category."
                    "\nEnter your choice: ").strip()
                if category_input == '0':
                    while True:
                        category = input(
                            "\nEnter the new category: ").strip().lower()
                        if category == '':
                            print(
                                "\nCategory name cannot be empty. Please enter a valid category."
                            )
                        elif category not in self.categories:
                            self.categories.append(category)
                            print(f"\nCategory '{category}' created!")
                            break
                        else:
                            print(f"\nCategory '{category}' already exists.")
                elif category_input == '':  # If no input is provided
                    category = None
                    print("No category assigned.")
                    break  # Exit the loop if 'None' is chosen
                else:
                    print("Invalid choice. Please try again.")
            else:
                category_input = input(
                    f"\nExisting categories:\n{''.join([f'{idx}. {cat}\n' for idx, cat in enumerate(self.categories, 1)])}"
                    f"\nSelect category by entering number (1 - {len(self.categories)})"
                    "/ Enter 0 to create a new category / Press -Enter- to assign no category.\n"
                ).strip()
                if category_input == '0':
                    while True:
                        category = input(
                            "\nEnter new category: ").strip().lower()
                        if category == '':
                            print(
                                "\nCategory cannot be empty. Please enter a valid category."
                            )
                        elif category not in self.categories:
                            self.categories.append(category)
                            print(f"Category '{category}' created!"
                                  )  # Add new category
                            break  # Exit the loop if a valid category is created
                        else:
                            print(f"Category '{category}' already exists.")
                            break
                elif category_input == '':  # If no input is provided
                    category = None
                    print("No category assigned.")
                    break  # Exit the loop and assign 'None' category
                else:
                    try:
                        category_index = int(category_input)
                        if 1 <= category_index <= len(self.categories):
                            category = self.categories[category_index - 1]
                            break  # Exit the loop if a valid category is selected
                        else:
                            print("Invalid choice. Please try again.")
                    except ValueError:
                        print("Invalid input. Assigning 'None' category.")
                        category = None
                        break  # Exit the loop if the input is invalid
        return category

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
                while True:
                    date_input = input(
                        "\nEnter the date (dd/mm/yyyy) / Press Enter for today: "
                    ).strip()
                    corrected_date = self.validate_date(date_input)

                    if not corrected_date:
                        print("Invalid date format! Please try again.")
                    else:
                        print(f"Corrected date: {corrected_date}")
                        break  # Exit the loop if the date is valid

                # Amount validation loop
                while True:
                    amount = input("\nEnter the amount: ").strip()
                    if self.validate_amount(amount):
                        break  # Exit the loop if the amount is valid
                    else:
                        print("\nInvalid amount! Please enter a valid number.")

                category = self.select_category()
                reason = input("\nEnter the reason: ").strip() or None
                self.add_expense(corrected_date, self.validate_amount(amount), category, reason)

            elif choice == "2":
                self.view_expenses()

            elif choice == "3":
                self.view_expenses()
                index = int(
                    input("Enter the index of the expense to delete: "))
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
