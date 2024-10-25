import json
import os


class json_funcs:
    def __init__(self):
        pass

    def read_json(self, file_path):
        """Reads and returns JSON data from a file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON data from '{file_path}'. The file may be corrupted or not in JSON format.")
        except PermissionError:
            print(f"Error: Permission denied when trying to read '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
        return None

    def write_json(self, data, file_path):
        """Writes data to a JSON file."""
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                #print(f"Data successfully written to '{file_path}'.")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except TypeError as e:
            print(f"Error: Failed to serialize data to JSON. Data might not be serializable. Details: {e}")
        except PermissionError:
            print(f"Error: Permission denied when trying to write to '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred while writing to the file: {e}")

    def ensure_json_file(self, file_path, dict_format):
        """Ensures the JSON file exists, or creates it with a specified format."""
        try:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(dict_format, f)
                    print(f"{file_path} created with the provided format.")
            else:
                print(f"{file_path} already exists.")
        except TypeError as e:
            print(f"Error: Failed to serialize initial dictionary to JSON. Data might not be serializable. Details: {e}")
        except PermissionError:
            print(f"Error: Permission denied when trying to create '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred while creating the file: {e}")


    def get_current_path(self, data, target_key, parent_path=""):
        """
        Retrieves path of the specified key.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                # Create the full path by appending the current key to the parent path
                current_path = f"{parent_path}.{key}" if parent_path else key
    
                if key == target_key:
                    # Return the parent path (not including the target key itself)
                    return current_path
    
                # Recursively check nested dictionaries
                if isinstance(value, dict):
                    result = self.get_current_path(value, target_key, current_path)
                    if result:
                        return result
    
        return None  # Return None if the key is not found
    
    
    def get_all_parent_paths(self, data, target_key, parent_path="", paths=None):
        """
        Retrieves paths of identicals keys in list form.
        """
        if paths is None:
            paths = []
            
        if isinstance(data, dict):
            for key, value in data.items():
                # Create the full path by appending the current key to the parent path
                current_path = f"{parent_path}.{key}" if parent_path else key
    
                if key == target_key:
                    # If the key matches the target key, append the parent path to the list
                    paths.append(parent_path)
    
                # Recursively check nested dictionaries
                if isinstance(value, dict):
                    self.get_all_parent_paths(value, target_key, current_path, paths)

        return paths
