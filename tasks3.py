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
            task_description = str(input("Enter task description: ")).lower()
        data = self.json_helper.read_json(self.filepath)

        if len(data["tasks"]) > 0:
            categories_list = self.view_categories()
            if len(categories_list) > 0:
                print("Choose a category:")
                for idx, category in enumerate(categories_list, 1):
                    print(f"{idx} - {category}")

                # Prompt the user to enter a number
                choice = int(input("Enter a number to choose the category: "))

                # Ensure the input is valid
                if 1 <= choice <= len(categories_list):
                    chosen_category = categories_list[choice - 1]
                    print(f"You selected: {chosen_category}")
                else:
                    print("Invalid choice")
        data["tasks"].append({
            "description": task_description, 
            "status": False
        })


    def view_categories(self):
        try:
            data = self.json_helper.read_json(self.filepath)
            #if len(data["tasks"]) > 0:
            categories_list = list({task["category"] for task in data["tasks"] if task["category"]})
            # Convert the set to a list (to remove duplicates) and print the result
            print("Categories:", categories_list)
            return categories_list
        
        

x = MyTasks()
x.add_task()