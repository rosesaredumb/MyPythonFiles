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