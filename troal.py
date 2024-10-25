from globals import datetime, pytz, time_format, player_progress_db_json_path

from level_system import Player, load_from_file, get_or_create_player

x = get_or_create_player()
# Example usage of gaining XP
x.gain_xp(120)  # Gain 120 XP
x.xp_needed_for_next_level()  # Show remaining XP needed for next level
#player.gain_xp(300)  # Gain 300 XP, may level up multiple times
#player.xp_needed_for_next_level()