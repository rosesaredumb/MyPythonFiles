import json

def get_current_path(data, target_key, parent_path=""):
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
                result = get_current_path(value, target_key, current_path)
                if result:
                    return result

    return None  # Return None if the key is not found


def get_all_parent_paths(data, target_key, parent_path="", paths=None):
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
                get_all_parent_paths(value, target_key, current_path, paths)

    return paths