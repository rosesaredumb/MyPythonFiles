from globals import json, player_progress_db_json_path, os
from json_functions import json_funcs
import matplotlib.pyplot as plt

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

    def gain_xp(self, amount, show_lvl_up=False):
        #print(f"{self.name} gains {amount} XP!")
        self.xp += amount
        self.check_level_up(show_lvl_up)
        self.save_to_file()  # Save progress after gaining XP

    def check_level_up(self, show_lvl_up=False):
        while self.xp >= self.xp_to_next_level:
            self.level_up(show_lvl_up)

    def level_up(self, show_lvl_up = False):
        self.xp -= self.xp_to_next_level
        self.level += 1
        # Smaller increment in multiplier per level
        self.xp_to_next_level = int(self.xp_to_next_level * (self.base_multiplier + (self.level * 0.05)))
        if show_lvl_up is True:
            print(f"{self.name} leveled up to lvl {self.level}")
            print(f"XP needed for next lvl: {self.xp_to_next_level}")
        elif show_lvl_up is False:
            if self.level % 10 == 0:
                print(f"{self.name} leveled up to lvl {self.level}")
                print(f"XP needed for next lvl: {self.xp_to_next_level}")

    def xp_needed_for_next_level(self):
        # Calculate how much more XP is required to reach the next level
        xp_needed = self.xp_to_next_level - self.xp
        print(f"{self.name} needs {xp_needed} more XP to reach the next level | Current level: {self.level}")
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


def get_or_create_player():
    player = load_from_file()
    if player is None:
        player = Player("Steeve")
        print("New player -Steeve- created!")  # Create a new player if loading fails
    return player

def calculate_and_print_xp_for_levels(max_level):
    base_xp = 50
    base_multiplier = 1.2
    xp_needed = []

    current_xp = base_xp
    for level in range(1, max_level + 1):
        xp_needed.append(current_xp)
        current_xp = int(current_xp * (base_multiplier + (level * 0.05)))

    # Print results for every 10 levels
    for level in range(1, max_level + 1):
        if level % 5 == 0:  # Check if the level is a multiple of 10
            print(f"Level {level}: {xp_needed[level - 1]} XP")

# Example usage
#calculate_and_print_xp_for_levels(50)

def calculate_and_plot_xp_graph(max_level):
    # Initialize base parameters
    base_xp = 50
    base_multiplier = 1.2
    xp_needed = []

    # Calculate XP for each level up to max_level
    current_xp = base_xp
    for level in range(1, max_level + 1):
        xp_needed.append(current_xp)
        current_xp = int(current_xp * (base_multiplier + (level * 0.05)))

    # Prepare data for plotting
    levels = list(range(1, max_level + 1))

    # Plot the XP requirements
    plt.figure(figsize=(10, 5))
    plt.plot(levels, xp_needed, marker='o')

    # Annotate every 10th level
    for level in range(10, max_level + 1, 10):
        plt.annotate(f"{xp_needed[level-1]} XP", 
                     xy=(level, xp_needed[level-1]), 
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center')

    # Set titles and labels
    plt.title('XP Required to Level Up')
    plt.xlabel('Level')
    plt.ylabel('XP Required')
    plt.xticks(levels)
    plt.grid()
    plt.show()

#calculate_and_plot_xp_graph(50)

def calculate_and_plot_xp_graph2(max_level, save_as_image=False, filename="xp_graph.png", dpi=300):
    # Initialize base parameters
    base_xp = 50
    base_multiplier = 1.2
    xp_needed = []

    # Calculate XP for each level up to max_level
    current_xp = base_xp
    for level in range(1, max_level + 1):
        xp_needed.append(current_xp)
        current_xp = int(current_xp * (base_multiplier + (level * 0.05)))

    # Prepare data for plotting
    levels = list(range(1, max_level + 1))

    # Plot the XP requirements
    plt.figure(figsize=(10, 5))
    plt.plot(levels, xp_needed, marker='o')

    # Annotate every 10th level
    for level in range(10, max_level + 1, 10):
        plt.annotate(f"{xp_needed[level-1]} XP", 
                     xy=(level, xp_needed[level-1]), 
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center')

    # Set titles and labels
    plt.title('XP Required to Level Up')
    plt.xlabel('Level')
    plt.ylabel('XP Required')
    plt.xticks(levels)
    plt.grid()

    # Show or save the plot
    if save_as_image:
        plt.savefig(filename, dpi=dpi)  # Save as high-resolution image
        print(f"Graph saved as '{filename}' with {dpi} dpi.")
    else:
        print("h")
        plt.show()

# Example usage: Save as a high-resolution image
#calculate_and_plot_xp_graph2(50, save_as_image=True, filename="xp_graph_high_res.png", dpi=300)