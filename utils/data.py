import PIL
from PIL import Image
import os
import datetime


"""
data.py -> every function related to storing of follower and following data in appdata/roaming/Py-TwitterBot\data.txt
"""

# method to get the directory of the user's appdata
def get_appdata_directory():
    """method to get the directory of the user's appdata

    Args:
        None

    Returns:
        string: the directory of the user's appdata

    """

    return os.getenv("APPDATA")


# method to make the data file at appdata/roaming/Py-TwitterBot\data.txt
def make_data_file():
    """method to make the data file at appdata/roaming/Py-TwitterBot\data.txt

    Args:
        None

    Returns:
        None

    """
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    with open(directory, "w") as f:
        f.write(f'0|{datetime.datetime.now().strftime("%m/%d/%Y")}|12:00:00|0\n')
    print(f"Made data file @ {directory}")


# method to make the appdata/roaming/Py-TwitterBot folder
def make_twitterbot_folder():
    """method to make the appdata/roaming/Py-TwitterBot folder

    Args:
        None

    Returns:
        None

    """
    directory = get_appdata_directory() + r"\py-TwitterBot"
    os.mkdir(directory)
    print(f"Made twitterbot folder @ {directory}")


# method to check if the appdata/roaming/Py-TwitterBot folder exists
def check_if_twitterbot_folder_exists():
    """method to check if the appdata/roaming/Py-TwitterBot folder exists

    Args:
        None

    Returns:
        bool: True if the folder exists, False if it doesn't

    """
    directory = get_appdata_directory() + r"\py-TwitterBot"
    return os.path.exists(directory)


# method to check if the appdata/roaming/Py-TwitterBot\data.txt file exists
def check_if_data_file_exists():
    """method to check if the appdata/roaming/Py-TwitterBot\data.txt file exists

    Args:
        None

    Returns:
        bool: True if the file exists, False if it doesn't

    """
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    return os.path.exists(directory)


# method to add a line to the data file
def add_line_to_data_file(line):
    """method to add a line to the data file

    Args:
        line (string): the line to add to the data file

    Returns:
        None

    """
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    with open(directory, "a") as f:
        f.write(line + "\n")


# method to check if the data_figure.png file exists in the twitterbot folder
def check_if_data_figure_exists():
    """method to check if the data_figure.png file exists in the twitterbot folder

    Args:
        None

    Returns:
        bool: True if the file exists, False if it doesn't

    """
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data_figure.png"
    return os.path.exists(directory)


# method to save a blank image to the data_figure.png file location
def save_blank_data_figure_image():
    print('Made a blank data figure image for first-time run.')
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data_figure.png"
    im = PIL.Image.new(mode="RGB", size=(700, 500))
    im.save(directory)



# run this code upon import: make sure twitterbot folder, data file, and data figure image all exist
if not check_if_data_figure_exists():
    save_blank_data_figure_image()


if not check_if_twitterbot_folder_exists():

    make_twitterbot_folder()
    make_data_file()

elif not check_if_data_file_exists():
    make_data_file()
