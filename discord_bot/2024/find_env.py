import os
import json

def retrieve_keys(item):
    with open('config.json') as config_file:
        config = json.load(config_file)

    if "REPLIT_DB_URL" in os.environ:
        print("This script is running in Replit!")
        TOKEN = os.getenv(f'{item}')
    else:
        print("This script is NOT running in Replit.")
        TOKEN = config.get(f'{item}')
    
    return TOKEN

print(retrieve_keys("DISCORD_TOKEN"))


