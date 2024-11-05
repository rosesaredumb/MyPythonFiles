from discord import player
from json_functions import json_funcs
from globals import clear_console, words_db_json_path
import random
from level_system import get_or_create_player
from typing import Literal

class Diet:
    def __init__(self) -> None:
        pass


    def planner(self):
        #age = input("age?: ")
        weight = float(input("weight?: "))
        max_kcals = 2480
        protein_requirement = weight * 0.83


    def cereal_amount(self, cereal_weight: int):
        kcals = 3.5 * cereal_weight
        protein = 0.1 * cereal_weight
        return kcals, protein

    
        