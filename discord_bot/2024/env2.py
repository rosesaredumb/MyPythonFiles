import os
import json

def retrieve_keys(item):
    """
    Retrieve the specified key from environment variables or a config file.
    
    Parameters:
        item (str): The name of the key to retrieve.
    
    Returns:
        str: The value of the key, or None if not found.
    """
    # Try to load the config file
    try:
        with open('config.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Config file not found. Please ensure 'config.json' exists.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check your config file.")
        return None

    if "REPLIT_DB_URL" in os.environ:
        print("This script is running in Replit!")
        token = os.getenv(item)
    else:
        print("This script is NOT running in Replit.")
        token = config.get(item)

    if token is None:
        print(f"Warning: '{item}' not found in environment variables or config file.")
    
    return token

# Example usage
print(retrieve_keys("DISCORD_TOKEN"))