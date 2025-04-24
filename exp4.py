from datetime import datetime
from json_functions import json_funcs
import re
from globals import expenses_db_json_path, clear_console
from typing import Literal
from dateutil.relativedelta import relativedelta
import inspect


class ExpenseTracker:

    def __init__(self):
        self.file_name = expenses_db_json_path
        self.json_handler = json_funcs()
        try:
            self.ensure_exist = self.json_handler.ensure_json_file(expenses_db_json_path, [])
        except Exception as e:
            print(f"Error creating JSON file: {e}")
            exit(1)
        self.expenses = self.load_expenses()
        self.categories = self.get_all_categories()
        self.input_bulletin = ">>"
        self.response_bulletin = "--"
        self.error_bulletin = "!!"
        self.expense_entry_format = "Date: {}\nAmount: {:.2f}\nCategory: {}\nReason: {}"

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
        self.expenses.sort(
            key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))
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

    def validate_amount(self, amount=None):
        """Validate and format the amount."""
        if amount is None:  # Check if no input is provided
            self.mprint("No input provided!", 3)
            return None
        try:
            checked_amount = round(float(amount), 2)
            if checked_amount < 0:
                self.mprint("Invalid input! Type a positive number.", 3)
                return None
            return checked_amount
        except ValueError:
            self.mprint("Invalid input! Type a valid number.", 3)
            return None

    def get_all_categories(self):
        """Get all unique categories from expenses."""
        categories = set()
        for expense in self.expenses:
            if expense["category"]:  # Ensure category is not None or empty
                categories.add(expense["category"].lower())
        return sorted(categories)

    def add_expense(self):
        """Add a new expense"""
        while True:
            date_input = str(
                self.mprint(
                    "Type the date (dd/mm/yyyy) / Press -Enter- for today: ")
            ).strip()
            date = self.validate_date(date_input)
            if date:
                self.mprint(f"Date set as: {date}", 2)
                break
            self.mprint("Invalid date format! Please try again.", 3)

        while True:
            amount = self.mprint("Type the amount: ").strip()
            formatted_amount = self.validate_amount(amount)
            if formatted_amount:
                self.mprint(f"Amount set as: {formatted_amount:.2f}", 2)
                break     

        category = self.select_category()
        self.mprint(f"Category set as: {category or '>no category<'}", 2)

        reason = str(
            self.mprint("Type the reason / Press -Enter- to assign no reason: "
                        )).strip() or None
        clear_console()

        expense = {
            "date": date,  # Validated date passed as argument
            "amount": formatted_amount,  # Validated amount passed as argument
            "category": category,  # Category can be None or valid input
            "reason": reason  # Reason can be None or valid input
        }
        self.expenses.append(expense)
        self.save_expenses()
        self.mprint("Entry added successfully!", 2)
        print(
            self.expense_entry_format.format(date, formatted_amount, category
                                             or '>no category<', reason
                                             or '>no reason<'))

    def view_expenses(self):
        """
        View recent expenses
        
        View the specified number of latest expenses or all expenses if none specified.
        Prompts the user to enter the number of latest expenses to display.
        """
        if not self.expenses:
            self.mprint("No expenses recorded yet.", 3)
            return

        try:
            # Prompt user for the number of expenses to display
            num_expenses_input = str(
                self.mprint(
                    "Type the number of latest expenses to view / press -Enter- for default 20: "
                )).strip()
            clear_console()
            num_expenses = int(
                num_expenses_input) if num_expenses_input else 20

            if num_expenses > 0:
                self.mprint(f"Displaying the last {num_expenses} expenses:\n",
                            2)
                print(
                    f"{'Date':<12} {'Amount':>10}    {'Category':<20} {'Reason':<30}"
                )
                print("-" * 80)
                for expense in self.expenses[-num_expenses:]:
                    date = expense.get("date", ">no date<")
                    amount = f"{expense.get('amount', 0.0):.2f}"
                    category = expense.get("category", None) or ">no category<"
                    reason = expense.get("reason", None) or ">no reason<"
                    print(
                        f"{date:<12} {amount:>10}    {category:<20} {reason:<30}"
                    )
            else:
                self.mprint("Please type a positive number.", 3)
        except ValueError:
            self.mprint("Invalid input! Please type a valid number.", 3)
        except Exception as e:
            self.mprint(f"An unexpected error occurred: {e}", 3)
            return

    def select_category(self):
        """Allow the user to select an existing category or create a new one."""
        while True:
            if not self.categories:
                category_input = self.mprint(
                    "No categories available.\nType 0 to create a new category / Press -Enter- to assign no category: "
                ).strip()
            else:
                categories_list = ''.join([f'{idx}. {cat}\n' for idx, cat in enumerate(self.categories, 1)])
                category_input = input(
                    f"\nExisting categories:\n{categories_list}"
                    f"Select category by number (1-{len(self.categories)}) / "
                    "Type 0 to create a new category / Press -Enter- to assign no category: "
                ).strip()

            if category_input == '0':  # Create a new category
                category = self.mprint("Type the new category: ").strip().lower()
                if category:
                    if category not in self.categories:
                        self.categories.append(category)
                        self.mprint(f"Category '{category}' created!", 2)
                        return category
                    self.mprint("Category already exists.", 2)
                else:
                    self.mprint("Category cannot be empty. Try again.", 3)
            elif not category_input:  # No category
                return None
            else:  # Select existing category
                try:
                    category_index = int(category_input)
                    if 1 <= category_index <= len(self.categories):
                        return self.categories[category_index - 1]
                    self.mprint("Invalid choice. Try again.", 3)
                except ValueError:
                    self.mprint("Invalid input. Try again.", 3)

    def get_specific_month_expenses(self):
        """
        View total expenses for a specific month
        
        Get the total expenses, number of entries, and expenses grouped by category for a specific month and year.
        If no input is provided, use the current month and year.
        Also display the percentage contribution of each category to the total expenses.
        :param month_year_input: Input in formats like 'mm/yyyy', 'mm yy', 'mm,yy', 'mm' (current year assumed).
        :return: Total expenses, number of entries, and a dictionary of expenses grouped by category.
        """
        try:
            month_year_input = str(
                self.mprint(
                    "Type the month and year (mm/yyyy) / Press -Enter- for the current month: "
                )).strip()
            clear_console()
            # Default to current month and year if no input is provided
            if not month_year_input.strip():
                month = datetime.now().month
                year = datetime.now().year
            else:
                # Split input using any non-digit character as a delimiter
                parts = [
                    int(part) for part in re.split(r"[^\d]", month_year_input)
                    if part.isdigit()
                ]

                # Determine month and year based on input length
                if len(parts) == 1:  # Only month provided
                    month = parts[0]
                    year = datetime.now().year  # Default to current year
                elif len(parts) == 2:  # Month and year provided
                    month, year = parts
                    if year < 100:  # Convert two-digit year to four-digit year
                        year += 2000
                else:
                    raise ValueError(
                        "Invalid input format. Provide 'mm/yyyy', 'mm yy', 'mm,yy', or 'mm'."
                    )

                # Validate month
                if not (1 <= month <= 12):
                    raise ValueError(
                        "Invalid month value. Must be between 1 and 12.")

            # Initialize category-wise expenses dictionary
            category_expenses = {}
            num_entries = 0  # Initialize entry counter

            # Calculate total and category-wise expenses
            total_expenses = 0.0
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%d/%m/%Y")
                if expense_date.month == month and expense_date.year == year:
                    total_expenses += expense["amount"]
                    category = expense[
                        "category"] or ">no category<"  # Replace None or empty category
                    category_expenses[category] = category_expenses.get(
                        category, 0) + expense["amount"]
                    num_entries += 1  # Increment entry counter

            total_expenses = round(total_expenses, 2)
            sorted_categories = sorted(category_expenses.items(),
                                       key=lambda x: x[1],
                                       reverse=True)

            # Display results
            self.mprint(
                f"Expense breakdown for {str(month).zfill(2)}/{year} (entries: {num_entries}):\n",
                2)
            print(f"{'Category':<20}  {'Amount':>10}  {'Percentage':>10}")
            print("-" * 60)
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses *
                              100) if total_expenses > 0 else 0
                print(f"{category:<20}  {amount:>10.2f}  {percentage:>9.1f}%")
            print("-" * 60)
            print(f"{'Total':<20}  {total_expenses:>10.2f}")

            return total_expenses, num_entries, dict(sorted_categories)

        except (ValueError, IndexError):
            self.mprint(
                "Invalid input format! Please provide 'mm/yyyy', 'mm yy', 'mm,yy', or 'mm'.",
                3)
            return 0.0, 0, {}

    def get_total_entries(self):
        """
        Display the total number of expense entries
        """
        total_entries = len(self.expenses)
        self.mprint(f"Total no.of expense entries: {total_entries}", 2)
        return total_entries

    def delete_recent_entry(self):
        """
        Delete an expense from the recent entries.
        """
        if not self.expenses:
            self.mprint("No expenses recorded yet.", 3)
            return False  # Indicate no deletion

        while True:
            num_expenses_input = self.mprint(
                "Type the number of latest expenses to view / Press -Enter- for default (20): "
            ).strip()
            clear_console()

            if not num_expenses_input:
                num_expenses = 20
                break
            elif num_expenses_input.isdigit() and int(num_expenses_input) > 0:
                num_expenses = int(num_expenses_input)
                break
            else:
                self.mprint("Invalid input! Type a valid positive number.", 3)

        recent_expenses = self.expenses[-num_expenses:]

        self.mprint(
            f"Most Recent {min(num_expenses, len(recent_expenses))} Entries:",
            2)
        print(
            f"{'Index':<6} {'Date':<10} {'Amount':>10}    {'Category':<20} {'Reason':<30}"
        )
        print("-" * 80)
        for i, expense in enumerate(recent_expenses, start=1):
            date = expense["date"]
            amount = f"{expense['amount']:.2f}"
            category = expense["category"] or ">no category<"
            reason = expense["reason"] or ">no reason<"
            print(
                f"{i:<6} {date:<10} {amount:>10}    {category:<20} {reason:<30}"
            )
        print("-" * 80)

        while True:
            index_input = input(
                f"Type the index of the entry to delete (1-{len(recent_expenses)}) / Type 0 to cancel: "
            ).strip()
            if not index_input.isdigit():
                self.mprint("Invalid input! Type a valid number.", 3)
                continue

            index = int(index_input)
            if index == 0:
                self.mprint("Deletion canceled.", 2)
                return False  # Indicate cancellation
            elif 1 <= index <= len(recent_expenses):
                actual_index = len(
                    self.expenses) - len(recent_expenses) + (index - 1)
                deleted_expense = self.expenses.pop(actual_index)
                try:
                    self.save_expenses()
                except Exception as e:
                    self.mprint(f"Error saving expenses: {e}", 3)
                    return False  # Indicate failure to save
                # Only if you don't update self.categories when removing an expense
                self.categories = self.get_all_categories()
                self.mprint("Deleted entry!", 2)
                print(
                    self.expense_entry_format.format(
                        deleted_expense['date'], deleted_expense['amount'],
                        deleted_expense['category'],
                        deleted_expense['reason']))

                return True  # Indicate successful deletion
            else:
                self.mprint(
                    f"Invalid index! Type a number between 1-{len(recent_expenses)}.",
                    3)

    def get_monthly_expenses(self):
        """
        View total expense for the specified number of months
        
        Display the total expenses and the number of entries for each of the last 'num_months' months.
        Returns:
            - expenses_by_month: Dictionary with keys as (month, year) and values as total expense.
            - total_sum: Total of all expenses in the last 'num_months' months.
            - entries_by_month: Dictionary with keys as (month, year) and values as the count of entries.
        """
        if not self.expenses:
            self.mprint("No expenses recorded yet.", 3)
            return {}, 0, {}
        try:
            num_months_input = str(
                self.mprint(
                    "Type the number of months to view / Press -Enter- for default (12): "
                )).strip()
            clear_console()
            num_months = int(num_months_input) if num_months_input else 12

            if num_months <= 0:
                self.mprint("Invalid input! Type a positive number.", 3)
                return

            current_date = datetime.now()
            expenses_by_month = {}
            entries_by_month = {}

            # Initialize months and calculate totals
            for i in range(num_months):
                month_date = current_date - relativedelta(months=i)
                month_year = (month_date.month, month_date.year)
                expenses_by_month[month_year] = 0.0
                entries_by_month[month_year] = 0

            # Aggregate expenses and entry counts
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%d/%m/%Y")
                month_year = (expense_date.month, expense_date.year)
                if month_year in expenses_by_month:
                    expenses_by_month[month_year] += expense["amount"]
                    entries_by_month[month_year] += 1

            # Calculate the total sum
            total_sum = sum(expenses_by_month.values())

            # Sort and display results
            sorted_months = sorted(expenses_by_month.items(),
                                   key=lambda x: (x[0][1], x[0][0]),
                                   reverse=True)
            self.mprint(
                f"Total expenses for the last {num_months} month(s):\n", 2)
            print(f"{'Month/Year':<15}  {'Amount':>10}  {'Entries':>8}")
            print("-" * 40)
            for (month, year), amount in sorted_months:
                month_year_str = f"{str(month).zfill(2)}/{year}"
                num_entries = entries_by_month.get((month, year), 0)
                print(
                    f"{month_year_str:<15}  {amount:>10.2f}  {num_entries:>8}")
            print("-" * 40)
            print(f"{'Total':<15}  {total_sum:>10.2f}")
            return expenses_by_month, total_sum, entries_by_month
        except ValueError:
            self.mprint(
                "Invalid input. Please type a positive integer for the number of months.",
                3)
        except Exception as e:
            self.mprint(f"An unexpected error occurred: {e}", 3)
            return {}, 0, {}

    def modify_expense(self):
        """
        Modify an expense's category, amount, or reason.

        Allows the user to select an expense from the recent entries and choose 
        which field to modify (category, amount, or reason).
        """
        if not self.expenses:
            self.mprint("No expenses recorded yet.", 3)
            return

        while True:
            # Prompt user for the number of recent expenses to display
            num_expenses_input = self.mprint(
                "Type the number of latest expenses to view / Press -Enter- for default (20): "
            ).strip()
            clear_console()

            if not num_expenses_input:
                num_expenses = 20  # Default to 20 if input is empty
                break
            elif num_expenses_input.isdigit() and int(num_expenses_input) > 0:
                num_expenses = int(num_expenses_input)
                break
            else:
                self.mprint(
                    "Invalid input! Type a valid positive number.", 3)

        recent_expenses = self.expenses[-num_expenses:]
        print(f"\nMost Recent {num_expenses} Entries (or fewer):")
        print(
            f"{'Index':<6} {'Date':<10} {'Amount':>10}    {'Category':<20} {'Reason':<30}"
        )
        print("-" * 80)
        for i, expense in enumerate(recent_expenses, start=1):
            date = expense["date"]
            amount = f"{expense['amount']:.2f}"
            category = expense["category"] or ">no category<"
            reason = expense["reason"] or ">no reason<"
            print(
                f"{i:<6} {date:<10} {amount:>10}    {category:<20} {reason:<30}"
            )
        print("-" * 80)

        # Prompt user to select an expense by index
        while True:
            try:
                index = int(
                    self.mprint(
                        f"Type the index of the entry to modify (1-{num_expenses}) / Type 0 to cancel: "
                    ).strip())
                if index == 0:
                    self.mprint("Operation canceled.", 2)
                    return
                if 1 <= index <= len(recent_expenses):
                    # Calculate actual index in the full expense list
                    actual_index = len(
                        self.expenses) - len(recent_expenses) + (index - 1)
                    break
                else:
                    self.mprint(
                        f"Invalid index! Type a number between 1-{len(recent_expenses)}.",
                        3)
            except ValueError:
                self.mprint("Invalid input! Type a valid number.", 3)

        # Allow user to choose which field to modify
        while True:
            field_choice = self.mprint(
                "What do you want to modify?\n0. ~To cancel operation\n1. Amount\n2. Category\n3. Reason\nType the index of the option: "
            ).strip()
            if field_choice == "0":
                self.mprint("Operation canceled.", 2)
                return
            elif field_choice == "1":  # Modify amount
                current_amount = self.expenses[actual_index]["amount"]
                self.mprint(f"Current amount: {current_amount:.2f}", 2)
                new_amount = self.mprint("Enter the new amount: ").strip()
                formatted_amount = self.validate_amount(new_amount)
                if formatted_amount:
                    self.expenses[actual_index][
                            "amount"] = formatted_amount
                    self.mprint(
                            f"Amount updated to: {formatted_amount:.2f}", 2)
                    break
            elif field_choice == "2":  # Modify category
                current_category = self.expenses[actual_index]["category"]
                self.mprint(
                    f"Current category: {current_category or '>no category<'}",
                    2)
                new_category = self.select_category()
                if new_category != current_category:
                    self.expenses[actual_index]["category"] = new_category
                    self.mprint(f"Category updated to: {new_category}", 2)
                    break
                else:
                    self.mprint("No changes were made to the category.", 2)
                    return
            elif field_choice == "3":  # Modify reason
                current_reason = self.expenses[actual_index]["reason"]
                self.mprint(
                    f"Current reason: {current_reason or '>no reason<'}", 2)
                new_reason = self.mprint("Type the new reason: ").strip()
                if new_reason:
                    self.expenses[actual_index]["reason"] = new_reason
                    self.mprint(f"Reason updated to: {new_reason}", 2)
                    break
                else:
                    self.mprint("Reason cannot be empty.", 3)
            else:
                self.mprint("Invalid choice! Type a valid index.", 3)
        self.save_expenses()
        self.mprint("Expense updated successfully.", 2)
        updated_expense = self.expenses[actual_index]
        print(
            self.expense_entry_format.format(updated_expense['date'],
                                             updated_expense['amount'],
                                             updated_expense['category'],
                                             updated_expense['reason']))

    def run(self):
        """Main menu to run the Expense Tracker."""
        self.mprint("Welcome to the Expense Tracker!", 2)
        while True:
            # Display the menu
            print("\n0. Exit")
            specific_functions = self.get_specific_functions()
            for index, (_, _, doc) in enumerate(specific_functions, start=1):
                print(f"{index}) {doc}")

            # Get user choice
            choice = input("Enter your choice: ").strip()
            clear_console()

            if choice == "0":
                self.mprint("Exiting the Expense Tracker. Goodbye!", 2)
                break

            # Handle valid function choices
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(specific_functions):
                    func = specific_functions[choice][1]
                    getattr(self, func)()  # Call the selected function
                else:
                    self.mprint("Invalid choice! Try again.", 3)
            except ValueError:
                self.mprint("Invalid input! Type a valid number.", 3)

    def get_specific_functions(self):
        """
        Retrieve a list of specific functions with their indices, names, and a brief description.

        Returns:
            list of tuple: A list where each tuple contains:
                - Index (int): The position of the function in the predefined list.
                - Function Name (str): The name of the function.
                - Description (str): The first line of the function's docstring or a default message.
        """
        # Define the specific functions to retrieve
        function_names = [
            'add_expense', 'view_expenses', 'delete_recent_entry',
            'get_specific_month_expenses', 'get_monthly_expenses',
            'get_total_entries', 'modify_expense'
        ]  # Adjust as needed

        # Retrieve all methods of the class
        functions = inspect.getmembers(self, predicate=inspect.ismethod)

        # Map function names to their objects
        function_dict = {name: func for name, func in functions}

        # Retrieve only the specific functions, maintaining the desired order
        result = []
        for i, name in enumerate(function_names):
            if name in function_dict:
                docstring = function_dict[name].__doc__
                description = docstring.strip().splitlines(
                )[0] if docstring else "No description available"
                result.append((i, name, description))
            else:
                # Optional: Log or handle missing functions
                pass

        return result


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
