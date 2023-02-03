from tweepy import TweepyException
import urllib.request
import time
from tfc.auth.auth import get_creds, make_api
from tfc.data import add_line_to_data_file
from tfc.targetting.target_finding_file import (
    count_targets_in_target_list_file,
    get_next_target,
)


api = make_api()
creds = get_creds()
screen_name = api.get_user(user_id=creds[0]).screen_name


# main for the following mode of the state tree
def following_main(logger, following_upper_limit, follow_wait_time):
    # runs until one of two cases
    # 1. following count >= following_upper_limit  -> returns 'unfollow' as new state string
    # 2. targets in target list is 0  -> returns 'get_targets' as new state string

    # on loop:
    # get the top name in the file of targets called target_list.txt and remove it from the list
    # get a list of users that follow that user
    # follow all of those users
    while True:
        # get this target
        logger.update_targets_left(count_targets_in_target_list_file())
        this_target = get_next_target()

        # if this target is "" then the list is empty so break and end program.
        if (this_target == "") or (this_target is None):
            logger.change_current_status(
                "Ran out of targets... \nTerminating following mode."
            )
            return "get_targets"

        # terminal print this_target
        logger.change_current_status(f"New target is: {this_target}")

        # increment accounts examined
        logger.add_account_examined()

        # get list of people that follow this target
        this_list_to_follow = remove_user_screen_name_from_follower_list(
            get_follower_list(logger, count=100, screen_name=this_target, timeout=15)
        )

        # follow everyone in that list
        if (
            follow_users(
                logger,
                user_list=this_list_to_follow,
                following_upper_limit=following_upper_limit,
                follow_wait_time=follow_wait_time,
            )
            == "following upper limit"
        ):
            return "unfollowing"


# method to check if the program has internet
def check_for_internet():
    try:
        urllib.request.urlopen("http://google.com")  # Python 3.x
        return True
    except:
        return False


# method to wait for the program to get internet
def wait_for_internet(logger):
    loops = 0
    print("Waiting for internet...")
    while not check_for_internet():
        time.sleep(1)
        loops += 1
        if loops % 1700 == 0:
            logger.change_current_status("Waiting for internet...")


# function to get a list of followers of a given size for a given scre[=e==='[en name
def get_follower_list(logger, count=100, screen_name="", timeout=0):
    try:
        followers = api.get_followers(count=count, screen_name=screen_name)
        follower_name_list = []
        for follower in followers:
            follower_name_list.append(follower.screen_name)
        return follower_name_list
    except Exception as e:
        if not check_for_internet():
            "No internet caused error getting follower list. Waiting for internet..."
            wait_for_internet()
            return get_follower_list(logger, count, screen_name, timeout)
        else:
            if timeout > 3800:
                timeout = 3800
            print(
                "Error getting follower list. Waiting "
                + str(timeout)
                + " seconds before trying again."
            )
            time.sleep(timeout)
            return get_follower_list(
                logger, count, screen_name, timeout=int(timeout * 1.3)
            )


# function to follow a given list of users
def follow_users(logger, user_list=[], following_upper_limit=None, follow_wait_time=0):
    # null param check
    if following_upper_limit is None:
        return "null param"

    for user in user_list:
        add_line_to_data_file((make_data_string(logger)))
        logger.update_targets_left(count_targets_in_target_list_file())
        follow_user(logger, screen_name=user, timeout=15)

        # if at following_upper_limit, break
        following_count = get_following_count(logger, screen_name, timeout=15)
        if int(following_count) > int(following_upper_limit):
            logger.change_current_status(
                f"Following upper limit reached: {following_count}. Quitting following mode..."
            )
            return "following upper limit"

        logger.change_current_status(
            f"Manual wait time of [{follow_wait_time}s] after following [{user}]"
        )
        time.sleep((int(follow_wait_time)))


def make_data_string(logger):
    user_id = creds[0]
    user_screen_name = api.get_user(user_id=user_id).screen_name

    try:
        followers_count = count_followers(
            logger=logger, screen_name=user_screen_name, timeout=15
        )
        following_count = count_following(api.get_user(user_id=creds[0]).screen_name,timeout=15)
    except:
        print('Error making data string for data file in following.py in make_data_string()')
        return

    # update the followers and following stats in the logger obj
    logger.update_current_followers_stat(followers_count)
    logger.update_current_following_stat(following_count)

    followers_count_string = (
        str(followers_count) + "|" + str(get_date_time()) + "|" + str(following_count)
    )
    return followers_count_string


# method to get the following count of a given profile name
def get_following_count(logger, profile_name, timeout):
    try:
        following_count = api.get_user(user_id=creds[0]).friends_count
        return following_count
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        print(
            f"Error getting following count...\nWaiting {timeout} sec then retrying..."
        )
        print(f"Error getting following count: {e}")
        time.sleep(timeout)
        return get_following_count(logger, profile_name, timeout=int(timeout * 1.3))


def check_create_friendship_output(text):
    out = text.find("following=")
    following_text = text[out : out + 15]

    if "True" in following_text:
        return "already following"
    return "success"


# method to remove 'the user's screen name' from any list
def remove_user_screen_name_from_follower_list(follower_list=[]):
    try:
        this_screen_name = api.get_user(user_id=creds[0]).screen_name
    except:
        timeout_time=5
        print(f"Error getting the users screen name. Waiting {timeout_time} seconds before trying again...")
        time.sleep(timeout_time)
        remove_user_screen_name_from_follower_list(follower_list=follower_list) 


    return_list = []
    for name in follower_list:
        if name != this_screen_name:
            return_list.append(name)
        else:
            pass
    return return_list


# method to count the followers of a given ID
def count_followers(logger, screen_name="", timeout=0):
    try:
        return api.get_user(screen_name=screen_name).followers_count
    except:
        if timeout > 3800:
            timeout = 3800

        print(
            "Error getting followers count for [{screen_name}]. Waiting {timeout} seconds before trying again...",
        )
        time.sleep(timeout)
        return count_followers(
            logger=logger, screen_name=screen_name, timeout=int(timeout * 1.75)
        )


# method to count how many people a given screen name is following
def count_following(screen_name="",timeout=0):
    try:
        return api.get_user(screen_name=screen_name).friends_count
    except:
        if timeout > 3600:timeout = 3600
        
        print(f'Error getting following count of {screen_name}. Waiting {timeout} seconds before trying again...')
        time.sleep(timeout)
        
        return count_following(screen_name=screen_name,timeout=int(timeout*1.75))


# method to get the current date and time in a readable format
def get_date_time():
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())


# method to follow a selected user
def follow_user(logger, screen_name="", timeout=0):
    try:
        api.create_friendship(screen_name=screen_name)
        print(f"Made friendship with {screen_name}")
        logger.change_current_status(f"Successfully followed {screen_name}")
        logger.add_follow()
    except TweepyException as follow_exception:
        # dont let timeout exceed an hour per timeout
        if timeout > 3800:
            timeout = 3800

        # sleep for the timeout
        print(
            f"Sleeping {timeout}s after error occured following user {screen_name}..."
        )
        time.sleep(timeout)

        # read the error message
        error_line = str(follow_exception.args[0])

        # check if this error is due to no internet
        if not check_for_internet():
            print("No internet caused this error")
            logger.change_current_status("No internet...")
            wait_for_internet(logger)

        # check if this error is due to the follower throttle
        elif " are unable to follow more people at thi" in error_line:
            print("Following throttle reached...")
            logger.change_current_status("Following throttle reached...")
            return follow_user(logger, screen_name=screen_name, timeout=(timeout * 1.5))

        else:
            print(
                f"An unknown error occured while following {screen_name}:\n{follow_exception}"
            )
