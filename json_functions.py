import json
import os
from typing import Any


class JSONReadError(Exception):
    pass


class JSONWriteError(Exception):
    pass


class JSONEnsureError(Exception):
    pass


class json_funcs:

    def read_json(self, file_path: str) -> Any:
        """
        Reads and returns JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            Any: The data read from the JSON file.

        Raises:
            JSONReadError: If the file cannot be read or the JSON is invalid.
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise JSONReadError(f"File '{file_path}' not found.")
        except json.JSONDecodeError:
            raise JSONReadError(
                f"Failed to decode JSON from '{file_path}'. Corrupted or invalid format."
            )
        except PermissionError:
            raise JSONReadError(f"Permission denied reading '{file_path}'.")
        except Exception as e:  # Keep a general exception for truly unexpected errors
            raise JSONReadError(f"An unexpected error occurred: {e}")

    def write_json(self, data: Any, file_path: str) -> None:
        """
        Writes data to a JSON file.

        Args:
            data (Any): The data to write.
            file_path (str): The path to the JSON file.

        Raises:
            JSONWriteError: If the file cannot be written to.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except TypeError as e:
            raise JSONWriteError(f"Failed to serialize data: {e}")
        except FileNotFoundError:
            raise JSONWriteError(f"File '{file_path}' not found.")
        except PermissionError:
            raise JSONWriteError(
                f"Permission denied writing to '{file_path}'.")
        except Exception as e:
            raise JSONWriteError(f"An unexpected error occurred: {e}")

    def ensure_json_file(self, file_path: str, default_data: Any) -> None:
        """
        Ensures the JSON file exists, creating it with default data if not.

        Args:
            file_path (str): The path to the JSON file.
            default_data (Any): The default data to write if the file doesn't exist.

        Raises:
            JSONEnsureError: If the file cannot be created.
        """
        try:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump(default_data, f, indent=4)
                    print(f"{file_path} created.")
            else:
                print(f"{file_path} already exists.")
        except TypeError as e:
            raise JSONEnsureError(
                f"Failed to serialize initial dictionary: {e}")
        except PermissionError:
            raise JSONEnsureError(f"Permission denied creating '{file_path}'.")
        except Exception as e:
            raise JSONEnsureError(f"An unexpected error occurred: {e}")

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
                    result = self.get_current_path(value, target_key,
                                                   current_path)
                    if result:
                        return result

        return None  # Return None if the key is not found

    def get_all_parent_paths(self,
                             data,
                             target_key,
                             parent_path="",
                             paths=None):
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
                    self.get_all_parent_paths(value, target_key, current_path,
                                              paths)

        return paths
