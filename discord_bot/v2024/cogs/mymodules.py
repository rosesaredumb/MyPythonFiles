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

main_ID = "ZXvh34o"
class imgur_functions:
    def __init__(self):
        pass

    def get_imgur_album_images(self, album_id: str):
        # Imgur API endpoint to get album images
        url = f"https://api.imgur.com/3/album/{album_id}/images"
        
        # Imgur requires the client ID to be sent as a header
        headers = {
            "Authorization": f"Client-ID {str(retrieve_keys("imgur client_ID"))}"
        }

        # Make the request to Imgur API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            images = data["data"]

            # Extract the links to each image
            image_links = [image["link"] for image in images]
            return image_links
        else:
            print(f"Failed to fetch album. Status code: {response.status_code}")
            return []


    def get_imgur_album_name(self, album_id: str):
        url = f"https://api.imgur.com/3/album/{album_id}"
        headers = {"Authorization": f"Client-ID {str(retrieve_keys("imgur client_ID"))}"}

        # Make the request to Imgur API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            album_title = data['data']['title']
            return album_title
        else:
            return f"Error: Unable to retrieve album info (Status code: {response.status_code})"

    def get_imgur_album_images_with_descriptions(self):
        # Imgur API endpoint to get album images
        url = f"https://api.imgur.com/3/album/{main_ID}/images"
        id = '2ea349879154d4a'
        # Imgur requires the client ID to be sent as a header
        headers = {
            "Authorization": f"Client-ID {str(retrieve_keys('imgur client_ID'))}"
        }

        # Make the request to Imgur API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            images = data["data"]

            # Extract the links and descriptions of each image
            image_data = {}
            for image in images:
                if image["description"]:
                    if image["description"] not in image_data:
                        image_data[image["description"]] = [image["link"]]

                    elif image["description"] in image_data:
                        image_data[image["description"]].append(image["link"])

                else:
                    if "None" not in image_data:
                        image_data["None"] = [image["link"]]

                    elif "None" in image_data:
                        image_data["None"].append(image["link"])
            
            titles = list(image_data.keys())

            return image_data, titles
        else:
            print(f"Failed to fetch album. Status code: {response.status_code}")
            return []

class json_funcs:
    def __init__(self):
        pass

    def read_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def write_json(self, data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def ensure_json_file(self, file_path):
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
    args = item.split()
    if "REPLIT_DB_URL" in os.environ:
        x = "_".join(args)
        TOKEN = os.environ[x]
    else:
        
        try:
            with open(discord_config_path) as config_file:
                config = json.load(config_file)
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