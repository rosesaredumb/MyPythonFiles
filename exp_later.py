    def edit_expense(self, index, date, amount, category, reason):
        """Edit an expense by index."""
        try:
            expense = self.expenses[index-1]
            expense["date"] = date
            expense["amount"] = float(amount)
            expense["category"] = category
            expense["reason"] = reason
            self.save_expenses()
            print("Expense edited successfully!")
        except IndexError:
            print("Invalid index. Please try again.")

elif choice == "4":
self.view_expenses()
index = int(input("Enter the index of the expense to edit: "))
date = input("Enter the new date (dd/mm/yyyy): ")
amount = input("Enter the new amount: ")
category = input("Enter the new category (e.g., food, phone, etc.): ")
reason = input("Enter the new reason: ")
self.edit_expense(index, date, amount, category, reason)