import psutil

"""import logging for file logging"""
import logging
import threading
import time
from functools import wraps


def round_down_int(this_float):
    return int(this_float - (this_float % 1))


class Logger:
    def __init__(
        self,
        stats: dict[str, str | int] | None = None,
    ):
        # stats for threaded communication
        self.stats = stats
        self.stats_mutex = threading.Lock()

        # bot stats
        self.runtime = self.calc_runtime()
        self.current_state = "Idle"
        self.start_time = time.time()
        self.restarts = 0
        self.time_of_last_restart = None
        self.active_drivers = None

        # bot progress stats
        self.follows = 0
        self.follows_per_minute = None
        self.unfollows = 0
        self.time_of_last_follow = None

        # bot user profile stats
        self.bot_user_following_value = 0
        self.bot_user_follower_value = 0

        # file stats
        self.whitelist_count = 0
        self.greylist_count = 0
        self.blacklist_count = 0

        # write initial values to queue
        self._update_stats()

    def check_if_can_follow(self) -> bool:
        # follow timeout = 4 minutes
        follow_timeout = 4 * 60

        if self.time_of_last_follow is None:
            return True

        time_since_last_follow = time.time() - self.time_of_last_follow

        if time_since_last_follow > follow_timeout:
            return True

        return False

    def set_time_of_last_restart(self):
        self.time_of_last_restart = time.time()

    def check_if_should_restart(self):
        restart_increment = 10 * 60

        time_of_last_restart = self.time_of_last_restart

        time_since_last_restart = time.time() - time_of_last_restart

        print(f"It has been {time_since_last_restart}s since last restart")

        if time_since_last_restart > restart_increment:
            return True

        return False

    def calc_runtime(self):
        try:
            t = time.time() - self.start_time
            t = self.format_runtime(t)
        except:
            return "0:00:00"

        return t

    def calc_follows_per_minute(self):
        try:
            start_time = self.start_time
            time_taken = time.time() - start_time
            follows = self.follows
            follows_per_second = follows / time_taken
            follows_per_minute = follows_per_second * 60
            self.follows_per_minute = str(follows_per_minute)[:4]
        except Exception as e:
            print(f"Failed to calculate follows per minute: {e}")
            self.follows_per_minute = "follows_per_minute"

    def calc_active_drivers(self):
        try:
            pids = []
            for process in psutil.process_iter(["pid", "name"]):
                try:
                    # Print the process name and PID
                    pid = process.info["pid"]
                    name = process.info["name"]
                    if "firefox" in name:
                        pids.append(pid)

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    # Handle exceptions that might occur while accessing process information
                    pass

            self.active_drivers = len(pids)
        except Exception as e:
            print("Failed to count active drivers: ", e)
            self.active_drivers = "0"

    def _update_log(self) -> None:
        self._update_stats()
        logging.info(self.current_state)

    def _update_stats(self) -> None:
        """updates the stats with a dictionary of mutable statistics"""
        self.calc_active_drivers()

        with self.stats_mutex:
            self.stats = {
                "follows": self.follows,
                "unfollows": self.unfollows,
                "status": self.current_state,
                "bot_user_following_value": self.bot_user_following_value,
                "bot_user_follower_value": self.bot_user_follower_value,
                "driver_count": self.active_drivers,
                "restarts": self.restarts,
                "whitelist_count": self.whitelist_count,
                "greylist_count": self.greylist_count,
                "blacklist_count": self.blacklist_count,
                "follows_per_minute": self.follows_per_minute,
            }

    def get_stats(self):
        """get stats"""
        with self.stats_mutex:
            stats = self.stats
        if stats is not None:
            stats["runtime"] = self.calc_runtime()
        return stats

    @staticmethod
    def _updates_log(func):
        """decorator to specify functions which update the queue with statistics"""

        @wraps(func)
        def wrapper(self: "Logger", *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._update_log()  # pylint: disable=protected-access
            return result

        return wrapper

    def log(self, message) -> None:
        """log something to file and logger.change_status to console with time and stats"""
        log_message = f"[{self.current_state}] {message}"
        logging.info(log_message)
        time_string = self.calc_runtime()
        print(f"[{self.current_state}] [{time_string}] {message}")

    def make_time_str(self, seconds) -> str:
        """convert epoch to time

        Args:
            seconds (int): epoch time in int

        Returns:
            str: human readable time
        """
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{hour}:{minutes:02}:{seconds:02}"

    def format_runtime(self, seconds):
        hours = round_down_int(seconds / 3600)
        seconds -= hours * 3600

        minutes = round_down_int(seconds / 60)
        seconds -= minutes * 60

        seconds = int(seconds)

        return f"{hours}:{minutes:02}:{seconds:02}"

    @_updates_log
    def set_current_state(self, state_to_set):
        """set logger's current_state to state_to_set"""
        self.current_state = state_to_set

    @_updates_log
    def add_follow(self):
        """add 1 to follows"""
        self.follows += 1
        self.calc_follows_per_minute()

    @_updates_log
    def set_time_of_last_follow(self):
        self.time_of_last_follow = time.time()

    @_updates_log
    def add_unfollow(self):
        """add 1 to unfollows"""
        self.unfollows += 1

    @_updates_log
    def add_restart(self):
        self.restarts += 1

    @_updates_log
    def set_bot_user_follower_value(self, value):
        prev_value = self.bot_user_follower_value
        if abs(prev_value - value) > 500:
            print(
                "This value is too different from the previous value. Skipping set_bot_user_follower_value()"
            )
            return

        self.bot_user_follower_value = value

    @_updates_log
    def set_bot_user_following_value(self, value):
        prev_value = self.bot_user_following_value
        if abs(prev_value - value) > 500:
            print(
                "This value is too different from the previous value. Skipping set_bot_user_following_value()"
            )
            return

        self.bot_user_following_value = value

    @_updates_log
    def set_whitelist_count(self, value):
        self.whitelist_count = value

    @_updates_log
    def set_greylist_count(self, value):
        self.greylist_count = value

    @_updates_log
    def set_blacklist_count(self, value):
        self.blacklist_count = value

    @_updates_log
    def error(self, message: str) -> None:
        """log error message

        Args:
            message (str): error message
        """
        self.errored = True
        logging.error(message)

    @_updates_log
    def change_status(self, status) -> None:
        """change status of bot in log

        Args:
            status (str): status of bot
        """
        self.current_state = status
        self.log(status)
        self.calc_follows_per_minute()
