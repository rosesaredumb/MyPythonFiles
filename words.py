from json_functions import json_funcs
from globals import clear_console, words_db_json_path





class Words:
    def __init__(self) -> None:
        self.json_helper = json_funcs()
        self.data = self.json_helper.read_json(words_db_json_path)
        self.chosen_dict = "gojo"

    def add_word(self):
        word = input("Enter the new word: ").lower()
        # Check if the word already exists in the chosen dictionary
        if self.data is not None and self.chosen_dict in self.data:
            if word in self.data[self.chosen_dict]:
                print(f"The word '{word}' already exists in the dictionary.")
                return  # Exit if the word exists

        # Second input: ask for the meaning
            meaning = input("Enter the meaning of the word: ")

        # Add the new word and its meaning to the chosen dictionary
            self.data[self.chosen_dict][word] = meaning
            self.json_helper.write_json(self.data, words_db_json_path)
            print(f"The word '{word}' has been added with the meaning: '{meaning}'.")


    def add_dict(self):
        new_dict_name = input("Enter the name of the new dictionary: ").lower()
        if self.data is not None:
            if new_dict_name not in self.data:
                self.data[new_dict_name] = {}
                self.json_helper.write_json(self.data, words_db_json_path)
                print(f"The dictionary '{new_dict_name}' has been added.")
            else:
                print(f"The dictionary '{new_dict_name}' already exists.")



def main():
    manager = Words()

    while True:
        print("\nOptions:")
        print("1. Add word")
        print("2. Add dictionary")
        print("3. Mark Task as Completed")
        print("4. View Pending Tasks")
        print("5. view all ungrouped tasks")
        print("6. view all categories")
        print("7. view tasks by category")
        print("8. view tasks by priority")
        print("9. view tasks by due date")
        print("10. Quit\n")

        choice = input("Choose an option: ")
        clear_console()

        if choice == '1':  
            manager.add_word()
        elif choice == '2':
            manager.add_dict()
        elif choice == '10':
            print("Exiting task manager.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()