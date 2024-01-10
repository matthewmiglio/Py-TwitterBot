import threading

import pygetwindow as gw

GUI_NAME = "Twitterbot v0.0.1"

FIREFOX_NAME = "Mozilla Firefox"


def get_window_pos(name):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        return window.topleft
    except IndexError:
        return None


def move_window(name, x, y):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        window.moveTo(x, y)
    except IndexError:
        return None


def get_window_size(name):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        return window.size
    except IndexError:
        return None


def resize_window(name, w, h):
    try:
        window = gw.getWindowsWithTitle(name)[0]
        window.resizeTo(w, h)
    except IndexError:
        return None


def get_firefox_window():
    name = "Mozilla Firefox"
    try:
        window = gw.getWindowsWithTitle(name)[0]
        return window
    except IndexError:
        return None


# method to get all window names
def get_all_window_names():
    return [window.title for window in gw.getAllWindows()]


def move_firefox_to_gui():
    gui_pos = get_window_pos(GUI_NAME)

    guiw, gui_h = get_window_size(GUI_NAME)

    move_window(FIREFOX_NAME, gui_pos[0] + guiw - 15, gui_pos[1])


def resize_firefox():
    # get res of gui
    w, h = get_window_size(GUI_NAME)
    h -= 1

    resize_window(FIREFOX_NAME, h, h)


def check_positions():
    gui_pos = get_window_pos(GUI_NAME)
    firefox_pos = get_window_pos(FIREFOX_NAME)

    x_diff = abs(gui_pos[0] - firefox_pos[0])

    y_diff = abs(gui_pos[1] - firefox_pos[1])

    # print(x_diff,y_diff)

    x_diff -= 857

    # if x diff is more than 1 away from 731, return False
    if x_diff > 1:
        print("x_diff", x_diff)
        return False

    # if y diff is more than 1 away from 0, return False
    if y_diff > 1:
        print("y_diff", y_diff)
        return False

    return True


def check_sizes():
    guiw, gui_h = get_window_size(GUI_NAME)

    firefoxw, firefoxh = get_window_size(FIREFOX_NAME)

    height_diff = abs(gui_h - firefoxh) - 2
    height_diff = abs(height_diff)

    if height_diff > 1:
        return False

    return True


def docker_main():
    while 1:
        try:
            # if not check_sizes():
            #     print("Resize")
            #     resize_firefox()

            if not check_positions():
                print("Dock")
                move_firefox_to_gui()
        except:
            pass


def start_dock_mode():
    print("Starting docking...")
    threading.Thread(target=docker_main).start()


if __name__ == "__main__":
    start_dock_mode()
