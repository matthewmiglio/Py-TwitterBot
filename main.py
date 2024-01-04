"""
This module contains the main entry point for the py-clash-bot program.
It provides a GUI interface for users to configure and run the bot.
"""
import sys
import PySimpleGUI as sg
import os
from PySimpleGUI import Window
from utils.logger import Logger
from worker import WorkerThread
from utils.thread import StoppableThread, PausableThread
from interface.layout import create_window
from threading import Lock
import time
from plotter.plot_followers import make_new_plot, plot_png_dir
from utils.docker import start_dock_mode

# from plotter.plot_followers import make_new_plot

plot_mutex = Lock()

# Set the option to suppress error popups
sg.set_options(suppress_error_popups=True)


def read_window(
    window: sg.Window, timeout: int = 10
) -> tuple[str, dict[str, str | int]]:
    """Method for reading the attributes of the window
    args:
        window: the window to read
        timeout: the timeout for the  read method

    returns:
        tuple of the event and the values of the window

    """

    # have a timeout so the output can be updated when no events are happening
    read_result = window.read(timeout=timeout)  # ms
    if read_result is None:
        print("Window not found")
        sys.exit()
    return read_result


def start_button_event(logger: Logger, window: Window, values) -> WorkerThread | None:
    """method for starting the main bot thread
    args:
        logger, the logger object for for stats storage and logger.change_statusing
        window, the gui window
        values: dictionary of the values of the window
    returns:
        None
    """

    logger.log("Start Button Event")
    logger.change_status(status="Starting the bot!")

    # args: tuple[list[str], int] = (jobs, acc_count)
    thread = WorkerThread(logger, None)
    thread.start()

    # # start the plotting thread
    # plotter_thread = PlotWorkerThread()
    # plotter_thread.start()

    # start the docking thread
    start_dock_mode()

    return thread


def stop_button_event(logger: Logger, window, thread: StoppableThread) -> None:
    """method for stopping the main bot thread
    args:
        logger, the logger object for for stats storage and logger.change_statusing
        window, the gui window
        thread: the main bot thread
    returns:
        None
    """
    logger.change_status(status="Stopping")
    thread.shutdown(kill=False)  # send the shutdown flag to the thread


def pause_resume_button_event(logger: Logger, window, thread: PausableThread) -> None:
    """method for temporarily stopping the main bot thread
    args:
        logger, the logger object for for stats storage and logger.change_statusing
        window, the gui window
        thread: the main bot thread
    returns:
        None
    """
    if thread.toggle_pause():
        logger.change_status(status="Pausing")
        window["-Pause-Resume-Button-"].update(text="Resume")
    else:
        logger.change_status(status="Resuming")
        window["-Pause-Resume-Button-"].update(text="Pause")


# method to check if a file is a valid png image
def is_valid_png(filename: str) -> bool:
    """method to check if a file is a valid png image
    args:
        filename: the filename of the file to check
    returns:
        True if the file is a valid png image, False otherwise
    """
    try:
        with open(filename, "rb") as f:
            return f.read(8) == b"\x89PNG\r\n\x1a\n"
    except:
        return False


def update_layout(window: sg.Window, logger: Logger) -> None:
    """method for updaing the values in the gui's window
    args:
        window, the gui window
        logger, the logger object for for stats storage and logger.change_statusing
    returns:
        None
    """
    window["runtime"].update(logger.calc_runtime())  # type: ignore

    # with plot_mutex:
    try:
        if is_valid_png(plot_png_dir):
            window["data_figure"].update(os.path.join(os.environ["APPDATA"], "TwitterBot", "data_figure.png"))  # type: ignore
    except:
        pass

    # update the statistics in the gui
    stats = logger.get_stats()
    if stats is not None:
        for stat, val in stats.items():
            window[stat].update(val)  # type: ignore


def exit_button_event(thread) -> None:
    """
    Method for handling the exit button event. Shuts down the thread if it is still running.

    Args:
        thread: The thread to be shut down.

    Returns:
        None
    """
    if thread is not None:
        thread.shutdown(kill=True)


def handle_thread_finished(
    window: sg.Window, thread: WorkerThread | None, logger: Logger
):
    """method for handling when the worker thread is finished"""
    # enable the start button and configuration after the thread is stopped
    if thread is not None and not thread.is_alive():
        if thread.logger.errored:
            window["-Pause-Resume-Button-"].update(disabled=True)
        else:
            # reset the logger
            logger = Logger()
            thread = None
    return thread, logger


def main_gui(start_on_run=False, settings: None | dict[str, str] = None) -> None:
    """method for displaying the main gui"""

    # create gui window
    window = create_window()

    # start the plotting thread
    plotter_thread = PlotWorkerThread()
    plotter_thread.start()

    # track worker thread and logger
    thread: WorkerThread | None = None
    logger = Logger()

    # run the gui
    while True:
        event, values = read_window(window, timeout=10)
        if start_on_run:
            event = "Start"
            start_on_run = False

        # on exit event, kill any existing thread
        if event in [sg.WIN_CLOSED, "Exit"]:
            # shut down the thread if it is still running
            exit_button_event(thread)
            break

        # on start event, start the thread
        if event == "start_button":
            logger = Logger()
            thread = start_button_event(logger, window, values)

        # on stop event, stop the thread
        elif event == "Stop" and thread is not None:
            stop_button_event(logger, window, thread)

        # on pause/resume event, pause/resume the thread
        elif event == "-Pause-Resume-Button-" and thread is not None:
            pause_resume_button_event(logger, window, thread)

        # upon changing any user settings, save the current settings
        # elif event in user_config_keys:
        #     save_current_settings(values)

        update_layout(window, logger)

    # shut down the thread if it is still running
    window.close()
    if thread is not None:
        thread.shutdown(kill=True)
        thread.join()


# the thread that handles the plotting
class PlotWorkerThread(StoppableThread):
    def __init__(self):
        super().__init__(args=None, kwargs=None)

    def run(self):
        # Make a new plot and save it to the appdata/roaming/Py-TwitterBot folder every 200 seconds
        print("Initializing plotter thread")
        figure_update_delay = 280

        # loop this until the program is stopped
        while not self.shutdown_flag.is_set():
            # print("PLOT: Making a new plot")
            with plot_mutex:
                try:
                    make_new_plot()
                except:
                    continue
                print(
                    f"PLOT: Made a new plot... sleeping {figure_update_delay} seconds"
                )

                time.sleep(figure_update_delay)


if __name__ == "__main__":
    main_gui()
