from my_modules import os
from trial import Trial_class

main_path = "./Cue Cards"
program = Trial_class()

MDs, SDs_combined, SDs_comb_with_name = [], [], []

for MD in os.scandir(main_path):
    MDs.append(MD.name)
    MD_path = f"{main_path}/{MD.name}"
    cards_combined, xx, cards_in_MD = [], [], 0

    for SD in os.scandir(MD_path):
        SD_path = f"{MD_path}/{SD.name}"
        card_paths = [f"{SD_path}/{card.name}" for card in os.scandir(SD_path)]
        cards_in_MD += len(card_paths)

        # Process cards in SD
        repeat_range = program.row_calc(len(card_paths))
        listpro = program.image_cropper(card_paths)

        # Combine cropped images row by row
        image_rows = [
            program.image_combiner([
                listpro[x] for x in program.grid_maker(i + 1, len(card_paths))
            ], "hor", program.important_vars("Card gap"))
            for i in range(repeat_range)
        ]

        cc = program.image_combiner(image_rows, "ver",
                                    program.important_vars("Card gap"))

        xx.append(program.add_name_2(cc, f"{SD.name} - {len(card_paths)}"))

    y = program.image_combiner(xx, "ver", program.important_vars("Card gap"))

    SDs_comb_with_name.append(
        program.add_name_2(y, f"{MD.name} - {cards_in_MD}"))

MDs_combined = program.image_combiner(SDs_comb_with_name, "hor",
                                      program.important_vars("Card gap"))

final = program.add_name_2(MDs_combined, "Cue Cards")

# Specify the filename and directory path
filename = "Cue Cards.jpg"
directory = "./"

# Combine the directory and filename into a full path
file_path = os.path.join(directory, filename)

if os.path.exists(file_path):
    print(f"'{filename}' exists. Deleting...")
    os.remove(file_path)

final.save(filename)
print("Saved!")
file_size = round((os.path.getsize(file_path) / (1024**2)), 2)
print(
    f"File size: {file_size} MB\nFile dimensions: {final.width} x {final.height}"
)
