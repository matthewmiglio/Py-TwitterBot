import random
import sys
import time

from twitterbot.firefox.firefox_driver import create_firefox_driver, close_all_firefox
from twitterbot.bot.twitterbot import (
    login_to_twitter,
    main_loop,
    update_data_list_logger_values,
)
from twitterbot.utils.logger import Logger
from twitterbot.utils.thread import PausableThread, ThreadKilled

RESTART_TIMEOUT = 10  # s


def restart_driver(driver, logger: Logger):
    logger.set_time_of_last_restart()

    close_all_firefox()

    if driver is not None:
        driver.quit()

    driver = create_firefox_driver(logger)

    while login_to_twitter(driver, logger) is False:
        logger.change_status("Failed to login to twitter, retrying...")
        try:
            driver.quit()
        except:
            pass
        close_all_firefox()
        driver = create_firefox_driver(logger)

    logger.add_restart()

    return driver


class WorkerThread(PausableThread):
    def __init__(self, logger: Logger, args, kwargs=None) -> None:
        super().__init__(args, kwargs)
        self.logger: Logger = logger

    def run(self) -> None:
        try:
            update_data_list_logger_values(self.logger)
            driver = restart_driver(None, self.logger)

            # loop until shutdown flag is set
            while not self.shutdown_flag.is_set():
                if self.logger.check_if_should_restart():
                    self.logger.change_status(status="Restarting driver...")
                    driver.quit()

                    driver = restart_driver(driver, self.logger)
                else:
                    self.logger.change_status("Skipping autorestart")

                # code to run
                if main_loop(driver, self.logger) is not True:
                    self.logger.change_status(
                        f"Waiting {RESTART_TIMEOUT}s before restarting driver..."
                    )
                    restart_wait(self.logger, RESTART_TIMEOUT)

                    driver = restart_driver(driver, self.logger)

                while self.pause_flag.is_set():
                    time.sleep(0.1)  # sleep for 100ms until pause flag is unset
        except ThreadKilled:
            # normal shutdown
            print("Normal shutdown!")
            sys.exit()

        except Exception as err:  # pylint: disable=broad-except
            # we don't want the thread to crash the interface so we catch all exceptions and log
            print("Unexpected shutdown!")
            self.logger.error(str(err))
            return self.run()


def restart_wait(logger, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        time_taken = time.time() - start_time
        time_left = str(duration - time_taken)[:5]
        logger.change_status(f"Waiting {time_left}s more before restart...")

        time.sleep(random.randint(1, 100) / 100)


if __name__ == "__main__":
    d = restart_driver(None, Logger())

    input("Enter to continue")
