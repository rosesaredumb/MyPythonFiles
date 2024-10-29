from discord import player
from json_functions import json_funcs
from globals import clear_console, words_db_json_path
import random
from level_system import get_or_create_player


class Words:
    def __init__(self) -> None:
        self.t_correct = "total_no_of_times_correct"
        self.t_called = "total_no_of_times_called"
        json_format = {
            "dict_albums": {
                "ungrouped" : {},
            },
            self.t_correct: 0,
            self.t_called: 0,
            "dict_being_used": "",
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
        self.chosen_dict = self.data["dict_being_used"] or "ungrouped"

    
    def add_word(self):
        word = input("Enter the new word: ").lower()  
        if self.data and self.data["dict_albums"] is not None and self.chosen_dict in self.data["dict_albums"]:
            # Check if the word already exists
            if word in self.data["dict_albums"][self.chosen_dict]:
                print(f"The word '{word}' already exists in the dictionary.")
                return  # Exit if the word exists
            # Ask for the meaning if the word does not exist
            meaning = input("Enter the meaning of the word: ").lower()
            # Add the new word and its meaning
            self.data["dict_albums"][self.chosen_dict][word] = meaning
            self.json_helper.write_json(self.data, words_db_json_path)
            print(f"The word '{word}' has been added with the meaning: '{meaning}'.")

 
    def add_dict(self):
        new_dict_name = input("Enter the name of the new dictionary: ").lower()
        # Check if "dict_albums" exists and if the new dictionary already exists within it
        if self.data is not None and self.data["dict_albums"] is not None:
            if new_dict_name not in self.data["dict_albums"]:
                # Add the new dictionary under "dict_albums"
                self.data["dict_albums"][new_dict_name] = {}
                self.json_helper.write_json(self.data, words_db_json_path)
                print(f"The dictionary '{new_dict_name}' has been added.")
            else:
                print(f"The dictionary '{new_dict_name}' already exists.")


    def get_random_word(self):
        # Access the specified dictionary inside "dict_albums"
        if self.data:  
            target_dict = self.data.get("dict_albums", {}).get(self.chosen_dict, {})
            # Check if the dictionary has any entries
            if target_dict:
                # Select and return a random word from the dictionary
                print(random.choice(list(target_dict.keys())))
                self.data
            else:
                print(f"The dictionary '{self.chosen_dict}' is empty or does not exist.")

    def cross_checker(self):
        x = input("press y/n")
        if x == "y":
            self.player.gain_xp(self.xp_for_correct_ans)
            print("Remembered the word!")
            if self.data:
                self.data[self.t_correct] += 1
                self.json_helper.write_json(self.data, words_db_json_path)
        elif x == "n":
            print("Forgot the word")
            

    def set_dict_being_used(self):
        new_dict = input("Enter the name of the dictionary to use: ").lower()
        if self.data and new_dict in self.data["dict_albums"]:
            self.chosen_dict = new_dict
            self.data["dict_being_used"] = new_dict
            self.json_helper.write_json(self.data, words_db_json_path)
            print(f"The dictionary '{new_dict}' is now being used.")
        else:
            print(f"The dictionary '{new_dict}' does not exist.")
        


def main():
    manager = Words()

    while True:
        print("\nOptions:")
        print("0. Quit")
        print("1. Add word")
        print("2. Add dictionary")
        print("3. Get random word")
        print("4. set dict being used")
        print("5. view all ungrouped tasks")
        print("6. view all categories")
        print("7. view tasks by category")
        print("8. view tasks by priority")
        print("9. view tasks by due date")
        
        
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