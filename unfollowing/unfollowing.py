import random
import time

from utils.client_interaction import (
    click_following_button_of_profile_page,
    click_program_user_profile_button,
    click_unfollow_button_of_profile_page,
    get_follower_value_of_this_profile,
    get_following_value_of_this_profile,
    get_names_of_followers_on_follower_list_page,
    get_to_user_profile_link,
    scroll_to_bottom,
)
from utils.data import add_line_to_data_file, get_most_recent_stats


"""
unfollowing.py -> every function related to the unfollowing state of the program
"""


# main method for the unfollowing state of the program
def unfollowing_main(
    driver, logger, following_lower_limit, unfollow_wait_time, username
):
    """main method for the unfollowing state of the program

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object
        following_lower_limit (int): the lower limit of following
        unfollow_wait_time (int): the time to wait between unfollowing users

    Returns:
        string: The next state of the program

    """

    logger.log(message="Initiating unfollowing state...", state="Unfollowing")
    while 1:
        logger.log('Checking following value before continuing with unfollowing state...')
        my_stats = get_my_stats(driver, logger, username)

        my_following_value = my_stats[0]

        if my_following_value < following_lower_limit:
            logger.log(
                message="Following lower limit reached! Passing to following state...",
                state="unfollowing",
            )
            return "following"

        # get a list of my followers
        logger.log(
            message=f"Getting a list of people the program user follows",
            state="Unfollowing",
        )
        following_list = cut_following_list_size(
            get_following_list_of_program_user(driver, logger,username)
        )
        logger.log(
            message=f"Retrieved a list of {len(following_list)} users to unfollow",
            state="Unfollowing",
        )

        unfollow_users(driver, logger, unfollow_wait_time, user_list=following_list)


# method to cut the list of followers to a random 20
def cut_following_list_size(following_list):
    """method to cut the list of followers to a random 20

    Args:
        following_list (String[]): list of usernames

    Returns:
        string[]: list of random 20 usernames from the given list

    """
    random.shuffle(following_list)
    new_list = []
    for n in range(20):
        new_list.append(following_list[n])
    return new_list


# method to get the program user's following/follower stats
def get_my_stats(driver, logger, username):
    """method to get the program user's following/follower stats

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object

    Returns:
        int,int: the program user's following , follower values

    """
    get_to_user_profile_link(driver, logger, username)
    time.sleep(3)

    following_value = get_following_value_of_this_profile(driver)
    follower_value = get_follower_value_of_this_profile(driver)

    # update to logger
    logger.update_current_following(following_value)
    logger.update_current_followers(follower_value)

    update_data_file(logger, follower_value, following_value)

    return following_value, follower_value


# method to get a list of followings of a given user
def get_following_list_of_program_user(driver, logger,username):
    """method to get a list of followings of a given user

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object

    Returns:
        string[]: list of usernames

    """
    # get to user profile

    # click_program_user_profile_button(driver, logger)
    get_to_user_profile_link(driver, logger, username)

    # click following button
    click_following_button_of_profile_page(driver, logger)
    time.sleep(3)

    # scroll down to load follower elements
    for _ in range(4):
        logger.log(message="Loading more followers...", state="following")
        scroll_to_bottom(driver, logger)
        time.sleep(2)

    name_list = get_names_of_followers_on_follower_list_page(driver, logger)
    return remove_duplicates_from_list(name_list)


# method to remove duplicate strings from a list of strings
def remove_duplicates_from_list(name_list):
    """method to remove duplicate strings from a list of strings

    Args:
        name_list (string[]): list of usernames

    Returns:
        string[]: list of usernames with no duplicates

    """
    new_list = []
    for name in name_list:
        if not name in new_list:
            new_list.append(name)
    return new_list


# method to unfollow a given user
def unfollow_user(driver, logger, user):
    """method to unfollow a given user

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object
        user (string): the username of the user to unfollow

    Returns:
        None

    """
    start_time = time.time()
    get_to_user_profile_link(driver, logger, user)
    time.sleep(1)
    if click_unfollow_button_of_profile_page(driver, logger) == "success":
        logger.add_unfollow()
        logger.log(
            message=f"Unfollowed {user} in {str(time.time()-start_time)[:4]} seconds",
            state="Unfollowing",
        )
    logger.log(
        message=f"Failed to unfollow {user} in {str(time.time()-start_time)[:4]} seconds",
        state="Unfollowing",
    )


# method to unfollow a given list of users
def unfollow_users(driver, logger, unfollow_wait_time, user_list):
    """method to unfollow a given list of users

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object
        unfollow_wait_time (int): the time to wait between unfollows
        user_list (string[]): list of usernames

    Returns:
        None

    """
    random.shuffle(user_list)
    for user in user_list:
        unfollow_user(driver, logger, user)
        time.sleep(unfollow_wait_time)


# method to add a line of data to the data file
def update_data_file(logger, input_follower_value, input_following_value):
    """method to add a line of data to the data file

    Args:
        logger (utils.logger.Logger): the logger object
        follower_value (int): the number of followers
        following_value (int): the number of followings

    Returns:
        None

    """
    #if new values are off significantly from previous just skip this time
        #follower, following
    most_recent_stats = get_most_recent_stats()
    if (abs(int(most_recent_stats[0]) - int(input_follower_value)) > 50) or (abs(int(most_recent_stats[1]) - int(input_following_value)) > 50):
        return


    line = str(input_follower_value) + "|" + str(get_date_time()) + "|" + str(input_following_value)
    add_line_to_data_file(line)
    logger.log(message="Updated data file...", state="Unfollowing")


# method to get the current date and time in a readable format
def get_date_time():
    """method to get the current date and time in a readable format

    Args:
        None

    Returns:
        string: the current date and time in a readable format

    """
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())

