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
        task_description = ""
        while not task_description.strip():  # Loop until non-empty input is provided
            task_description = str(input("Enter task description: "))
        data = self.json_helper.read_json(self.filepath)

        
        categories_list = self.view_categories()
        chosen_category = None
        if len(categories_list) > 0:
            print("Choose a category:")
            for idx, category in enumerate(categories_list, 1):
                print(f"{idx} - {category}")
            
            # Prompt the user to enter a number
            choice = input("Enter a number to choose the category: ")
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
                            print("Category already exists!")
                            return chosen_category
                    elif choice > len(categories_list):
                        print("Invalid choice! Please try again.")
                        return None
        
                except ValueError: 
                    print("Please enter a valid number.")

        else:
            choice = input("no existing categories. Enter a 0 to make the category or click enter: ")
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
            
        data["tasks"].append({
            "description": task_description, 
            "status": False,
            "category": chosen_category
        })
        self.json_helper.write_json(data, self.filepath)
        print("done")
            
    
        


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