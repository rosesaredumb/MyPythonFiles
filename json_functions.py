import json

def get_current_path(data, target_key, parent_path=""):
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