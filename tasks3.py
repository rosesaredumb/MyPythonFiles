from globals import datetime, json, os, pytz
from globals import tasks_db_json_path, time_format, time_zone, clear_console
from json_functions import json_funcs


class MyTasks:
    def __init__(self):
        try:
            self.json_helper = json_funcs()
        except Exception as e:
            print(f"Error initializing json_funcs: {e}")
            return  # You could raise an exception or set it to None, based on your design

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


    
    def add_task(self):

        #description
        task_description = ""
        while not task_description.strip():  # Loop until non-empty input is provided
            task_description = str(input("Enter task description: "))
        print(f"--Description set as: {task_description}\n")

        #category
        categories_list = self.view_categories()
        chosen_category = None
        if len(categories_list) > 0:
            print("Choose a category:")
            for idx, category in enumerate(categories_list, 1):
                print(f"{idx} - {category}")
            
            # Prompt the user to enter a number
            choice = input(">Type a number to choose the category or\n>Type '0' to create a new category or\n>Enter to keep task ungrouped: ")
            if choice:
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(categories_list):
                        chosen_category = categories_list[choice - 1]
                        print(f"--You selected category: {chosen_category}!\n")
                        
                    elif choice == 0:
                        chosen_category = ""
                        while not chosen_category.strip():
                            chosen_category = str(input("Enter name of the category you want to create: ")).lower()
                        if chosen_category in categories_list:
                            print(f"--Category: {chosen_category} already exists!\n")
                            return
                        print(f"--Category: {chosen_category} created!\n")
                    elif choice > len(categories_list):
                        print("Invalid choice! Please try again.")
                        return None
        
                except ValueError: 
                    print("Please enter a valid number.")

        else:
            choice = input(">No existing categories. Type '0' to make a new category or click Enter to keep task ungrouped: ")
            if choice:
                try:
                    choice = int(choice)
                    if choice == 0:
                        chosen_category = ""
                        while not chosen_category.strip():
                            chosen_category = str(input("Enter name of the category you want to create: ")).lower()
                    else:
                        print("Invalid choice! Please try again.")
                        return None
                except ValueError: 
                    print("Please enter a valid number.")
            else:
                chosen_category = None
        print(f"--Category set as: {chosen_category or ">ungrouped<"}\n")

        #priority
        priority_input = input(">Enter task priority (1-5) or press Enter for default (1): ")
        priority = 1
        if priority_input:
            try:
                priority_input = int(priority_input)
                if 1 <= priority_input <= 5:
                    priority = priority_input
                else:   
                    print("Invalid priority! Please enter a number between 1 and 5.")
                    
            except ValueError:
                print("Invalid input! Using default priority (1).")
        print(f"--Priority set as: {priority}\n")

        #created date
        created_date = datetime.now(pytz.timezone(time_zone)).strftime(time_format)


        #due date
        due_date_input = input(">Type due date (dd/mm/yyyy - hh:mm) or press Enter to skip: ")
        due_date = None
        if due_date_input.strip() == "":
            due_date = None
        else:
            try:
                if " - " in due_date_input:
                    due_date = datetime.strptime(due_date_input, "%d/%m/%Y - %H:%M")
                else:
                    due_date = datetime.strptime(due_date_input, "%d/%m/%Y")  # Default time to 00:00
                    due_date = due_date.replace(hour=0, minute=0)
                due_date = due_date.strftime("%d/%m/%Y - %H:%M")
            except ValueError:
                print("Invalid due date format! Skipping due date.\n")
        print(f"--Due date set as: {due_date or ">no due date<"}\n")

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
            print("Task added successfully!\n")
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
        


    def task_print_format(self, idx, task, status=False, bulletin="--"):
        x = (
            f"{idx}. {task["description"]}\n"
            f"{bulletin}Priority: {task["priority"]}\n"
            f"{bulletin}Category: {task["category"] or ">ungrouped<"}\n"
            f"{bulletin}Created: {task["created_date"]}\n"
            f"{bulletin}Due: {task["due_date"] or '>no due date<'}\n"
        )
        if status is True:
            x += f"{bulletin}Status: {"completed" if task["status"] else "pending"}\n"
        
        print(x)
    
    def view_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                print("Tasks:")
                for idx, task in enumerate(self.data["tasks"], 1):
                    self.task_print_format(idx, task, status=True)
            else:
                print("No tasks found.")
        else:
            print("error in viewing tasks")

    def view_all_ungrouped_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                print("All Ungrouped Tasks:")
                for idx, task in enumerate(self.data["tasks"], 1):
                    if task["category"] is None:
                        self.task_print_format(idx, task, status=True)
            else:
                print("No ungrouped tasks found.")
        else:
            print("error in viewing all ungrouped tasks")
            

    def mark_task_as_completed(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                print("Tasks:")
                for idx, task in enumerate([t for t in self.data["tasks"] if not t["status"]], 1):
                    self.task_print_format(idx, task)
                task_index = input(">Enter the number of the task you want to mark as completed: ")
                try:
                    task_index = int(task_index)
                    if 1 <= task_index <= len(self.data["tasks"]):
                        task = self.data["tasks"][task_index - 1]
                        task["status"] = True
                        self.data["total_no_of_tasks_completed"] += 1
                        self.json_helper.write_json(self.data, self.filepath)
                        print(f"Task marked as completed: {task['description']}\n")
                    else:
                        print("Invalid task number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid task number.")
                    
    def view_pending_tasks(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                pending_tasks = [t for t in self.data["tasks"] if not t["status"]]
                if pending_tasks:
                    for idx, task in enumerate(pending_tasks, 1):
                        self.task_print_format(idx, task)
                else:
                    print("No pending tasks.")

    def view_tasks_by_category(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                categories_list = self.view_categories()
                if len(categories_list) > 0:
                    print("Tasks by Category:")
                    for category in categories_list:
                        print(f"Category: {category}")
                        for idx, task in enumerate(self.data["tasks"], 1):
                            if task["category"] == category:
                                self.task_print_format(idx, task)
                else:
                    print("No categories found.")
            else:
                print("No tasks found.")

    def view_tasks_by_priority(self):
        if self.data is not None:
            if len(self.data["tasks"]) > 0:
                sorted_tasks = sorted(self.data["tasks"], key=lambda x: x["priority"], reverse=True)
                print("Tasks by Priority:")
                for idx, task in enumerate(sorted_tasks, 1):
                    self.task_print_format(idx, task)
            else:
                print("No tasks found.")
    
    

def main():
    manager = MyTasks()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. View Pending Tasks")
        print("5. view all ungrouped tasks")
        print("6. view all categories")
        print("7. view tasks by category")
        print("8. view tasks by priority")
        print("9. Quit\n")
        

        choice = input("Choose an option: ")
        clear_console()
        
        if choice == '1':  
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
        elif choice == '9':
            print("Exiting task manager.")
            break
        
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()