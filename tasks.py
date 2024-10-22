from globals import datetime, json, os, pytz
from globals import tasks_db_json_path

class Task:
    def __init__(self, description, category, priority=1, completed=False, created_at=None):
        self.description = description
        self.category = category.lower()  # Store categories in lowercase
        self.priority = priority
        self.completed = completed
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now(pytz.timezone("Asia/Calcutta")).strftime('%d/%m/%y %H:%M:%S')

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            description=task_dict['description'],
            category=task_dict['category'],
            priority=task_dict['priority'],
            completed=task_dict['completed'],
            created_at=task_dict['created_at']
        )

    def __str__(self):
        return f"[{'X' if self.completed else ' '}] {self.description} ({self.category}) - Priority: {self.priority} - Added: {self.created_at}"


class TaskManager:
    def __init__(self, filename=tasks_db_json_path):
        self.tasks = []
        self.filename = filename
        self.total_tasks_added = 0
        self.total_tasks_completed = 0
        self.load_tasks()

    def add_task(self, description, category, priority=1):
        task = Task(description, category, priority)
        self.tasks.append(task)
        self.total_tasks_added += 1  # Increment total tasks added count
        self.save_tasks()
        print(f"Task added: {description} to {category} category with priority {priority}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks for today!")
        else:
            print("\nToday's Tasks:")
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task}")
            # Display total tasks added and completed
            print(f"\nTotal tasks added: {self.total_tasks_added}")
            print(f"Total tasks completed: {self.total_tasks_completed}")

    def view_pending_tasks(self):
        pending_tasks = [task for task in self.tasks if not task.completed]
        if not pending_tasks:
            print("No pending tasks!")
        else:
            print("\nPending Tasks:")
            for i, task in enumerate(pending_tasks, 1):
                print(f"{i}. {task}")
        return pending_tasks

    def view_tasks_by_category(self, category):
        category = category.lower()  # Normalize the category for comparison
        tasks_in_category = [task for task in self.tasks if task.category == category]
        if not tasks_in_category:
            print(f"No tasks in the '{category}' category!")
        else:
            print(f"\nTasks in '{category}' category:")
            for i, task in enumerate(tasks_in_category, 1):
                print(f"{i}. {task}")

    def get_categories(self):
        return list(set(task.category for task in self.tasks))

    def show_categories(self):
        categories = self.get_categories()
        if categories:
            print("\nExisting categories:")
            for index, category in enumerate(categories, 1):
                print(f"{index}. {category}")
        else:
            print("No categories available.")

    def select_category(self):
        self.show_categories()
        existing_categories = {cat.lower(): cat for cat in self.get_categories()}

        try:
            category_choice = int(input("Select a category by number (or enter 0 to create a new one): "))
            if category_choice == 0:
                new_category = input("Enter the new category name (in lowercase): ").lower()
                if new_category in existing_categories:
                    print(f"Category '{new_category}' already exists. Task will be added to this category.")
                    return new_category
                return new_category
            elif 1 <= category_choice <= len(existing_categories):
                return existing_categories[list(existing_categories.keys())[category_choice - 1]]
            else:
                print("Invalid choice! Would you like to create a new category? (y/n): ")
                if input().lower() == 'y':
                    new_category = input("Enter the new category name (in lowercase): ").lower()
                    if new_category in existing_categories:
                        print(f"Category '{new_category}' already exists. Task will be added to this category.")
                        return new_category
                    return new_category
                else:
                    return None
        except ValueError:
            print("Please enter a valid number.")
            return None

    def mark_task_completed(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1].mark_completed()
            self.total_tasks_completed += 1  # Increment completed tasks count
            self.save_tasks()
            print(f"Task {task_number} marked as completed.")
        else:
            print("Invalid task number!")

    def mark_pending_task_completed(self):
        pending_tasks = self.view_pending_tasks()
        if not pending_tasks:
            return  # No pending tasks to mark as completed

        try:
            task_number = int(input("Enter task number to mark as completed: "))
            if 0 < task_number <= len(pending_tasks):
                selected_task = pending_tasks[task_number - 1]
                self.tasks[self.tasks.index(selected_task)].mark_completed()
                self.total_tasks_completed += 1  # Increment completed tasks count
                self.save_tasks()
                print(f"Task '{selected_task.description}' marked as completed.")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number.")

    def remove_completed_tasks(self):
        self.tasks = [task for task in self.tasks if not task.completed]
        self.save_tasks()
        print("All completed tasks removed!")

    def save_tasks(self):
        """Saves tasks along with the total number of tasks added and completed to the JSON file."""
        with open(self.filename, 'w') as f:
            data = {
                "tasks": [task.to_dict() for task in self.tasks],
                "total_tasks_added": self.total_tasks_added,
                "total_tasks_completed": self.total_tasks_completed
            }
            json.dump(data, f, indent=4)
        print(f"Tasks saved to {self.filename}")

    def load_tasks(self):
        """Loads tasks and stats (total_tasks_added and total_tasks_completed) from the JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                tasks_as_dict = data.get("tasks", [])
                self.tasks = [Task.from_dict(task) for task in tasks_as_dict]
                self.total_tasks_added = data.get("total_tasks_added", 0)
                self.total_tasks_completed = data.get("total_tasks_completed", 0)
            print(f"Tasks loaded from {self.filename}")
        else:
            print("No existing tasks found, starting fresh.")


def main():
    manager = TaskManager()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Tasks by Category")
        print("4. Mark Task as Completed")
        print("5. Remove Completed Tasks")
        print("6. View All Existing Categories")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            task_description = input("Enter task description: ")
            task_category = manager.select_category()
            if task_category:
                priority_input = input("Enter task priority (1-5) or press Enter for default (1): ")
                priority = 1
                if priority_input:
                    try:
                        priority = int(priority_input)
                        if priority < 1 or priority > 5:
                            print("Invalid priority! Please enter a number between 1 and 5.")
                            continue
                    except ValueError:
                        print("Invalid input! Using default priority (1).")
                manager.add_task(task_description, task_category, priority)
            else:
                print("Task not added due to invalid category selection.")
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            category = input("Enter category to view: ").lower()
            manager.view_tasks_by_category(category)
        elif choice == '4':
            manager.mark_pending_task_completed()
        elif choice == '5':
            manager.remove_completed_tasks()
        elif choice == '6':
            manager.show_categories()
        elif choice == '7':
            print("Exiting task manager.")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
