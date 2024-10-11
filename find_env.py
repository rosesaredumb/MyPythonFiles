import os

def is_running_in_replit():
    return "REPLIT_DB_URL" in os.environ

if is_running_in_replit():
    print("This script is running in Replit!")
else:
    print("This script is NOT running in Replit.")

