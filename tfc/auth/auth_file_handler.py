from tfc.interface import THEME
import PySimpleGUI as sg
import os


def get_appdata_directory():
    return os.getenv("APPDATA")


#####methods for twitterbot folder
def make_twitterbot_folder():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    os.mkdir(directory)
    print(f"Made twitterbot folder @ {directory}")


def check_if_twitterbot_folder_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot"
    return os.path.exists(directory)


# methods for creds file
def make_creds_file():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    with open(directory, "w") as f:
        f.write('id = ""\n')
        f.write('consumer_key = ""\n')
        f.write('consumer_key_secret = ""\n')
        f.write('user_access_key = ""\n')
        f.write('access_secret_key = ""\n')
    print(f"Made creds file @ {directory}")


def check_if_creds_file_exists():
    directory = get_appdata_directory() + r"\py-TwitterBot" + r"\creds.txt"
    return os.path.exists(directory)


def check_if_creds_are_exmpty():
    creds = get_creds()
    for cred in creds:
        if cred != "":
            return False
    return True


def get_creds():
    user_id = ""
    consumer_key = ""
    consumer_key_secret = ""
    user_access_key = ""
    access_secret_key = ""

    lines = get_lines_in_creds_file()
    for line in lines:
        if line.startswith("consumer_key_secret"):
            consumer_key_secret = parse_string_for_cred_reading(
                "consumer_key_secret", line
            )

        elif line.startswith("consumer_key"):
            consumer_key = parse_string_for_cred_reading("consumer_key", line)

        elif line.startswith("id"):
            user_id = parse_string_for_cred_reading("id", line)
        elif line.startswith("user_access_key"):
            user_access_key = parse_string_for_cred_reading("user_access_key", line)
        elif line.startswith("access_secret_key"):
            access_secret_key = parse_string_for_cred_reading("access_secret_key", line)

    return (
        user_id,
        consumer_key,
        consumer_key_secret,
        user_access_key,
        access_secret_key,
    )


def get_lines_in_creds_file():
    path = os.getenv("APPDATA") + r"\py-TwitterBot" + r"\creds.txt"
    with open(path, "r") as f:
        return f.readlines()


def parse_string_for_cred_reading(cred_key, string_to_chop):
    return_string = ""

    # remove the name of this cred
    first_remove_length = len(cred_key) + 4
    string_to_chop = string_to_chop[first_remove_length:]

    # add chars until you hit a "
    for char in string_to_chop:
        if char != '"':
            return_string += char
        else:
            break

    return return_string


def show_missing_auth_file_gui(location):
    out_text = (
        "TWITTER API CREDENTIALS FILE IS MISSING.\n\n"
        + f"Please write in your Twitter API Credentials in the file at [{location}] in the format outlined in the new file.\n"
        + "Restart the program after these changes..."
    )
    sg.theme(THEME)
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("CRITICAL ERROR- User Action Required", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()


def show_missing_creds_in_auth_file_gui(location):
    out_text = (
        "TWITTER API CREDENTIALS MISSING IN creds.txt!\n\n"
        + f"Please write in your Twitter API Credentials in the file at [{location}] in the format outlined in the new file.\n"
        + "Restart the program after these changes..."
    )
    sg.theme(THEME)
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("CRITICAL ERROR- User Action Required", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()


if not check_if_twitterbot_folder_exists():
    make_twitterbot_folder()

if not check_if_creds_file_exists():
    make_creds_file()

if check_if_creds_are_exmpty():
    show_missing_creds_in_auth_file_gui(
        os.getenv("APPDATA") + r"\py-TwitterBot" + r"\creds.txt"
    )
    exit()
