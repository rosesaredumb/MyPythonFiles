import os
import re
from typing import Literal

from PIL import Image, ImageDraw, ImageFont


class Trial_class:

    def __init__(self):
        self.path = "./Cue Cards"
        self.new_card_wd = 300
        self.SD_font_size = 25
        self.no_of_columns = 5
        self.total_img_count = self.count_all_files_in_directory(self.path)

    def add_name_above_image(self, blank_path, image_text: str, imagex):

        img = Image.open(blank_path)
        font_size = 50
        try:
            font = ImageFont.truetype("./Vera.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        wd, ht = imagex.size

        resized_blank = self.image_resizer(img, wd, (font_size + 10))

        draw = ImageDraw.Draw(resized_blank)

        bbox = draw.textbbox((0, 0), image_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        #text_width, text_height = font.getsize(image_name)

        text_x = (resized_blank.width - text_width) / 2
        text_y = (resized_blank.height - text_height) / 2

        draw.text((text_x, text_y), image_text, fill="black", font=font)

        listz = []
        listz.append(resized_blank)
        listz.append(imagex)

        zz = self.image_combiner(listz, "ver", 5)

        return zz

    def add_name_2(self, image, text):

        font_size = self.SD_font_size
        try:
            font = ImageFont.truetype("./Vera.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        blankHt = font_size + 10

        new_image_height = image.height + blankHt
        new_image = Image.new("RGB", (image.width, new_image_height),
                              (255, 255, 255))

        # Create a drawing object and add text
        draw = ImageDraw.Draw(new_image)

        bbox = draw.textbbox((0, 0), text, font=font)

        text_height = bbox[3] - bbox[1]

        text_x = 10
        text_y = (blankHt - text_height) // 2
        draw.text((text_x, text_y), text, font=font, fill="black")

        new_image.paste(image, (0, blankHt))

        return new_image

    def row_calc(self, no_of_images: int):
        """
        Calculates no.of rows of images based on 
        the no.of columns and no.of images.

        Args:
            no_of_images (int): Total no.of images in the grid.

        Returns:
            int: The total number of rows for the grid.
        """
        return (int(no_of_images) + self.no_of_columns -
                1) // self.no_of_columns

    def important_vars(self, item_name: str):

        Card_gap = self.SD_font_size // 8
        SD_Bpic_Ht = self.SD_font_size + 10
        cropped_card_wd = int(0.98 * self.new_card_wd)
        SD_Bpic_Wd = ((cropped_card_wd * self.no_of_columns))
        #(Card_gap * (self.no_of_columns - 1))

        vars = {
            "SD font size": self.SD_font_size,
            "MD font size": ((self.SD_font_size * 1.2) - 5),
            "Title font size": ((self.SD_font_size + 5) * 1.4) - 5,
            "Card gap": Card_gap,
            "SD gap": Card_gap + 10,
            "MD gap": Card_gap + 30,
            "SD name gap": Card_gap + 5,
            "MD name gap": Card_gap + 20,
            "SD Bpic Ht": SD_Bpic_Ht,
            "MD Bpic Ht": SD_Bpic_Ht * 1.2,
            "Title Bpic Ht": SD_Bpic_Ht * 1.4,
            "SD Bpic Wd": SD_Bpic_Wd,
            "Card Wd": self.new_card_wd,
            "left crop": 0.01,
            "top crop": 0.14,
            "right crop": 0.99,
            "bottom crop": 0.76,
            "Left offset": 5,
            "NoC": self.no_of_columns
        }
        #new_dict = json.dumps(new_dict)
        return vars[f"{item_name}"]

    def grid_maker(self, repeat_index: int, no_of_images: int):
        """
        Provides a list of indexes for images of that specific row.

        Args:
            repeat_index (int): is the row number.
            no_of_images (int): total no.of images in the grid.

        Returns:
            list: A list of numbers which are the indexes 
            for the images in that specific row.
        """
        range_beginning = (repeat_index *
                           self.no_of_columns) - (self.no_of_columns - 1)
        range_end = min(repeat_index * self.no_of_columns, no_of_images)
        return [item - 1 for item in range(range_beginning, range_end + 1)]

    def image_resizer(self, image, new_width, new_height):

        y = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return y

    def image_cropper(self, paths):
        '''
        [image paths] is input
        '''
        zz = []
        for img_path in paths:
            im = Image.open(img_path)

            width, height = im.size
            new_height = int((self.new_card_wd / width) * height)

            resized_img = self.image_resizer(im, self.new_card_wd, new_height)

            left = int(self.important_vars("left crop") * self.new_card_wd)
            top = int(0.14 * new_height)
            right = int(0.99 * self.new_card_wd)
            bottom = int(0.76 * new_height)

            im1 = resized_img.crop((left, top, right, bottom))
            zz.append(im1)
        return zz

    def count_all_files_in_directory(self, path):
        return sum(len(files) for _, _, files in os.walk(path))

    def get_files(self):
        """
        Retrieves a tuple

        Returns:
            tuple: Consisting of the main folders, dictionary of decks, 
            all the image paths, total no.of images
        """
        MDs = []
        card_paths = []
        mydict = {}
        for MD in os.scandir(self.path):
            MDs.append(MD.name)
            mydict[MD.name] = [
                SD.name for SD in os.scandir(f"{self.path}/{MD.name}")
            ]
            card_paths.extend([
                f"{self.path}/{MD.name}/{SD.name}/{card.name}"
                for SD in os.scandir(f"{self.path}/{MD.name}")
                for card in os.scandir(f"{self.path}/{MD.name}/{SD.name}")
            ])

        total_card_count = len(card_paths)

        return MDs, mydict, card_paths, total_card_count

    def image_renamer(self, paths):
        for img_path in paths:
            Image.open(img_path).convert("RGB").save(
                re.sub(".png", ".jpg", img_path, flags=re.IGNORECASE))
            os.remove(img_path)

    def image_combiner(self, images: list, axis: Literal["hor", "ver"],
                       gap: int):
        """
        Combines images in the desired axis.

        Args:
            images (list): A list of images.
            axis (Literal["hor", "ver"]): The axis of 
            combining the images (hor / ver).

        Returns:
            PIL.Image.Image: The combined image.
        """
        sizes = [img.size for img in images]
        widths, heights = zip(*sizes)

        if axis == "hor":
            result_size = (sum(widths), max(heights))
            offsets = [(sum(widths[:i]) + (gap * i), 0)
                       for i in range(len(images))]
        else:
            result_size = (max(widths), sum(heights))
            offsets = [(0, sum(heights[:i]) + (gap * i))
                       for i in range(len(images))]

        result = Image.new('RGB', result_size, (255, 255, 255))
        for img, offset in zip(images, offsets):
            result.paste(img, offset)

        return result
