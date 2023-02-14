import os


# method to get the appdata directory
def get_appdata_directory():
    return os.getenv("APPDATA")


# method to make the target_list.txt file at appdata/roaming/Py-TwitterBot\target_list.txt
def make_target_list_file():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    with open(directory, "w") as f:
        f.write("")
    print(f"Made target_list_file @ {directory}")


# method to check if target_list.txt exists in appdata/roaming/Py-TwitterBot
def check_if_target_list_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    return os.path.exists(directory)


# method to add a line to appdata/roaming/Py-TwitterBot\target_list.txt
def add_line_to_target_list_file(line):
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    with open(directory, "a") as f:
        f.write(line + "\n")


# method to make the appdata/roaming/Py-TwitterBot folder
def make_twitterbot_folder():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    os.mkdir(directory)
    print(f"Made twitterbot folder @ {directory}")


# method to check if the appdata/roaming/Py-TwitterBot folder exists
def check_if_twitterbot_folder_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    return os.path.exists(directory)


# method to make the appdata/roaming/Py-TwitterBot\target_list_history.txt file
def make_target_history_file():
    directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list_history.txt"
    )
    with open(directory, "w") as f:
        f.write("")
    print(f"Made target_list_history file @ {directory}")


# method to check if the appdata/roaming/Py-TwitterBot\target_list_history.txt file exists
def check_if_target_history_list_exists():
    directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list_history.txt"
    )
    return os.path.exists(directory)


# method to add a line to appdata/roaming/Py-TwitterBot\target_list.txt file
def add_line_to_target_list_file(line):
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    with open(directory, "a") as f:
        f.write(line + "\n")


# method to add a line to the appdata/roaming/Py-TwitterBot\target_list_history.txt file
def add_line_to_target_history_file(line):
    directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list_history.txt"
    )
    with open(directory, "a") as f:
        f.write(line + "\n")


# method to remove the first line of a given file
def remove_first_line_of_target_list_file():
    target_list_directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    )
    with open(target_list_directory, "r") as f:
        lines = f.readlines()
    with open(target_list_directory, "w") as f:
        for line in lines[1:]:
            f.write(line)


# method to get the first line of a given file
def get_first_line_of_target_list_file():
    target_list_directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    )
    with open(target_list_directory, "r") as f:
        lines = f.readlines()
    try:
        return lines[0]
    except:
        return None


# method to remove then return the first line of the target_list.txt file
def get_next_target():
    next_target_string = get_first_line_of_target_list_file()
    remove_first_line_of_target_list_file()
    return next_target_string


# method to check if a line is in a given file
def check_if_target_in_target_history_file(target_name):
    target_history_directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list_history.txt"
    )
    with open(target_history_directory, "r") as f:
        lines = f.readlines()
    for line in lines:
        if line == (target_name):
            return True
    return False


# method to count the amoutn of targets in the appdata/roaming/Py-TwitterBot\target_list.txt file
def count_targets_in_target_list_file():
    target_history_directory = (
        get_appdata_directory() + r"\py-TwitterBot" + r"\target_list.txt"
    )
    with open(target_history_directory, "r") as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        count += 1
    return count


# import this file to run these methods before running any code
# methods to make the appdata/roaming/Py-TwitterBot folder and target_list.txt and target_list_histoy.txt file if they don't exist
if not check_if_twitterbot_folder_exists():
    make_twitterbot_folder()

if not check_if_target_history_list_exists():
    make_target_history_file()

if not check_if_target_list_exists():
    make_target_list_file()
