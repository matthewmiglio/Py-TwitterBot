import os
import datetime

# method to get the directory of the user's appdata
def get_appdata_directory():
    return os.getenv("APPDATA")


# method to make the data file at appdata/roaming/Py-TwitterBot\data.txt
def make_data_file():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    with open(directory, "w") as f:
        f.write(f'0|{datetime.datetime.now().strftime("%m/%d/%Y")}|12:00:00|0\n')
    print(f"Made data file @ {directory}")


# method to make the appdata/roaming/Py-TwitterBot folder
def make_twitterbot_folder():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    os.mkdir(directory)
    print(f"Made twitterbot folder @ {directory}")


# method to check if the appdata/roaming/Py-TwitterBot folder exists
def check_if_twitterbot_folder_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    return os.path.exists(directory)


# method to check if the appdata/roaming/Py-TwitterBot\data.txt file exists
def check_if_data_file_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    return os.path.exists(directory)


# method to add a line to the data file
def add_line_to_data_file(line):
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data.txt"
    with open(directory, "a") as f:
        f.write(line + "\n")


# method to check if the data_figure.png file exists in the twitterbot folder
def check_if_data_figure_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\data_figure.png"
    return os.path.exists(directory)


if not check_if_twitterbot_folder_exists():
    make_twitterbot_folder()
    make_data_file()

elif not check_if_data_file_exists():
    make_data_file()