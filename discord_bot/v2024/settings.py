import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from functools import partial
import json
import logging
import os
import re
import subprocess
import time
import timeit
import traceback
from typing import Literal
from PIL import Image, ImageDraw, ImageFont



mindmap_json_path = "./mindmap/data.json"
discord_config_path = './discord_bot/v2024/config.json'
cogs_path = './discord_bot/v2024/cogs'

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def ensure_json_file(file_path):
    """Ensure the JSON file exists or create it."""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({"seed": {}}, f)
            print(f"{file_path} created!")
    else:
        print(f"{file_path} already exists.")

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
            with open(discord_config_path) as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            print("Config file not found. Please ensure 'config.json' exists.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check your config file.")
            return None
        TOKEN = config.get(item)
    return TOKEN


async def send_embed_response(interaction: discord.Interaction, title: str = "", description: str = "", color: discord.Color = discord.Color.blue()):
    """
    Create and send an embed response.

    Args:
        interaction (discord.Interaction): The interaction to respond to.
        title (str): The title of the embed.
        description (str): The description of the embed.
        color (discord.Color): The color of the embed.
    """
    embed = discord.Embed(title=title, description=f"```\n{description}\n```", color=color)
    await interaction.response.send_message(embed=embed)