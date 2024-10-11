import json
import os

def get_yes_no_input(prompt):
    while True:
        response = input(prompt).strip().lower()  # Get user input
        if response in ['yes', 'y']:
            return True  # Return True for 'yes'
        elif response in ['no', 'n']:
            return False  # Return False for 'no'
        else:
            print("Please answer 'yes' or 'no'.") 

def update_key_value(data, path_to_update, new_value):
    current = data
    keys = path_to_update.split('.')
    for key in keys[:-1]:
        current = current[key]
    x = list(current[keys[-1]].keys())
    print(x)
    if new_value not in x:
        current[keys[-1]][new_value] = {}
    else:
        if get_yes_no_input("already there. Do you want to replace? (yes/no): "):
            print("You chose to continue.")
            current[keys[-1]][new_value] = {}
        else:
            print("You chose not to continue.")



def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

file_path = 'data.json'

#write_json(file_path, {"seed": {}}) if not os.path.exists(file_path) else print(f"{file_path} already exists.")

if not os.path.exists(file_path):
    write_json(file_path, {"seed": {}})
    print(f"{file_path} created!")
else:
    print(f"{file_path} already exists.")

# Read the JSON file
json_data = read_json(file_path)


update_key_value(json_data, "seed.gynccc.lol", "s")
write_json('data.json', json_data)
print(json.dumps(json_data, indent=4))
