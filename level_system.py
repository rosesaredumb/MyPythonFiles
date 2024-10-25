from globals import json, player_progress_db_json_path, os
from json_functions import json_funcs

class Player:
    def __init__(self, name):
        self.json_helper = json_funcs()
        self.filepath = player_progress_db_json_path
        self.data = self.json_helper.read_json(self.filepath)
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 50  # Lower starting XP
        self.base_multiplier = 1.2  # Lower base multiplier

    def gain_xp(self, amount):
        #print(f"{self.name} gains {amount} XP!")
        self.xp += amount
        self.check_level_up()
        self.save_to_file()  # Save progress after gaining XP

    def check_level_up(self):
        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.xp -= self.xp_to_next_level
        self.level += 1
        # Smaller increment in multiplier per level
        self.xp_to_next_level = int(self.xp_to_next_level * (self.base_multiplier + (self.level * 0.05)))
        if self.level % 10 == 0:
            print(f"{self.name} leveled up to level {self.level}!")
            print(f"XP needed for next level: {self.xp_to_next_level}")

    def xp_needed_for_next_level(self):
        # Calculate how much more XP is required to reach the next level
        xp_needed = self.xp_to_next_level - self.xp
        print(f"{self.name} needs {xp_needed} more XP to reach the next level.")
        return xp_needed

    def save_to_file(self):
        data = {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level
        }
        self.json_helper.write_json(data, self.filepath)
        #print(f"{self.name}'s progress saved to {self.filepath}.")

def load_from_file(filename=player_progress_db_json_path):
    # Check if the file exists; if not, create it with an empty dictionary
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({}, f)  # Create an empty JSON file
        print(f"{filename} created.")

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            # Since this is for a single player, check for player data directly
            if 'name' in data:
                player = Player(data['name'])
                player.level = data['level']
                player.xp = data['xp']
                player.xp_to_next_level = data['xp_to_next_level']
                #print(f"{data['name']}'s progress loaded from {filename}.")
                return player
            else:
                print("No player data found in the file.")
                return None
    except FileNotFoundError:
        print("Save file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding the save file.")
        return None