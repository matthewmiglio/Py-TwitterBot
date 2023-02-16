import os
import time
from functools import wraps
from queue import Queue

"""
logger.py -> a program-wide logger object for the program that stores usable statistics
"""


class Logger:
    """Handles creating and reading logs"""

    def __init__(self, queue=None, timed=True):
        """Logger init"""

        self.queue: Queue[dict[str, str | int]] = Queue() if queue is None else queue

        self.start_time = time.time()

        self.current_followers = 0
        self.current_following = 0

        self.follows = 0
        self.unfollows = 0
        self.accounts_targetted = 0
        self.new_targets_found = 0
        self.targets_left = count_targets_in_target_list()

        self.current_state = "Idle" #state indicator
        self.current_status = "Waiting for user input..."  #action indicator

        self.errored = False

        self.starting_followers = 0
        self.starting_following = 0

        self.followers_change = 0
        self.following_change = 0

    def _update_queue(self):
        """updates the queue with a dictionary of mutable statistics"""
        if self.queue is None:
            return

        statistics: dict[str, str | int] = {
            "time_since_start": self.calc_time_since_start(),
            "current_state": self.current_state,
            "current_status": self.current_status,
            "unfollows": self.unfollows,
            "follows": self.follows,
            "accounts_examined": self.accounts_targetted,
            "targets_left": self.targets_left,
            "targets_added": self.new_targets_found,
            "current_followers": self.current_followers,
            "current_following": self.current_following,
            "followers_change": self.followers_change,
            "following_change": self.following_change,
        }
        self.queue.put(statistics)

    @staticmethod
    def _updates_queue(func):
        """decorator to specify functions which update the queue with statistics"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._update_queue()  # pylint: disable=protected-access
            return result

        return wrapper

    @_updates_queue
    def set_current_state(self, state):
        self.current_state = state

    @_updates_queue
    def set_current_status(self, status):
        self.current_status = status

    @_updates_queue
    def error(self, message: str):
        """logs an error"""
        self.errored = True
        self.status = f"Error: {message}"
        print(f"Error: {message}")

    @_updates_queue
    def update_current_followers(self, value):
        if self.starting_followers == 0:
            self.starting_followers = value

        self.current_followers = value

        self.followers_change = value - self.current_followers

    @_updates_queue
    def update_current_following(self, value):
        if self.starting_following == 0:
            self.starting_following = value
        self.current_following = value
        self.following_change = value - self.starting_following

    @_updates_queue
    def add_follow(self):
        self.follows += 1
        self.targets_left = count_targets_in_target_list()

    @_updates_queue
    def add_unfollow(self):
        self.unfollows += 1

    @_updates_queue
    def add_account_targetted(self):
        self.accounts_targetted += 1

    @_updates_queue
    def add_new_target_found(self):
        self.new_targets_found += 1
        self.targets_left = count_targets_in_target_list()

    @_updates_queue
    def error(self, message: str):
        """logs an error"""
        self.errored = True
        self.status = f"Error: {message}"
        print(f"Error: {message}")

    @_updates_queue
    def log(self, state="Idle", message=""):
        """add message to log

        Args:
            message (str): message to add
            state (str): state of the program during the message
        """

        following_value = self.current_following
        follower_value = self.current_followers

        follows_value = self.follows
        unfollows_value = self.unfollows

        time_string = f"[{self.make_timestamp()}]"
        state_string = f"[{state}]"
        info_string = f"[{following_value}/{follower_value}followers][{follows_value}Fs/{unfollows_value}UNFs]"

        print(time_string + state_string + info_string + message)
        self.set_current_status(message)

    def calc_time_since_start(self) -> str:
        if self.start_time is not None:
            hours, remainder = divmod(time.time() - self.start_time, 3600)
            minutes, seconds = divmod(remainder, 60)
        else:
            hours, minutes, seconds = 0, 0, 0
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def make_timestamp(self):
        """creates a time stamp for log output

        Returns:
            str: log time stamp
        """
        output_time = time.time() - self.start_time
        output_time = int(output_time)

        time_str = str(self.convert_int_to_time(output_time))

        output_string = time_str

        return output_string

    def convert_int_to_time(self, seconds):
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
        return "%d:%02d:%02d" % (hour, minutes, seconds)


# method to count how many lines are in a given file
def count_targets_in_target_list():
    file_directory = os.getenv("APPDATA") + r"\py-TwitterBot" + r"\target_list.txt"

    try:
        with open(file_directory, "r") as f:
            for i, l in enumerate(f):
                pass
        return i + 1
    except:
        return 0
