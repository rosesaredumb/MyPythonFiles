from my_mods import json, os

def find_keys(data, target_key, parent_path="", results=None):
    """
    Recursive function to find all identical keys in the JSON and their paths.
    """
    if results is None:
        results = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{parent_path}.{key}" if parent_path else key

            if key == target_key:
                # Store the current path and value of the matching key
                results.append((current_path, value))

            # Recursively check nested dictionaries
            if isinstance(value, dict):
                find_keys(value, target_key, current_path, results)

    return results


def get_paths(d, path=""):
    paths = []  # List to store all the paths
    for key, value in d.items():
        # Build the new path by appending the current key
        new_path = f"{path}.{key}" if path else key
        if isinstance(value, dict) and value:
            # If the value is a non-empty dictionary, recurse deeper and extend paths
            paths.extend(get_paths(value, new_path))
        else:
            # If it's a final (empty) value, append the path to the list
            paths.append(new_path)
    return paths

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
        if get_yes_no_input("That item already exists. Do you want to replace? (yes/no): "):
            current[keys[-1]][new_value] = {}
            print("Replaced")
        else:
            print("You chose not to continue.")

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


#write_json(file_path, {"seed": {}}) if not os.path.exists(file_path) else print(f"{file_path} already exists.")

def update_item(file_path):
    if not os.path.exists(file_path):
        write_json(file_path, {"seed": {}})
        print(f"{file_path} created!")
    else:
        print(f"{file_path} already exists.")

    # Read the JSON file
    json_data = read_json(file_path)


    target_key, new_value = input("Type the key and the new value in format: key, new value: ").split(", ", 1)


    duplicate_keys = find_keys(json_data, target_key)

    if len(duplicate_keys) > 1:
        print(f"Found {len(duplicate_keys)} occurrences of the key '{target_key}':")
        for i, (path, value) in enumerate(duplicate_keys, start=1):
            print(f"{i}: Path: {path}, Current Value: {value}")
        choice = int(input(f"Which '{target_key}' key would you like to update (1-{len(duplicate_keys)})? ")) - 1
        update_key_value(json_data, duplicate_keys[choice][0], new_value)
    elif len(duplicate_keys) == 1:
        update_key_value(json_data, duplicate_keys[0][0], new_value)
    elif len(duplicate_keys) < 1:
        print("topic doesnt exist")


    write_json(file_path, json_data)
    print(json.dumps(json_data, indent=4))


if __name__ == "__main__":
    file_path = './mindmap/data.json'
    json_data = read_json(file_path)
    print(get_paths(json_data))
