from globals import datetime, pytz, time_format, player_progress_db_json_path

from level_system import Player, load_from_file
name_p = "Hero"
# Load player or create a new one if it doesn't exist
player = load_from_file()
if player is None:
    player = Player(name_p)
    print(f"New player -{name_p}- created!")# Create a new player if loading fails

# Example usage of gaining XP
player.gain_xp(120)  # Gain 120 XP
player.xp_needed_for_next_level()  # Show remaining XP needed for next level
#player.gain_xp(300)  # Gain 300 XP, may level up multiple times
#player.xp_needed_for_next_level()