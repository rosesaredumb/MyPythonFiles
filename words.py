from json_functions import json_funcs

path_db = "words.json"


class Words:
    def __init__(self) -> None:
        self.json_helper = json_funcs()
        self.data = self.json_helper.read_json(path_db)
        self.chosen_dict = "gojo"

    def add_word(self):
        word = input("Enter the new word: ")

        # Check if the word already exists in the chosen dictionary
        if self.data is not None and self.chosen_dict in self.data:
            if word in self.data[self.chosen_dict]:
                print(f"The word '{word}' already exists in the dictionary.")
                return  # Exit if the word exists

        # Second input: ask for the meaning
            meaning = input("Enter the meaning of the word: ")

        # Add the new word and its meaning to the chosen dictionary
            self.data[self.chosen_dict][word] = meaning
            self.json_helper.write_json(self.data, path_db)
            print(f"The word '{word}' has been added with the meaning: '{meaning}'.")

x = Words()
x.add_word()