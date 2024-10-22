from globals import json, os
from globals import mindmap_db_json_path

class JsonEditor:
    def __init__(self, file_path=None):
        # Set default file path if none is provided
        self.file_path = file_path if file_path else mindmap_db_json_path

        # Check and ensure the file exists
        self.ensure_file_exists()

        # Load the JSON data from the file
        self.data = self.read_json()

    def ensure_file_exists(self):
        """Ensure that the file exists. If not, create it with an initial structure."""
        if not os.path.exists(self.file_path):
            # Create the file with a default seed structure if it doesn't exist
            self.write_json({"seed": {}})
            print(f"{self.file_path} created with initial structure!")
        else:
            print(f"{self.file_path} already exists.")

    def read_json(self):
        """Read JSON from the file."""
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def write_json(self, data):
        """Write JSON data back to the file."""
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def find_keys(self, target_key, parent_path="", results=None):
        """
        Recursive function to find all identical keys in the JSON and their paths.
        """
        if results is None:
            results = []
        
        data = self.data
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{parent_path}.{key}" if parent_path else key

                if key == target_key:
                    results.append((current_path, value))

                if isinstance(value, dict):
                    self.find_keys(target_key, current_path, results)

        return results

    def get_paths(self, d=None, path=""):
        """Get all the paths of keys in the JSON data."""
        if d is None:
            d = self.data

        paths = []
        for key, value in d.items():
            new_path = f"{path}.{key}" if path else key
            if isinstance(value, dict) and value:
                paths.extend(self.get_paths(value, new_path))
            else:
                paths.append(new_path)
        return paths

    def update_key_value(self, path_to_update, new_value):
        """Update a specific key with a new value."""
        current = self.data
        keys = path_to_update.split('.')
        for key in keys[:-1]:
            current = current[key]

        x = list(current[keys[-1]].keys())
        print(x)

        if new_value not in x:
            current[keys[-1]][new_value] = {}
        else:
            if self.get_yes_no_input("That item already exists. Do you want to replace? (yes/no): "):
                current[keys[-1]][new_value] = {}
                print("Replaced")
            else:
                print("You chose not to continue.")

    def get_yes_no_input(self, prompt):
        """Helper function to get 'yes' or 'no' input from the user."""
        while True:
            response = input(prompt).strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please answer 'yes' or 'no'.")

    def update_item(self):
        """Update an item in the JSON data."""
        target_key, new_value = input("Type the key and the new value in format: key, new value: ").split(", ", 1)
        duplicate_keys = self.find_keys(target_key)

        if len(duplicate_keys) > 1:
            print(f"Found {len(duplicate_keys)} occurrences of the key '{target_key}':")
            for i, (path, value) in enumerate(duplicate_keys, start=1):
                print(f"{i}: Path: {path}, Current Value: {value}")
            choice = int(input(f"Which '{target_key}' key would you like to update (1-{len(duplicate_keys)})? ")) - 1
            self.update_key_value(duplicate_keys[choice][0], new_value)
        elif len(duplicate_keys) == 1:
            self.update_key_value(duplicate_keys[0][0], new_value)
        else:
            print("Topic doesn't exist.")

        self.write_json(self.data)
        print(json.dumps(self.data, indent=4))


if __name__ == "__main__":
    editor = JsonEditor()
    print(editor.get_paths())
    editor.update_item()
