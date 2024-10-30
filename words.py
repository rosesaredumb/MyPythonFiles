from discord import player
from json_functions import json_funcs
from globals import clear_console, words_db_json_path
import random
from level_system import get_or_create_player
from typing import Literal

class Words:
    def __init__(self) -> None:
        self.t_correct = "total_no_of_times_correct"
        self.t_called = "total_no_of_times_called"
        self.input_bulletin = ">>"
        self.response_bulletin = "--"
        self.error_bulletin = "!!"
        json_format = {
            "dict_albums": {
                "ungrouped" : {},
            },
            self.t_correct: 0,
            self.t_called: 0,
            "dict_being_used": "ungrouped",
        }
        self.json_helper = json_funcs()
        try:
            self.data = self.json_helper.read_json(words_db_json_path)
            if not isinstance(self.data, dict):
                print("Warning: Data read is invalid. Initializing a new structure.")
                self.data = json_format
            elif "dict_albums" not in self.data:
                print("Warning: 'dict_albums' key not found. Adding default structure.")
                self.data["dict_albums"] = {}
        except Exception as e:
            print(f"Error reading JSON data: {e}. Initializing empty structure.")
            self.data = json_format
        self.player = get_or_create_player()
        self.xp_for_adding_word = 200
        self.xp_for_correct_ans = 450
        self.chosen_dict = self.data["dict_being_used"]


    def mprint(self, sentence: str, type: Literal[1, 2, 3] = 1) -> str:
        if type not in {1, 2, 3}:
            raise ValueError("Type must be '1' or '2'")
        if type == 1:
            x = str(input(f"{self.input_bulletin}{sentence}"))
            return x
        elif type == 2:
            print(f"{self.response_bulletin}{sentence}")
            return ''
        elif type == 3:
            print(f"{self.error_bulletin}{sentence}")
            return ''

    
    def add_word(self):
        word = self.mprint(f"Current dict: |{self.chosen_dict}|. Enter the new word: ").lower()
        if self.data and self.data["dict_albums"] is not None and self.chosen_dict in self.data["dict_albums"]:
            # Check if the word already exists
            if word in self.data["dict_albums"][self.chosen_dict]:
                self.mprint(f"'{word}' already exists in |{self.chosen_dict}|.", 3)
                return  # Exit if the word exists
            # Ask for the meaning if the word does not exist
            meaning = self.mprint("Enter the meaning of the word: ").lower()
            # Add the new word and its meaning
            self.data["dict_albums"][self.chosen_dict][word] = meaning
            for dict_name, inner_dict in self.data["dict_albums"].items():
                # Sort the inner dictionary by keys and update the dictionary
                sorted_inner_dict = dict(sorted(inner_dict.items()))
                self.data["dict_albums"][dict_name] = sorted_inner_dict
            self.json_helper.write_json(self.data, words_db_json_path)
            self.mprint(f"'{word}': '{meaning}' added to |{self.chosen_dict}|.", 2)
            self.player.gain_xp(self.xp_for_adding_word, show_lvl_up=True)

 
    def add_dict(self):
        new_dict_name = self.mprint("Type the name of the new dictionary: ").lower()
        # Check if "dict_albums" exists and if the new dictionary already exists within it
        if self.data is not None and self.data["dict_albums"] is not None:
            if new_dict_name not in self.data["dict_albums"]:
                # Add the new dictionary under "dict_albums"
                self.data["dict_albums"][new_dict_name] = {}
                self.json_helper.write_json(self.data, words_db_json_path)
                self.mprint(f"|{new_dict_name}| created!", 2)
            else:
                self.mprint(f"|{new_dict_name}| already exists.", 3)


    def get_random_word(self):
        # Access the specified dictionary inside "dict_albums"
        if self.data:  
            target_dict = self.data.get("dict_albums", {}).get(self.chosen_dict, {})
            # Check if the dictionary has any entries
            if target_dict:
                # Select and return a random word from the dictionary
                self.mprint(random.choice(list(target_dict.keys())), 2)
                self.data[self.t_called] += 1
                self.json_helper.write_json(self.data, words_db_json_path)
            else:
                self.mprint(f"|{self.chosen_dict}| is empty or does not exist.", 3)

    def cross_checker(self):
        x = self.mprint("press y/n")
        if x == "y":
            self.player.gain_xp(self.xp_for_correct_ans)
            self.mprint("Remembered the word!", 2)
            if self.data:
                self.data[self.t_correct] += 1
                self.json_helper.write_json(self.data, words_db_json_path)
                self.player.gain_xp(self.xp_for_correct_ans)
        elif x == "n":
            self.mprint("Forgot the word", 2)
            

    def set_dict_being_used(self):
        if self.data and "dict_albums" in self.data and self.data["dict_albums"]:
            dict_list = list(self.data["dict_albums"].keys())

            # Print available dictionaries with their indices
            self.mprint("Available dictionaries:", 2)
            for index, dict_name in enumerate(dict_list):
                print(f"{index}: {dict_name}")

            # Prompt user to choose a dictionary by index
            choice = self.mprint(f"Current dict: |{self.chosen_dict}|. Enter the index of the new dict to use: ")

            # Check if the input is a digit and a valid index
            if choice.isdigit():
                index = int(choice)
                if 0 <= index < len(dict_list):
                    old_dict = self.chosen_dict
                    self.chosen_dict = dict_list[index]
                    self.data["dict_being_used"] = self.chosen_dict
                    self.json_helper.write_json(self.data, words_db_json_path)
                    self.mprint(f"Dict changed from |{old_dict}| to |{self.chosen_dict}|.", 2)
                else:
                    self.mprint("Invalid index. Please choose a valid dictionary index.", 3)
            else:
                self.mprint("Invalid input. Please enter a number corresponding to the index of the dictionary.", 3)
        else:
            self.mprint("No dictionaries found in 'dict_albums'.", 3)
        


def main():
    manager = Words()

    while True:
        print("\nOptions:")
        print("0. Quit")
        print("1. Add word")
        print("2. Add dictionary")
        print("3. Get random word")
        print("4. set dict being used")
        
        
        choice = input("Choose an option: ")
        clear_console()

        if choice == '0':
            print("Exiting program")
            break
        elif choice == '1':  
            manager.add_word()
        elif choice == '2':
            manager.add_dict()
        elif choice == '3':
            manager.get_random_word()
            manager.cross_checker()
        elif choice == '4':
            manager.set_dict_being_used()
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()