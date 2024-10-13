from settings import json, os

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

file_path = './mindmap/data2.json'

#write_json(file_path, {"seed": {}}) if not os.path.exists(file_path) else print(f"{file_path} already exists.")

if not os.path.exists(file_path):
    write_json(file_path, {})
    print(f"{file_path} created!")
else:
    print(f"{file_path} already exists.")

# Read the JSON file
json_data = read_json(file_path)
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

# Call the function on the dictionary
print(get_paths(json_data))