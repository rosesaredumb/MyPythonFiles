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