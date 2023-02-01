import os
import time
import webbrowser
from queue import Queue
from threading import Lock, Thread

import PySimpleGUI as sg

import tfc.data
import tfc.targetting.target_finding_file
from tfc.interface import (
    THEME,
    disable_keys,
    main_layout,
    show_help_gui,
    user_config_keys,
)
from tfc.state import state_tree
from tfc.util.caching import (
    cache_program_state,
    cache_user_settings,
    check_for_user_settings_file,
    read_program_state,
    read_user_settings,
)
from tfc.util.logger import Logger
from tfc.util.plotter.plot_followers import make_new_plot
from tfc.util.thread import StoppableThread




plot_mutex = Lock()





def save_current_settings(values):
    # read the currently selected values for each key in user_config_keys
    user_settings = {key: values[key] for key in user_config_keys if key in values}
    # cache the user settings
    cache_user_settings(user_settings)


def load_last_state():
    state=read_program_state()

    return state


def load_last_settings(window):
    if check_for_user_settings_file():
        window.read(timeout=10)  # read the window to edit the layout
        user_settings = read_user_settings()
        if user_settings is not None:
            for key in user_config_keys:
                if key in user_settings:
                    window[key].update(user_settings[key])
        window.refresh()  # refresh the window to update the layout


def start_button_event(logger: Logger, window, values):
    logger.change_current_status("Starting")

    for key in disable_keys:
        window[key].update(disabled=True)

    # setup thread and start it
    args = (
        values["following_lower_limit"],
        values["following_upper_limit"],
        values["targets_to_find"],
        values["profiles_to_scrape_for_targets"],
        values["follow_wait_time"],
    )

    thread = WorkerThread(logger, args)
    thread.start()

    # enable the stop button after the thread is started
    window["Stop"].update(disabled=False)

    return thread


def stop_button_event(logger: Logger, window, thread):
    logger.change_current_status("Stopping")
    window["Stop"].update(disabled=True)
    shutdown_thread(thread)  # send the shutdown flag to the thread


def shutdown_thread(thread, join=False):
    if thread is not None:
        thread.shutdown_flag.set()
        if join:
            # wait for the thread to close
            thread.join()  # this will block the gui


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


def main():
    # start the plotting thread
    plotter_thread = PlotWorkerThread()
    plotter_thread.start()

    thread: WorkerThread | None = None
    comm_queue: Queue[dict[str, str | int]] = Queue()
    logger = Logger(comm_queue, timed=False)  # dont time the inital logger

    # window layout
    window = sg.Window("Py-TwitterBot", main_layout)

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


class WorkerThread(StoppableThread):
    def __init__(self, logger: Logger, args, kwargs=None):
        super().__init__(args, kwargs)
        self.logger = logger

    def run(self):
        try:
            (
                following_lower_limit,
                following_upper_limit,
                targets_to_find,
                profiles_to_scrape_for_targets,
                follow_wait_time,
            ) = self.args  # parse thread args

            state = load_last_state()

            # loop until shutdown flag is set
            while not self.shutdown_flag.is_set():
                #cache the current state to maintain function across multiple instances over time 
                cache_program_state(program_state_string=state)

                state = state_tree(
                    self.logger,
                    state,
                    following_lower_limit,
                    following_upper_limit,
                    targets_to_find,
                    profiles_to_scrape_for_targets,
                    follow_wait_time,
                )


        except Exception as exc:  # pylint: disable=broad-except
            # catch exceptions and log to not crash the main thread
            self.logger.error(str(exc))


class PlotWorkerThread(StoppableThread):
    def __init__(self):
        super().__init__(args=None, kwargs=None)

    def run(self):
        figure_update_delay=280

        # loop until shutdown flag is set
        while not self.shutdown_flag.is_set():
            print("PLOT: Making a new plot")
            with plot_mutex:
                make_new_plot()
            print(f"PLOT: Made a new plot... sleeping {figure_update_delay} seconds")

            time.sleep(figure_update_delay)


if __name__ == "__main__":
    main()
