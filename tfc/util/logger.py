import os
import time
from functools import wraps
from queue import Queue


class Logger:
    """Handles creating and reading logs"""

    def __init__(self, queue=None, timed=True):
        """Logger init"""

        self.queue: Queue[dict[str, str | int]] = Queue() if queue is None else queue

        self.start_time = time.time()
        self.unfollows = 0
        self.follows = 0
        self.accounts_examined = 0
        self.targets_added = 0
        self.current_mode = None
        self.targets_left = 0
        self.current_followers = None
        self.current_following = None
        self.current_state = 'Idle'
        self.errored = False
        
        self.starting_followers = None
        self.starting_following = None

        self.followers_change = 0
        self.following_change = 0


    
    def _update_queue(self):
        """updates the queue with a dictionary of mutable statistics"""
        if self.queue is None:
            return

        statistics: dict[str, str | int] = {
            "current_status": self.current_mode,
            "time_since_start": self.calc_time_since_start(),
            "unfollows": self.unfollows,
            "follows": self.follows,
            "accounts_examined": self.accounts_examined,
            "targets_left": self.targets_left,
            "targets_added": self.targets_added,
            "current_state": self.current_state,
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
    def error(self, message: str):
        """logs an error"""
        self.errored = True
        self.status = f"Error: {message}"
        print(f"Error: {message}")

    @_updates_queue
    def log(self, message):
        """add message to log

        Args:
            message (str): message to add
        """
        targets_in_target_list = count_targets_in_target_list()
        targets_added = self.targets_added
        unfollows = self.unfollows

        logger_stats_string = f"{self.make_timestamp()}||{self.current_mode}||{self.follows} follows||{unfollows} unfollows||{self.accounts_examined} accounts examined||{targets_in_target_list} targets left||{targets_added} new targets added||"
        
        print(logger_stats_string, message)

    @_updates_queue
    def change_current_status(self, new_status):
        self.current_mode = new_status

    @_updates_queue
    def add_target_added(self):
        """add unfollow tally to log"""
        self.targets_added += 1
    
    @_updates_queue
    def update_current_followers_stat(self,stat):
        self.current_followers = stat
        self.followers_change  = self.calc_followers_change()
    
    @_updates_queue
    def update_current_following_stat(self,stat):
        self.current_following = stat
        self.following_change  = self.calc_following_change()
    
    @_updates_queue
    def update_current_state(self,state):
        self.current_state = state
    
    @_updates_queue
    def update_starting_followers_stat(self,stat):
        if self.starting_followers != None: return
        self.starting_followers = stat
        self.followers_change  = self.calc_followers_change()
    
    @_updates_queue
    def update_starting_following_stat(self,stat):
        if self.starting_following != None: return
        self.starting_following = stat
        self.following_change  = self.calc_followers_change()
    
    

    @_updates_queue
    def add_unfollow(self):
        """add unfollow tally to log"""
        self.unfollows += 1

    @_updates_queue
    def add_follow(self):
        """add unfollow tally to log"""
        self.follows += 1

    @_updates_queue
    def update_targets_left(self, targets_left):
        """add unfollow tally to log"""
        self.targets_left = targets_left

    @_updates_queue
    def add_account_examined(self):
        """add restart to log"""
        self.accounts_examined += 1

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

    def calc_followers_change(self):
        #calc the change as an int
        if self.current_followers is None or self.starting_followers is None:
            followers_change=0
        else: followers_change = self.current_followers - self.starting_followers

        #put a plus in front if needed, then return as string
        if followers_change > 0:
            followers_change = "+" + str(followers_change)
        else:
            followers_change = str(followers_change)
        
        return followers_change
    
    def calc_following_change(self):
        print(f"current_following is {self.current_following} \n starting_following is {self.starting_following}")
        
        #calc the change as an int
        if self.current_following is None or self.starting_following is None:
            following_change='0'
        else: following_change = self.current_following - self.starting_following

        #put a plus in front if needed, then return as string
        if int(following_change) > 0:
            following_change = "+" + str(following_change)
        else:
            following_change = str(following_change)

        return following_change
    


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


