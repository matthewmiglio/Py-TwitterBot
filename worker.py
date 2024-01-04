import random
import time

from utils.logger import Logger
from utils.thread import PausableThread, ThreadKilled
from firefox.firefox_driver import create_firefox_driver
from twitterbot import login_to_twitter, main_loop, update_data_list_logger_values


def restart_driver(driver, logger):
    if driver is not None:
        driver.quit()

    driver = create_firefox_driver(logger)

    login_to_twitter(driver, logger)

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
                    restart_timeout = random.randint(45, 120)  # s
                    self.logger.change_status(
                        f"Waiting {restart_timeout}s before restarting driver..."
                    )
                    restart_wait(self.logger, restart_timeout)

                    driver = restart_driver(driver, self.logger)

                while self.pause_flag.is_set():
                    time.sleep(0.1)  # sleep for 100ms until pause flag is unset

        except ThreadKilled:
            # normal shutdown
            return

        except Exception as err:  # pylint: disable=broad-except
            # we don't want the thread to crash the interface so we catch all exceptions and log
            # raise e
            self.logger.error(str(err))


def restart_wait(logger, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        time_taken = time.time() - start_time
        time_left = str(duration - time_taken)[:5]
        logger.change_status(f"Waiting {time_left}s more after restart...")

        time.sleep(random.randint(1, 100) / 100)


if __name__ == "__main__":
    d = restart_driver(None, Logger())

    input("Enter to continue")
