import PySimpleGUI as sg

from .theme import THEME


def show_help_gui():
    out_text = (
        "Authentication Information\n"
        + "    The program will automatically create a creds.txt file in appdata/roaming/Py-TwitterBot\n"
        + "    Replace the empty fields with your own Twitter API credentials to use the program\n\n"
        +"Controls Information\n"
        + "    1. Following lower limit: The count of people you follow at which the unfollow algorithm will stop unfollowing\n"
        + "    2. Following upper limit: The count of people you follow at which the follow algorithm will stop, then start unfollowing\n"
        + "    3. Targets per cycle: The count of targets per follow cycle [1-10] (1 being the most up-to-date list of followers of the targets)\n"
        + "    4. Profiles to Scrape for Targets: The profiles from which the program will get targets for the following algorithm\n"
        + "    5. Wait time between following: The manual wait time after each follow operation to avoid API throttling (~150s reccomended)\n"




    )

    sg.theme(THEME)
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("Py-TwitterBot", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()
