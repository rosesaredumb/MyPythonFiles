import json

user_input = str(input("type the key and the new value to be added in the format: key, new value"))

def find_duplicate_keys(data, target_key, parent_path="", results=None):
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
                find_duplicate_keys(value, target_key, current_path, results)

    return results


def update_key_value(data, path_to_update, new_value):
    """
    Function to update the value of the selected duplicate key.
    """
    keys = path_to_update.split('.')
    current = data

    # Traverse the path except for the last key
    for key in keys[:-1]:
        current = current[key]
    
    # Update the value of the last key in the path
    current[keys[-1]][new_value] = {}


def read_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Write updated JSON data back to the file
def write_json_to_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


file_path = 'data.json'

# Read the JSON data from the file
json_data = read_json_from_file(file_path)


target_key = "cv"

# Find all occurrences of the key
duplicate_keys = find_duplicate_keys(json_data, target_key)

# If duplicates are found, prompt the user for which one to update
if len(duplicate_keys) > 1:
    print(f"Found {len(duplicate_keys)} occurrences of the key '{target_key}':")
    for i, (path, value) in enumerate(duplicate_keys, start=1):
        print(f"{i}: Path: {path}, Current Value: {value}")
    
    # Ask the user to select which key to update
    choice = int(input(f"Which '{target_key}' key would you like to update (1-{len(duplicate_keys)})? ")) - 1

    # Ask the user for the new value
    new_value = input(f"Enter the new value for '{target_key}' at path {duplicate_keys[choice][0]}: ")

    #new_value = {new_value: {}}
    # Update the selected key with the new value
    update_key_value(json_data, duplicate_keys[choice][0], new_value)

    # Print the updated JSON structure
    write_json_to_file(file_path, json_data)
    print(json.dumps(json_data, indent=4))

else:
    new_value = input(f"Enter the new value for '{target_key}' at path {duplicate_keys[0][0]}: ")

    #new_value = {new_value: {}}
    # Update the selected key with the new value
    update_key_value(json_data, duplicate_keys[0][0], new_value)

    # Print the updated JSON structure
    write_json_to_file(file_path, json_data)
    print(json.dumps(json_data, indent=4))
