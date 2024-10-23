from globals import datetime, json, os, pytz
from globals import tasks_db_json_path, time_format, time_zone, json_funcs


class MyTasks:
    def __init__(self):
        self.json_helper = json_funcs()
        self.filepath = tasks_db_json_path
        self.json_format = {
                            "tasks":[],
                            "total_no_of_tasks_added": 0,
                            "total_no_of_tasks_completed": 0
                           }
        self.json_helper.ensure_json_file(self.filepath, self.json_format)

    
    def add_task(self):
        data = self.json_helper.read_json(self.filepath)

        #description
        task_description = ""
        while not task_description.strip():  # Loop until non-empty input is provided
            task_description = str(input("Enter task description: "))
        print(f"--Description set as: {task_description}")

        #category
        categories_list = self.view_categories()
        chosen_category = None
        if len(categories_list) > 0:
            print("Choose a category:")
            for idx, category in enumerate(categories_list, 1):
                print(f"{idx} - {category}")
            
            # Prompt the user to enter a number
            choice = input("Type a number to choose the category or\nType '0' to create a new category or\nEnter to keep task ungrouped: ")
            if choice:
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(categories_list):
                        chosen_category = categories_list[choice - 1]
                        print(f"You selected: {chosen_category}")
                        return chosen_category
                    elif choice == 0:
                        chosen_category = ""
                        while not chosen_category.strip():
                            chosen_category = str(input("Enter name of the category you want to create: ")).lower()
                        if chosen_category not in categories_list:
                            print(f"Category: {chosen_category} created!")
                            return chosen_category
                        else:
                            print(f"Category: {chosen_category} already exists!")
                            return chosen_category
                    elif choice > len(categories_list):
                        print("Invalid choice! Please try again.")
                        return None
        
                except ValueError: 
                    print("Please enter a valid number.")

        else:
            choice = input("No existing categories. Type '0' to make a new category or click Enter to keep task ungrouped: ")
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
        print(f"--Category set as: {chosen_category}")

        #priority
        priority_input = input("Enter task priority (1-5) or press Enter for default (1): ")
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
        print(f"--Priority set as: {priority}")

        #created date
        created_date = datetime.now(pytz.timezone(time_zone)).strftime(time_format)


        #due date
        due_date_input = input("Enter due date (dd/mm/yyyy - hh:mm) or press Enter to skip: ")
        due_date = None
        if due_date_input.strip() == "":
            due_date = None
        try:
            if " - " in due_date_input:
                due_date = datetime.strptime(due_date_input, "%d/%m/%Y - %H:%M")
            else:
                due_date = datetime.strptime(due_date_input, "%d/%m/%Y")  # Default time to 00:00
                due_date = due_date.replace(hour=0, minute=0)
            due_date = due_date.strftime("%d/%m/%Y - %H:%M")
        except ValueError:
            print("Invalid due date format! Skipping due date.")
        print(f"--Due date set as: {due_date}")

        
        data["tasks"].append({
            "description": task_description, 
            "status": False,
            "priority": priority,
            "category": chosen_category,
            "created_date": created_date,
            "due_date": due_date
        })
        self.json_helper.write_json(data, self.filepath)
        print(data["tasks"])
            
    
        


    def view_categories(self):
        data = self.json_helper.read_json(self.filepath)
        
        if len(data["tasks"]) > 0:
            categories_list = list({task["category"] for task in data["tasks"] if task["category"]})
            # Convert the set to a list (to remove duplicates) and print the result
            print("Categories:", categories_list)
            return categories_list
        else:
            return []
        
        

x = MyTasks()
x.add_task()