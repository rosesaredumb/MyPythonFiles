from datetime import timedelta
from globals import datetime, json, os, pytz, re
from globals import tasks_db_json_path, time_format, time_zone, clear_console
from json_functions import json_funcs
from level_system import get_or_create_player
from typing import Literal

class MyTasks:
    def __init__(self):
        self.player = get_or_create_player()
        self.xp_for_adding_task = 200
        self.bulletins = {"input": ">>>", "response": "--", "error": "!!"}
        self.json_helper = self._initialize_json_helper()
        if self.json_helper is None:
            raise RuntimeError("json_funcs initialization failed.")
        self.filepath = self._initialize_filepath()
        self.json_format = {"tasks": [], "total_no_of_tasks_added": 0, "total_no_of_tasks_completed": 0}
        self.data = self._load_or_initialize_data()

    def _initialize_json_helper(self):
        try:
            return json_funcs()  # Assuming json_funcs is a callable class/function
        except Exception as e:
            print(f"Error initializing json_funcs: {e}")
            return None

    def _initialize_filepath(self):
        if not tasks_db_json_path:
            print("Invalid file path for tasks_db_json_path.")
            return None
        return tasks_db_json_path

    def _load_or_initialize_data(self):
        if self.json_helper and self.filepath:
            self.json_helper.ensure_json_file(self.filepath, self.json_format)
            return self.json_helper.read_json(self.filepath) or self.json_format
        print("Error loading data.")
        return self.json_format

    # Other methods remain unchanged...

    def mprint(self, sentence: str, type: Literal[1, 2, 3] = 1) -> str:
        bulletin = self.bulletins.get({1: "input", 2: "response", 3: "error"}.get(type, "input"))
        return input(f"{bulletin}{sentence}") if type == 1 else print(f"{bulletin}{sentence}") or ""

    def task_print_format(self, idx, task, status=False, date_diff=False):
        bullet = self.bulletins["response"]
        task_str = (
            f"{idx}. {task['description']}\n"
            f"{bullet}Priority: {task['priority']}\n"
            f"{bullet}Category: {task.get('category', '>ungrouped<')}\n"
            f"{bullet}Created: {task['created_date']}\n"
            f"{bullet}Due: {task.get('due_date', '>no due date<')}\n"
        )
        if status:
            task_str += f"{bullet}Status: {'completed' if task['status'] else 'pending'}\n"
        if date_diff:
            task_str += f"{bullet}Time left: {self.get_date_difference(task) or ''}\n"
        print(task_str)

    def _input_with_fallback(self, prompt, fallback=""):
        response = self.mprint(prompt)
        return response if response.strip() else fallback

    def add_task(self):
        task_description = self._input_with_fallback("Type task description: ").strip()
        chosen_category = self._choose_or_create_category()
        priority = int(self._input_with_fallback("Type task priority (1-5) or press Enter for default (1): ", "1"))
        created_date = datetime.now(pytz.timezone(time_zone)).strftime(time_format)
        due_date = self._parse_due_date(self.mprint("Type due date (dd/mm/yyyy - hh:mm) or press Enter to skip: "))

        new_task = {"description": task_description, "status": False, "priority": priority,
                    "category": chosen_category, "created_date": created_date, "due_date": due_date}
        self._save_task(new_task)
        self.player.gain_xp(self.xp_for_adding_task)

    def _choose_or_create_category(self):
        categories = self.view_categories()
        if categories:
            print("Choose a category:")
            for idx, cat in enumerate(categories, 1):
                print(f"{idx} - {cat}")
            choice = self._input_with_fallback("Type a number to choose the category or '0' to create new: ")
            if choice.isdigit():
                return self._handle_category_choice(int(choice), categories)
        return None

    def _handle_category_choice(self, choice, categories):
        if choice == 0:
            new_category = self._input_with_fallback("Type new category name: ").lower()
            return new_category if new_category not in categories else None
        elif 1 <= choice <= len(categories):
            return categories[choice - 1]

    def _parse_due_date(self, date_str):
        if not date_str.strip():
            return None
        try:
            day, month, year, hour, minute = [int(part) for part in re.split(r"[-/\\' ;]", date_str)] + [0, 0, 0, 0, 0]
            return datetime(year, month, day, hour, minute).strftime(time_format)
        except ValueError:
            self.mprint("Invalid due date format! Skipping due date.\n", 3)

    def _save_task(self, task):
        self.data["tasks"].append(task)
        self.data["total_no_of_tasks_added"] += 1
        if self.json_helper:  # Check if json_helper is not None
            self.json_helper.write_json(self.data, self.filepath)
            self.mprint("Task added successfully!\n", 2)
        else:
            print("Error saving task: json_helper not initialized.")

    def view_categories(self):
        return list({task["category"] for task in self.data["tasks"] if task["category"]})

    def view_tasks(self):
        for idx, task in enumerate(self.data["tasks"], 1):
            self.task_print_format(idx, task, status=True, date_diff=True)

    def mark_task_as_completed(self):
        pending_tasks = [t for t in self.data["tasks"] if not t["status"]]
        for idx, task in enumerate(pending_tasks, 1):
            self.task_print_format(idx, task)
        task_idx = int(self.mprint("Type the task number to mark as completed: ")) - 1
        if 0 <= task_idx < len(pending_tasks):
            pending_tasks[task_idx]["status"] = True
            self.data["total_no_of_tasks_completed"] += 1
            if self.json_helper:  # Check if json_helper is not None
                self.json_helper.write_json(self.data, self.filepath)
                self.mprint("Task added successfully!\n", 2)
            else:
                print("Error saving task: json_helper not initialized.")

    def get_date_difference(self, task):
        created_date = datetime.strptime(task["created_date"], time_format)
        due_date = datetime.strptime(task["due_date"], time_format) if task["due_date"] else None
        if due_date:
            delta = due_date - created_date
            return f"{delta.days} days, {delta.seconds // 3600} hours, {delta.seconds // 60 % 60} minutes"

def main():
    manager = MyTasks()
    actions = {
        '1': manager.add_task,
        '2': manager.view_tasks,
        '3': manager.mark_task_as_completed,
        '4': manager.view_categories,
        '5': manager.get_date_difference
    }
    while True:
        choice = input("Choose an option (1. Add Task, 2. View Tasks, 3. Complete Task, 4. View Categories, 5. Quit): ")
        clear_console()
        if choice == '5':
            print("Exiting.")
            break
        elif choice in ['2', '3']:
            # Get task number before proceeding to mark as completed or view tasks
            manager.view_tasks()
            task_idx = int(manager.mprint("Type the task number for further action (or 0 to cancel): ")) - 1
            if choice == '2' and task_idx >= 0:
                manager.task_print_format(task_idx + 1, manager.data["tasks"][task_idx], status=True, date_diff=True)
            elif choice == '3' and task_idx >= 0:
                manager.data["tasks"][task_idx]["status"] = True
                manager.data["total_no_of_tasks_completed"] += 1
                if manager.json_helper:
                    manager.json_helper.write_json(manager.data, manager.filepath)
                else:
                    print("Error: json_helper is not initialized, task status not updated.")
                manager.mprint("Task marked as completed!\n", 2)
        else:
            actions.get(choice, lambda: print("Invalid choice"))()

if __name__ == "__main__":
    main()