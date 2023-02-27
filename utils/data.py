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
    print("Made a blank data figure image for first-time run.")
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data_figure.png"
    im = PIL.Image.new(mode="RGB", size=(700, 500))
    im.save(directory)


# method to get the most recent line of the data file
def get_most_recent_stats():
    """method to get the most recent line of the data file

    Args:
        None

    Returns:
        (int,int) tuple: the most recent follower and following count

    """
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    with open(directory, "r") as f:
        lines = f.readlines()
        line = lines[-1]
        follower_count = get_follower_count_from_line(line)
        following_count = get_following_count_from_line(line)

    return follower_count, following_count


# method to get the follower count from a data line string
def get_follower_count_from_line(line):
    """method to get the follower count from a data line string

    Args:
        line (string): the line to get the follower count from

    Returns:
        int: the follower count

    """

    count = ""
    for char in line:
        if char != "|":
            count += char
        else:
            break
    return count


# method to get the follower count from a data line string
def get_following_count_from_line(line):
    """method to get the following count from a data line string

    Args:
        line (string): the line to get the following count from

    Returns:
        int: the following count

    """

    count = ""
    div_count = 0
    for char in line:
        if char == "\n":
            continue
        if char == "|":
            div_count += 1
            continue
        if div_count == 3:
            count += char
    return count


# run this code upon import: make sure twitterbot folder, data file, and data figure image all exist
if not check_if_data_figure_exists():
    save_blank_data_figure_image()


if not check_if_twitterbot_folder_exists():

    make_twitterbot_folder()
    make_data_file()


elif not check_if_data_file_exists():
    make_data_file()
