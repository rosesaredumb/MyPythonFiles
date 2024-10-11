import os
import json
import discord
from discord.ext import commands
import asyncio


def retrieve_keys(item):
    """
    Retrieve the specified key from environment variables or a config file.
    
    Parameters:
        item (str): The name of the key to retrieve.
    
    Returns:
        str: The value of the key, or None if not found.
    """
    try:
        with open('./discord_bot/2024/config.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("Config file not found. Please ensure 'config.json' exists.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check your config file.")
        return None

    if "REPLIT_DB_URL" in os.environ:
        print("This script is running in Replit!")
        TOKEN = os.getenv(item)
    else:
        print("This script is NOT running in Replit.")
        TOKEN = config.get(item)
    if TOKEN is None:
        print(f"Warning: '{item}' not found in environment variables or config file.")
    
    return TOKEN
