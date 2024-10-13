from settings import Literal, Image, ImageDraw, ImageFont, time, timeit, os, subprocess
from trial import Trial_class

prog = Trial_class()


def get_directory():
    """
    Get the current working directory
    """
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)


def program_time(func):
    """
    Gets the time taken for the program to run alone.
    """
    x = timeit.timeit(f"{func}", globals=globals(), number=1)
    return f"{round((x * (10 ** 6)), 2)} μs"


def execution_time(python_script):
    """
    Gets the time taken for the whole program to run including it's dependencies.

    Args:
        python_script (str): The path of the python script.
    """
    start_time = time.time()
    subprocess.run(["python3", python_script])
    end_time = time.time()

    x = end_time - start_time
    return f"{round(x, 2)} s"


def image_renamer_for_ios(self):
    file_name = str(self.shortcut_inp[2])

    alphabets = ''
    numbers = ''
    fin_list = []

    for i in file_name:
        if (i.isdigit()):
            numbers += i
        else:
            alphabets += i

    fin_list.append(alphabets)
    fin_list.append(numbers)

    print(str(fin_list[0] + "-" + fin_list[1] + ".PNG"))


def image_combinerr(images: list, axis: Literal["hor", "ver"]):
    """
    Combines images in the desired axis.

    Args:
        images (list): A list of images.
        axis (Literal["hor", "ver"]): The axis of combining the images (hor / ver).

    Returns:
        PIL.Image.Image: The combined image.
    """
    width_list = []
    height_list = []
    for img in images:
        (width_n, height_n) = img.size
        width_list.append(width_n)
        height_list.append(height_n)

    if axis == "hor":
        result_width = sum(width_list)
        result_height = max(height_list)
        result = Image.new('RGB', (result_width, result_height))

        for imge in images:
            N = images.index(imge)
            if N < 1:
                position = 0
            else:
                position_list = width_list[:N]
                position = sum(position_list)

            result.paste(imge, (position, 0))
        return result

    if axis == "ver":
        result_width = max(width_list)
        result_height = sum(height_list)
        result = Image.new('RGB', (result_width, result_height))

        for imge in images:
            N = images.index(imge)
            if N < 1:
                position = 0
            else:
                position_list = height_list[:N]
                position = sum(position_list)

            result.paste(imge, (0, position))
        return result


def grid_maker(no_of_columns: int, repeat_index: int, no_of_images: int):
    """
    Provides a list of indexes for images of that specific row.

    Args:
        repeat_index (int): is the row number.
        no_of_images (int): total no.of images in the grid.

    Returns:
        list: A list of numbers which are the 
        indexes for the images in that specific row.
    """

    if repeat_index * no_of_columns <= no_of_images:
        range_end = (repeat_index * no_of_columns)
        range_beginning = range_end - (no_of_columns - 1)
        y = list(range(range_beginning, range_end))
        y.append(range_end)

    else:
        range_beginning = (repeat_index * no_of_columns) - (no_of_columns - 1)
        range_end = no_of_images
        y = list(range(range_beginning, range_end))
        y.append(range_end)

    new_list = [item - 1 for item in y]
    return new_list


def row_calc(no_of_columns: int, no_of_images: int):
    no_of_images = int(no_of_images)
    no_of_rows = 0

    if no_of_images % no_of_columns == 0:
        no_of_rows = no_of_images / no_of_columns
    else:
        no_of_rows = (no_of_images // no_of_columns) + 1
    return int(no_of_rows)


def get_files(path):
    MDs = []
    card_paths = []
    mydict = {}
    total_card_count = 0

    for MD in os.scandir(path):
        #if entry.is_dir():
        MDs.append(MD.name)

        mydict[MD.name] = ''
        MD_path = f"{path}/{MD.name}"

        SDs = []
        for SD in os.scandir(MD_path):
            SDs.append(SD.name)
            SD_path = f"{MD_path}/{SD.name}"

            for card in os.scandir(SD_path):
                card_path = f"{MD_path}/{SD.name}/{card.name}"
                card_paths.append(card_path)
                total_card_count += 1

        mydict[MD.name] = SDs

    return MDs, mydict, card_paths, total_card_count


def image_renamer(paths):
    '''
        [image paths] is input
        '''
    for img_path in paths:
        png_img = Image.open(img_path)
        jpg_img = png_img.convert("RGB")

        split_string = img_path.split("/")
        split_string_name = split_string[-1].split(".")

        #pure_img_name is the image name without the extension

        pure_img_name = split_string_name[0]
        file_path = "/".join(split_string[:-1])
        new_img_name = f"{file_path}/{pure_img_name}.jpg"

        jpg_img.save(new_img_name)
        os.remove(img_path)


def add_name_above_image2(blank_path, image_text: str, imagex):

    img = Image.open(blank_path)
    font_size = 50
    try:
        font = ImageFont.truetype("./Vera.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    wd, ht = imagex.size

    resized_blank = prog.image_resizer(img, wd, (font_size + 10))

    draw = ImageDraw.Draw(resized_blank)

    bbox = draw.textbbox((0, 0), image_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (resized_blank.width - text_width) / 2
    text_y = (resized_blank.height - text_height) / 2

    draw.text((text_x, text_y), image_text, fill="black", font=font)

    listz = []
    listz.append(resized_blank)
    listz.append(imagex)

    zz = prog.image_combiner(listz, "ver", 5)
    return zz
