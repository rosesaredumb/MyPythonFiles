import asyncio
from datetime import datetime
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
import pytz


tasks_db_json_path = "./database/tasks_db.json"
mindmap_db_json_path = "./database/mindmap_db.json"
config_json_path = './config.json'
time_format = "%d/%m/%Y - %H:%M"
time_zone = 'Asia/Calcutta'


def retrieve_key(item: str) -> str:
    """  
    Retrieve the specified key from environment variables or a config file.  

    Parameters:  
        item (str): The name of the key to retrieve.  

    Returns:  
        str: The value of the key.  

    Raises:  
        KeyError: If the key is not found in environment variables or the config file.  
        FileNotFoundError: If the config file does not exist.  
        json.JSONDecodeError: If the config file is not valid JSON.  
    """  
    formatted_key = "_".join(item.split())  

    if "REPLIT_DB_URL" in os.environ:  
        print("This script is running in Replit!")  
        token = os.environ.get(formatted_key)  
        if token is None:  
            raise KeyError(f"Key '{formatted_key}' not found in environment variables.")  
        return token  
    else:  
        print("This script is NOT running in Replit.")  
        try:  
            with open(config_json_path) as config_file:  
                config = json.load(config_file)  
        except FileNotFoundError:  
            raise FileNotFoundError("Config file not found. Please ensure 'config.json' exists.")  
        except json.JSONDecodeError as e:  
            raise json.JSONDecodeError("Error decoding JSON. Please check your config file.", e.doc, e.pos)  

        token = config.get(formatted_key)  
        if token is None:  
            raise KeyError(f"Key '{formatted_key}' not found in config.")  
        return token

#print(type(retrieve_key("discord rosesaredumb token")))
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
                json.dump({"tasks":[],
                          "tasks_completed": 0,
                          }, f)
                print(f"{file_path} created!")
        else:
            print(f"{file_path} already exists.")