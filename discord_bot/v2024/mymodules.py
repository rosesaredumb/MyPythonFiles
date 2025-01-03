import ast
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from functools import partial
import json
import logging
import os
import re
import requests
import subprocess
import time
import timeit
import traceback
from typing import Literal
from PIL import Image, ImageDraw, ImageFont
import inspect



mindmap_json_path = "./discord_bot/v2024/cogs/data.json"
discord_config_path = './discord_bot/v2024/config.json'
cogs_path = './discord_bot/v2024/cogs'

def retrieve_keys(item):
    """
    Retrieve the specified key from environment variables or a config file.

    Parameters:
        item (str): The name of the key to retrieve.

    Returns:
        str: The value of the key, or None if not found.
    """   
    args = item.split()
    if "REPLIT_DB_URL" in os.environ:
        x = "_".join(args)
        print("This script is running in Replit!")
        TOKEN = os.environ[x]
    else:
        
        try:
            with open(discord_config_path) as config_file:
                config = json.load(config_file)
            print("This script is NOT running in Replit.")
        except FileNotFoundError:
            print("Config file not found. Please ensure 'config.json' exists.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check your config file.")
            return None

        value = config

        try:
            for arg in args:
                value = value[arg]  # Access the next level using the current key
            TOKEN = value
        except KeyError:
            print(f"Key {' -> '.join(args)} not found in the config.")
            return None
        except TypeError:
            print("Invalid path provided. Check the keys and their hierarchy.")
            return None
    return str(TOKEN)


async def send_embed_response(interaction: discord.Interaction, 
                              title: str = "", 
                              description: str = "", 
                              color: discord.Color = discord.Color.blue(), 
                              type = "message", 
                              ephemeral: bool = False):
    """
    Create and send an embed response.

    Args:
        interaction (discord.Interaction): The interaction to respond to.
        title (str): The title of the embed.
        description (str): The description of the embed.
        color (discord.Color): The color of the embed.
        type (str): The type of response ('message' or 'followup').
        ephemeral (bool): Whether the message should be ephemeral (default is True).
    """
    embed = discord.Embed(title=title, description=f"```\n{description}\n```", color=color)
    if type == "message":
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
    elif type == "followup":
        await interaction.followup.send(embed=embed, ephemeral=ephemeral)

