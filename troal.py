from globals import datetime, pytz, time_format, player_progress_db_json_path

from level_system import Player

# Load player or create a new one if it doesn't exist
player = Player.load_from_file(player_progress_db_json_path)
if player is None:
    player = Player("Hero")  # Create a new player if loading fails

# Example usage of gaining XP
player.gain_xp(120)  # Gain 120 XP
player.xp_needed_for_next_level()  # Show remaining XP needed for next level
player.gain_xp(300)  # Gain 300 XP, may level up multiple times
player.xp_needed_for_next_level()