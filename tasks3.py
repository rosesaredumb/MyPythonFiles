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
        self.xp_for_completing_task = 350
        self.input_bulletin = ">>>"
        self.response_bulletin = "--"
        self.error_bulletin = "!!"
        try:
            self.json_helper = json_funcs()
        except Exception as e:
            print(f"Error initializing json_funcs: {e}")
            return  # You hcould raise an exception or set it to None, based on your design
        try:
            self.filepath = tasks_db_json_path
            if not self.filepath:
                raise ValueError("Invalid file path for tasks_db_json_path.")
        except ValueError as ve:
            print(f"Error with tasks_db_json_path: {ve}")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")
            return
        self.json_format = {
            "tasks": [],
            "total_no_of_tasks_added": 0,
            "total_no_of_tasks_completed": 0
        }
        try:
            # Ensure the file exists and has the correct format
            if self.json_helper and self.filepath:
                self.json_helper.ensure_json_file(self.filepath, self.json_format)
            else:
                raise FileNotFoundError("Error in creating or finding the task database file.")
        except FileNotFoundError as fnf_error:
            print(f"File error: {fnf_error}")
        except json.JSONDecodeError as json_error:
            print(f"Error decoding JSON file: {json_error}")
        except Exception as e:
            print(f"An unexpected error occurred while ensuring the JSON file: {e}")
        # Read the data from the JSON file during initialization
        try:
            self.data = self.json_helper.read_json(self.filepath)
            if self.data is None:
                # If read_json returns None, fall back to the default json_format
                print("Warning: Read operation returned None, using default format.")
                self.data = self.json_format
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            # Fall back to the default json_format in case of any read error
            self.data = self.json_format
        self.incomplete_tasks = [task for task in self.data["tasks"] if not task.get("status", False)]

    def task_print_format(self, idx, task, status=False, bulletin="-->", date_difference=False):
        x = (
            f"{idx}. {task['description']}\n"
            f"{bulletin}Priority: {task['priority']}\n"
            f"{bulletin}Category: {task['category'] or '>ungrouped<'}\n"
            f"{bulletin}Created: {task['created_date']}\n"
            f"{bulletin}Due: {task['due_date'] or '>no due date<'}\n"
        )
        if status:
            x += f"{bulletin}Status: {'completed' if task['status'] else 'pending'}\n"
        if date_difference:
            y = self.get_date_difference(task)
            if y is not None:
                x += f"{bulletin}Time left: {y}\n"
        print(x)

    def mprint(self, sentence: str, type: Literal[1, 2, 3] = 1) -> str:
        if type not in {1, 2, 3}:
            raise ValueError("Type must be '1', '2', or '3'")
        if type == 1:
            x = str(input(f"{self.input_bulletin}{sentence}"))
            return x
        elif type == 2:
            print(f"{self.response_bulletin}{sentence}")
            return ""
        elif type == 3:
            print(f"{self.error_bulletin}{sentence}")
            return ""
            
    
    def add_task(self):
        """Add Task"""
        #description
        task_description = ""
        while not task_description.strip():  # Loop until non-empty input is provided
            task_description = str(self.mprint("Type task description: "))
        self.mprint(f"Description: {task_description} - set!\n", 2)

        #category
        categories_list = self.view_categories()
        chosen_category = None
        if len(categories_list) > 0:
            print("Choose a category:")
            for idx, category in enumerate(categories_list, 1):
                print(f"{idx} - {category}") 
            # Prompt the user to enter a number
            sent = ("Type a number to choose the category or\n"
                           f"{self.input_bulletin}Type '0' to create a new category or\n"
                           f"{self.input_bulletin}Press Enter to keep task ungrouped: ")
            choice = self.mprint(sent)
            if choice:
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(categories_list):
                        chosen_category = categories_list[choice - 1]
                        self.mprint(f"Category: {chosen_category} - selected!\n", 2)
                        
                    elif choice == 0:
                        chosen_category = ""
                        while not chosen_category.strip():
                            chosen_category = str(self.mprint("Type the name of the category you want to create: ")).lower()
                        if chosen_category in categories_list:
                            self.mprint(f"Category: {chosen_category} - already exists!\n", 2)
                            return
                        self.mprint(f"Category: {chosen_category} - created!\n", 2)
                    elif choice > len(categories_list):
                        self.mprint("Invalid choice! Please try again.", 3)
                        return None
                except ValueError: 
                    self.mprint("Please enter a valid number.", 3)
        else:
            choice = self.mprint("No existing categories. Type '0' to make a new category or press Enter to keep task ungrouped: ")
            if choice:
                try:
                    choice = int(choice)
                    if choice == 0:
                        chosen_category = ""
                        while not chosen_category.strip():
                            chosen_category = str(self.mprint("Type the name of the category you want to create: ")).lower()
                    else:
                        print("Invalid choice! Please try again.")
                        return None
                except ValueError: 
                    print("Please enter a valid number.")
            else:
                chosen_category = None
        self.mprint(f"Category: {chosen_category or ">ungrouped<"} - set\n", 2)

        #priority
        priority_input = self.mprint("Type task priority (1-5) or press Enter for default (1): ")
        priority = 1
        if priority_input:
            try:
                priority_input = int(priority_input)
                if 1 <= priority_input <= 5:
                    priority = priority_input
                else:   
                    print("Invalid priority! Please type a number between 1 and 5.")
                    
            except ValueError:
                print("Invalid input! Using default priority (1).")
        self.mprint(f"Priority: {priority} - set\n", 2)

        #created date
        created_date = datetime.now(pytz.timezone(time_zone)).strftime(time_format)
        created_date_main = datetime.strptime(created_date, time_format)
        
        #due date
        due_date = None
        while due_date is None:
            due_date_input = self.mprint("Type due date (dd/mm/yyyy - hh:mm) or press Enter to skip: ")

            if due_date_input.strip():
                # Extract date and time parts from the input
                date_parts = [int(part) for part in re.split(r"[-/\\' ;]", due_date_input) if part.isdigit()]

                # If only time is provided, assume today's date
                if len(date_parts) == 2:
                    hour, minute = date_parts
                    now = datetime.now(pytz.timezone(time_zone))
                    date_obj = datetime(now.year, now.month, now.day, hour, minute)

                else:
                    # Pad with zeros if date is partially incomplete
                    while len(date_parts) < 5:
                        date_parts.append(0)

                    # Ensure the year has exactly 4 digits
                    year_str = str(date_parts[2])
                    if len(year_str) == 2:
                        date_parts[2] = int("20" + year_str)  # Convert to 20XX format
                    elif len(year_str) == 1:
                        date_parts[2] = int("200" + year_str)  # Convert to 200X format
                    elif len(year_str) == 3:
                        self.mprint("Year format is invalid. Please provide a 4-digit year.")
                        continue

                    # Unpack list into day, month, year, hour, and minute
                    day, month, year, hour, minute = date_parts
                    try:
                        date_obj = datetime(year, month, day, hour, minute)
                    except ValueError:
                        self.mprint("Invalid due date format! Please try again.\n", 3)
                        continue

                # Check if due date is later than the created date
                if date_obj <= created_date_main:
                    self.mprint("Due date must be later than the created date. Please try again.\n", 3)
                else:
                    due_date = date_obj.strftime(time_format)
            else:
                break  # Allow skipping if no input is provided

        # Print the result with the appropriate message
        self.mprint(f"Due date: {due_date or '>no due date<'} - set\n", 2)

        
        if self.data is not None:
            self.data["tasks"].append({
                "description": task_description,
                "status": False,
                "priority": priority,
                "category": chosen_category,
                "created_date": created_date,
                "due_date": due_date
            })
            self.data["total_no_of_tasks_added"] += 1
            self.json_helper.write_json(self.data, self.filepath)
            self.mprint("Task added successfully!\n", 2)
            self.player.gain_xp(self.xp_for_adding_task)
        else:
            print("Error: Unable to add task. Data is unavailable.")   

              
    def view_categories(self):
        if self.data is not None:    
            if len(self.data["tasks"]) > 0:
                categories_list = list({task["category"] for task in self.data["tasks"] if task["category"]})
                # Convert the set to a list (to remove duplicates) and print the result
                #print("Categories:", categories_list)
                return categories_list
            else:
                return []
        else:
            print("error in viewing categories")
            return []
        
 
    def view_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                print("Tasks:")
                for idx, task in enumerate(self.data["tasks"], 1):
                    self.task_print_format(idx, task, status=True, date_difference=True)
            else:
                print("No tasks found.")
        else:
            print("error in viewing tasks")

    def view_all_ungrouped_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                print("All Ungrouped Tasks:")
                # Filter ungrouped tasks and enumerate only those
                ungrouped_tasks = [task for task in self.data["tasks"] if task["category"] is None]
                if ungrouped_tasks:
                    for idx, task in enumerate(ungrouped_tasks, 1):
                        self.task_print_format(idx, task)
                else:
                    print("No ungrouped tasks found.")
            else:
                print("No tasks found.")
        else:
            print("Error in viewing all ungrouped tasks")
            

    def mark_task_as_completed(self):
        if self.data is not None:
            # Use the preloaded self.incomplete_tasks list directly
            if self.incomplete_tasks:
                print("Tasks:")
                # Display only incomplete tasks with updated index
                for idx, task in enumerate(self.incomplete_tasks, 1):
                    self.task_print_format(idx, task)
                # Prompt for task number input
                task_index = self.mprint("Type the number of the task you want to mark as completed: ")
                try:
                    task_index = int(task_index)
                    if 1 <= task_index <= len(self.incomplete_tasks):
                        # Get the task from self.incomplete_tasks
                        task = self.incomplete_tasks[task_index - 1]
                        task["status"] = True
                        self.data["total_no_of_tasks_completed"] += 1
                        # Save updated data to JSON
                        self.json_helper.write_json(self.data, self.filepath)
                        self.mprint(f"Task marked as completed: {task['description']}\n", 2)
                        # Update the self.incomplete_tasks list after marking the task as completed
                        self.player.gain_xp(self.xp_for_completing_task)
                        self.incomplete_tasks = [t for t in self.data["tasks"] if not t.get("status", False)]
                    else:
                        print("Invalid task number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid task number.")
            else:
                print("All tasks are already completed.")

    
    def view_pending_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                if self.incomplete_tasks:
                    for idx, task in enumerate(self.incomplete_tasks, 1):
                        self.task_print_format(idx, task)
                else:
                    print("No pending tasks.")

    def view_tasks_by_category(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                categories_list = self.view_categories()
                if len(categories_list) > 0:
                    print("Tasks by Category:")
                    for idx, category in enumerate(categories_list, 1):
                        print(f"{idx}. {category}")
                    try:
                        selection = int(self.mprint("Enter the number of the category to view tasks: "))
                        if 1 <= selection <= len(categories_list):
                            selected_category = categories_list[selection - 1]
                            
                            tasks_in_category = [task for task in self.incomplete_tasks if task["category"] == selected_category]
                            if tasks_in_category:
                                self.mprint(f"\nTasks in Category: {selected_category} | Total: {len(tasks_in_category)}",2)
                                for idx, task in enumerate(tasks_in_category, 1):
                                    self.task_print_format(idx, task)
                            else:
                                print("  No tasks in this category.")
                        else:
                            print("Invalid selection. Please choose a valid category number.")

                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                else:
                    print("No categories found.")
            else:
                print("No tasks found.")
        else:
            print("Error: Task data not available.")
            

    def view_tasks_by_priority(self):
        if self.data is not None:
            # Filter to include only incomplete tasks
            if self.incomplete_tasks:
                # Sort incomplete tasks by priority
                sorted_tasks = sorted(self.incomplete_tasks, key=lambda x: x["priority"], reverse=True)
                print("Tasks by Priority:")
                for idx, task in enumerate(sorted_tasks, 1):
                    self.task_print_format(idx, task)
            else:
                print("No incomplete tasks found.")

                
    def calculate_and_display_due_difference(self):
        if self.data is not None:
            tasks_with_differences = []
            # Define the format for parsing dates
            # Calculate the time difference for each task
            for task in self.incomplete_tasks:
                created_date = datetime.strptime(task["created_date"], time_format)
                if task["due_date"]:
                    if task.get("status") is True:
                        continue
                    due_date = datetime.strptime(task["due_date"], time_format)
                    difference = due_date - created_date
                    tasks_with_differences.append((task, difference))
            # Sort tasks by time left (difference)
            tasks_with_differences.sort(key=lambda item: item[1])  # Sort by the timedelta (difference)
            # Display tasks in increasing order of time left
            for task, difference in tasks_with_differences:
                days = difference.days
                hours, remainder = divmod(difference.seconds, 3600)
                minutes = remainder // 60
                print(f"Task: {task['description']} - Due in {days} days, {hours} hours, {minutes} minutes")

    def get_date_difference(self, task):
        created_date = datetime.strptime(task["created_date"], time_format)
        if task["due_date"]:
            due_date = datetime.strptime(task["due_date"], time_format)
            difference = due_date - created_date
            days = difference.days
            hours, remainder = divmod(difference.seconds, 3600)
            minutes = remainder // 60
            return f"Due in {days} days, {hours} hours, {minutes} minutes"
        else:
            return None

    def view_tasks_due_today(self):
        # Get the current date in the configured timezone
        now = datetime.now(pytz.timezone(time_zone))
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        tasks_due_today = [
            task for task in self.incomplete_tasks
            if task["due_date"] and today_start <= datetime.strptime(task["due_date"], time_format) < today_end
        ]

        # Display tasks due today, if any
        if tasks_due_today:
            print("\nTasks Due Today:")
            for idx, task in enumerate(tasks_due_today, 1):
                self.task_print_format(idx, task, status=True, date_difference=True)
        else:
            print("\nNo tasks are due today.")

    def check_due_and_overdue_tasks(self):
        now = datetime.now(pytz.timezone(time_zone))
        # Separate lists for tasks due today and overdue tasks
        due_today = []
        overdue_tasks = []
        for task in self.incomplete_tasks:
            if task["due_date"]:
                due_date = datetime.strptime(task["due_date"], time_format).replace(tzinfo=pytz.timezone(time_zone))
                # Check if task is due today
                if now <= due_date <= now + timedelta(days=1):
                    due_today.append(task)
                # Check if task is overdue
                elif due_date < now:
                    overdue_tasks.append(task)
        # Display tasks due today
        if due_today:
            print("\nTasks Due Today:")
            for idx, task in enumerate(due_today, 1):
                self.task_print_format(idx, task, status=True)
        else:
            print("\nNo tasks due today.")
        # Display overdue tasks
        if overdue_tasks:
            print("\nOverdue Tasks:")
            for idx, task in enumerate(overdue_tasks, 1):
                self.task_print_format(idx, task, status=True)
        else:
            print("\nNo overdue tasks.")

    

def main():
    manager = MyTasks()
    manager.check_due_and_overdue_tasks()

    while True:
        print("\nOptions:")
        print("0. Quit")
        print(f"1. {manager.add_task.__doc__}")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. View Pending Tasks")
        print("5. view all ungrouped tasks")
        print("6. view all categories")
        print("7. view tasks by category")
        print("8. view tasks by priority")
        print("9. view tasks by due date")
          
        choice = input("\nChoose an option: ")
        clear_console()
        if choice == '0':
            print("Exiting task manager.")
            break
        elif choice == '1':  
            manager.add_task()
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            manager.mark_task_as_completed()
        elif choice == '4':
            manager.view_pending_tasks()
        elif choice == '5':
            manager.view_all_ungrouped_tasks()
        elif choice == "6":
            if len(manager.view_categories()) > 0:
                print("Categories:")
                for idx, category in enumerate(manager.view_categories(), 1):
                    print(f"{idx}. {category}")
        elif choice == "7":
            manager.view_tasks_by_category()
        elif choice == "8":
            manager.view_tasks_by_priority()
        elif choice == "9":
            manager.calculate_and_display_due_difference()
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()