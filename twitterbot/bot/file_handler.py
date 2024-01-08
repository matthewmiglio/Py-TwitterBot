import os
import random
import time

appdata_dir = os.getenv("APPDATA")

BASE_FOLDER_NAME = "TwitterBot"
twitterbot_folder_dir = os.path.join(appdata_dir, BASE_FOLDER_NAME)

whitelist_data_file_name = "whitelist_profile_data.txt"
whitelist_data_file_dir = os.path.join(twitterbot_folder_dir, whitelist_data_file_name)

greylist_data_file_name = "greylist_profile_data.txt"
greylist_data_file_dir = os.path.join(twitterbot_folder_dir, greylist_data_file_name)

blacklist_data_file_name = "blacklist_profile_data.txt"
blacklist_data_file_dir = os.path.join(twitterbot_folder_dir, blacklist_data_file_name)

creds_file_name = "creds.txt"
creds_file_path = os.path.join(twitterbot_folder_dir, creds_file_name)

bot_user_data_file_name = "bot_user_data.txt"
bot_user_data_file_dir = os.path.join(twitterbot_folder_dir, bot_user_data_file_name)


def check_for_twitterbot_folder():
    directory = os.path.join(appdata_dir, BASE_FOLDER_NAME)
    return check_for_folder(directory)


def check_for_folder(directory):
    if os.path.exists(directory):
        return True
    else:
        return False


def make_folder(directory, folder_name):
    path = os.path.join(directory, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def make_text_file(directory, file_name):
    path = os.path.join(directory, file_name)
    if not os.path.exists(path):
        open(path, "w+")
    return path


def make_whitelist_profile_data_file():
    make_text_file(os.path.join(twitterbot_folder_dir), whitelist_data_file_name)


def make_blacklist_profile_data_file():
    make_text_file(os.path.join(twitterbot_folder_dir), blacklist_data_file_name)


def check_for_file(directory, file_name):
    path = os.path.join(directory, file_name)
    return os.path.exists(path)


def make_creds_file():
    make_text_file(os.path.join(twitterbot_folder_dir), "creds.txt")
    with open(os.path.join(twitterbot_folder_dir, "creds.txt"), "w") as f:
        f.write("username:\npassword:")


def add_to_whitelist_file(line):
    add_line_to_file(whitelist_data_file_dir, line)


def add_to_blacklist_file(line):
    add_line_to_file(blacklist_data_file_dir, line)


def add_to_greylist_file(line):
    if check_if_line_exists(greylist_data_file_dir, line):
        return False

    if check_if_line_exists(greylist_data_file_dir, line):
        return False

    add_line_to_file(greylist_data_file_dir, line)

    return True


# method to remove a line from a file given the line and a directory to the text file
def remove_line_from_file(directory, line):
    with open(directory, "r") as f:
        lines = f.readlines()
    with open(directory, "w") as f:
        for l in lines:
            if l.strip("\n") != line:
                f.write(l)


def add_line_to_file(directory, line):
    with open(directory, "a") as f:
        f.write(line + "\n")


def make_greylist_file():
    make_text_file(os.path.join(twitterbot_folder_dir), greylist_data_file_name)


def read_file_lines(directory):
    with open(directory, "r") as f:
        lines = f.readlines()
    return lines


def get_creds():
    lines = read_file_lines(creds_file_path)
    username = None
    password = None
    for l in lines:
        l = l.replace("\n", "")
        l = l.replace(" ", "")
        if "username" in l:
            username = l.split(":")[1].strip("\n")
        elif "password" in l:
            password = l.split(":")[1].strip("\n")

    return username, password


def check_for_invalid_creds():
    creds = get_creds()
    if creds[0] == "" or creds[1] == "":
        return True

    # if either password or username or under length of 3, return True
    if len(creds[0]) < 3 or len(creds[1]) < 3:
        return True

    return False


# method to check if a line exists in a given text file
def check_if_line_exists(directory, line):
    with open(directory, "r") as f:
        lines = f.readlines()
    for l in lines:
        if l.strip("\n") == line:
            return True
    return False


def count_greylist_profiles():
    lines = read_file_lines(greylist_data_file_dir)
    return len(lines)


def count_whitelist_profiles():
    lines = read_file_lines(whitelist_data_file_dir)
    return len(lines)


def count_blacklist_profiles():
    lines = read_file_lines(blacklist_data_file_dir)
    return len(lines)


def get_name_from_greylist_file():
    lines = read_file_lines(greylist_data_file_dir)
    line = random.choice(lines)

    # remove the line
    remove_line_from_file(greylist_data_file_dir, line)
    remove_line_from_file(greylist_data_file_dir, line.replace("\n", ""))

    line = line.replace("\n", "")
    return line.replace(" ", "")


def get_name_from_whitelist_file():
    lines = read_file_lines(whitelist_data_file_dir)
    line = random.choice(lines)

    # remove the line
    remove_line_from_file(whitelist_data_file_dir, line)
    remove_line_from_file(whitelist_data_file_dir, line.replace("\n", ""))

    add_to_blacklist_file(line)

    line = line.replace("\n", "")
    return line.replace(" ", "")


def check_if_line_exists_in_whitelist(line):
    for l in read_file_lines(whitelist_data_file_dir):
        if l.strip("\n") == line:
            return True

    return False


def check_if_line_exists_in_blacklist(line):
    for l in read_file_lines(blacklist_data_file_dir):
        if l.strip("\n") == line:
            return True

    return False


def make_bot_user_data_file():
    make_text_file(os.path.join(twitterbot_folder_dir), bot_user_data_file_name)


def add_line_to_data_file(follower_count, following_count):
    line = f"NEW_DELIMITER{follower_count}NEW_DELIMITER{following_count}NEW_DELIMITER{time.time()}NEW_DELIMITER"
    add_line_to_file(bot_user_data_file_dir, line)


def file_setup():
    if not check_for_twitterbot_folder():
        make_folder(appdata_dir, BASE_FOLDER_NAME)
        print("  Made twitterbot folder")

    if not check_for_file(twitterbot_folder_dir, whitelist_data_file_name):
        make_whitelist_profile_data_file()
        print("  Made whitelist data file")

    if not check_for_file(twitterbot_folder_dir, blacklist_data_file_name):
        make_blacklist_profile_data_file()
        print("  Made blacklist data file")

    if not check_for_file(twitterbot_folder_dir, creds_file_name):
        make_creds_file()
        print("  Made creds file")
    if not check_for_file(twitterbot_folder_dir, greylist_data_file_name):
        make_greylist_file()
        print("  Made greylist data file")

    if not check_for_file(twitterbot_folder_dir, bot_user_data_file_name):
        make_bot_user_data_file()
        print("  Made bot user data file")


def change_delimiter():
    # bot_user_data_file_dir =

    # get all lines from data file
    lines = read_file_lines(bot_user_data_file_dir)

    # print all lines
    new_lines = []
    for l in lines:
        print(l)
        l = l.replace("JJ ", "NEW_DELIMITER")
        l = l.replace("NEW_DELIMITER ", "NEW_DELIMITER")
        print(l)
        new_lines.append(l)

    # remove all lines frmo data file
    open(bot_user_data_file_dir, "w").close()

    # add all lines back to data file
    for l in new_lines:
        add_line_to_file(bot_user_data_file_dir, l)


if __name__ == "__main__":
    change_delimiter()
    file_setup()
