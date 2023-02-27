import os
import time
import webbrowser
from queue import Queue
from threading import Lock, Thread

import PySimpleGUI as sg

import targetting.target_file
import utils.data
from interface import THEME, disable_keys, main_layout, show_help_gui, user_config_keys
from login.creds import get_creds_from_file
from login.login import log_in_to_twitter
from state import state_tree
from utils.caching import (
    cache_program_state,
    cache_user_settings,
    check_for_user_settings_file,
    read_program_state,
    read_user_settings,
)
from utils.chrome_driver import make_chrome_driver
from utils.data import get_follower_count_from_line, get_following_count_from_line
from utils.file_cleaning import clean_selenium_files
from utils.logger import Logger
from utils.plotter.plot_followers import make_new_plot
from utils.thread import StoppableThread

plot_mutex = Lock()

# method for caching the user's GUI settings
def save_current_settings(values):
    # read the currently selected values for each key in user_config_keys
    user_settings = {key: values[key] for key in user_config_keys if key in values}
    # cache the user settings
    cache_user_settings(user_settings)


# method to retrieve the previous runtime's last state
def load_last_state():
    state = read_program_state()

    return state


# method to load the GUI with the previous runtime's saved settings
def load_last_settings(window):
    if check_for_user_settings_file():
        window.read(timeout=10)  # read the window to edit the layout
        user_settings = read_user_settings()
        if user_settings is not None:
            for key in user_config_keys:
                if key in user_settings:
                    window[key].update(user_settings[key])
        window.refresh()  # refresh the window to update the layout


# method to handle the start button event (begins the program)
def start_button_event(logger: Logger, window, values):
    logger.log(message="Starting", state="Idle")

    for key in disable_keys:
        window[key].update(disabled=True)

    # PACK ARGS from gui to thread
    args = (
        values["following_lower_limit"],
        values["following_upper_limit"],
        values["profiles_to_scrape_for_targets"],
        values["follow_wait_time"],
        values["unfollow_wait_time"],
    )

    thread = WorkerThread(logger, args)
    thread.start()

    # enable the stop button after the thread is started
    window["Stop"].update(disabled=False)

    return thread


# method to handle the stop button event (stops the program)
def stop_button_event(logger: Logger, window, thread):
    logger.set_current_status("Stopping")
    window["Stop"].update(disabled=True)
    shutdown_thread(thread)  # send the shutdown flag to the thread


# method to handle the closing of a thread
def shutdown_thread(thread, join=False):
    if thread is not None:
        thread.shutdown_flag.set()
        if join:
            # wait for the thread to close
            thread.join()  # this will block the gui


# method to update the GUI's display vars
def update_layout(window: sg.Window, logger: Logger):
    # comm_queue: Queue[dict[str, str | int]] = logger.queue
    window["time_since_start"].update(logger.calc_time_since_start())  # type: ignore

    with plot_mutex:
        window["data_figure"].update(os.path.join(os.environ["APPDATA"], "py-TwitterBot", "data_figure.png"))  # type: ignore

    # update the statistics in the gui
    if not logger.queue.empty():
        # read the statistics from the logger
        for stat, val in logger.queue.get().items():
            window[stat].update(val)  # type: ignore


# main method of the entire Py-TwitterBot program
def main():
    # clean residuial selenium files
    clean_selenium_files()

    # start the plotting thread
    plotter_thread = PlotWorkerThread()
    plotter_thread.start()

    # start the worker thread (the thread that runs the bot)
    thread: WorkerThread | None = None
    comm_queue: Queue[dict[str, str | int]] = Queue()
    logger = Logger(comm_queue, timed=False)  # dont time the inital logger

    # window layout
    window = sg.Window("Py-TwitterBot", main_layout)

    # load the last settings from the previous runtime
    load_last_settings(window)

    # start timer for autostart
    start_time = time.time()
    auto_start_time = 30  # seconds
    auto_started = False

    # run the gui
    while True:
        # get gui vars
        read = window.read(timeout=100)
        event, values = read or (None, None)

        # check if bot should be autostarted
        if (
            thread is None
            and values is not None
            and values["autostart"]
            and not auto_started
            and time.time() - start_time > auto_start_time
        ):
            auto_started = True
            event = "Start"

        if event in [sg.WIN_CLOSED, "Exit"]:
            # shut down the thread if it is still running
            shutdown_thread(thread)
            break

        if event == "Start":
            # start the bot with new queue and logger
            comm_queue = Queue()
            logger = Logger(comm_queue)
            thread = start_button_event(logger, window, values)

        elif event == "Stop":
            stop_button_event(logger, window, thread)

        elif event == "Help":
            show_help_gui()

        elif event == "Donate":
            webbrowser.open(
                "https://www.paypal.com/donate/"
                + "?business=YE72ZEB3KWGVY"
                + "&no_recurring=0"
                + "&item_name=Support+my+projects%21"
                + "&currency_code=USD"
            )

        elif event == "issues-link":
            webbrowser.open(
                "https://github.com/matthewmiglio/py-tarkbot/issues/new/choose"
            )

        elif event in user_config_keys:
            save_current_settings(values)

        # handle when thread is finished
        if thread is not None and not thread.is_alive():
            # enable the start button and configuration after the thread is stopped
            for key in disable_keys:
                window[key].update(disabled=False)
            if thread.logger.errored:
                window["Stop"].update(disabled=True)
            else:
                # reset the communication queue and logger
                comm_queue = Queue()
                logger = Logger(comm_queue, timed=False)
                thread = None

        update_layout(window, logger)

    shutdown_thread(thread, join=True)
    shutdown_thread(plotter_thread, join=True)

    window.close()


# test method for running any specific function of the program that happens to be buggy
def test_main():
    s = utils.data.get_most_recent_stats()
    print (s)


# the thread that handles the bot
class WorkerThread(StoppableThread):
    def __init__(self, logger: Logger, args, kwargs=None):
        super().__init__(args, kwargs)
        self.logger = logger

    def run(self):
        # unpack the vars from the GUI
        (
            following_lower_limit,
            following_upper_limit,
            profiles_to_scrape_for_targets,
            follow_wait_time,
            unfollow_wait_time,
        ) = self.args  # unpack args from gui to thread

        # convert the number vars from strings to ints
        following_lower_limit = int(following_lower_limit)
        following_upper_limit = int(following_upper_limit)
        follow_wait_time = int(follow_wait_time)
        unfollow_wait_time = int(unfollow_wait_time)

        # load the last state from the previous runtime
        state = load_last_state()

        # create the selenium driver object
        driver = make_chrome_driver()

        # retrieve twitter credentials from the file
        creds = get_creds_from_file()
        username = creds[0]

        log_in_to_twitter(driver, self.logger, username, password=creds[1])
        time.sleep(3)

        # run the program until stopped
        while not self.shutdown_flag.is_set():
            cache_program_state(program_state_string=state)

            # loop the state tree, continually updating the current state to that of the output of the previous state
            state = state_tree(
                driver=driver,
                logger=self.logger,
                state=state,
                scrape_list=profiles_to_scrape_for_targets,
                targets_to_find=3,
                following_upper_limit=following_upper_limit,
                following_lower_limit=following_lower_limit,
                follow_wait_time=follow_wait_time,
                unfollow_wait_time=unfollow_wait_time,
                username=username,
            )


# the thread that handles the plotting
class PlotWorkerThread(StoppableThread):
    def __init__(self):
        super().__init__(args=None, kwargs=None)

    def run(self):
        # Make a new plot and save it to the appdata/roaming/Py-TwitterBot folder every 200 seconds
        figure_update_delay = 280

        # loop this until the program is stopped
        while not self.shutdown_flag.is_set():
            print("PLOT: Making a new plot")
            with plot_mutex:
                make_new_plot()
            print(f"PLOT: Made a new plot... sleeping {figure_update_delay} seconds")

            time.sleep(figure_update_delay)


if __name__ == "__main__":
    # main()
    test_main()
