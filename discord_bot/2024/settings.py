import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import json
import os



def retrieve_keys(item):
    """
    Retrieve the specified key from environment variables or a config file.
    
    Parameters:
        item (str): The name of the key to retrieve.
    
    Returns:
        str: The value of the key, or None if not found.
    """   

    if "REPLIT_DB_URL" in os.environ:
        print("This script is running in Replit!")
        TOKEN = os.getenv(item)
    else:
        print("This script is NOT running in Replit.")
        try:
            with open('./discord_bot/2024/config.json') as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            print("Config file not found. Please ensure 'config.json' exists.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check your config file.")
            return None
        TOKEN = config.get(item)
    return TOKEN