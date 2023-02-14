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
from utils.data import add_line_to_data_file


# main method for the unfollowing state of the program
def unfollowing_main(driver, logger, following_lower_limit,unfollow_wait_time):
    logger.log(message="Initiating unfollowing state...", state="Unfollowing")
    while 1:
        my_stats = get_my_stats(driver, logger)

        my_following_value = my_stats[0]

        if my_following_value < following_lower_limit:
            logger.log(
                message="Following lower limit reached! Passing to following state...",
                state="unfollowing",
            )
            return "following"

        # get a list of my followers
        logger.log(
            message=f"Getting a list of people the program user follows", state="Unfollowing"
        )
        following_list = cut_following_list_size(
            get_following_list_of_program_user(driver, logger)
        )
        logger.log(
            message=f"Retrieved a list of {len(following_list)} users to unfollow",
            state="Unfollowing",
        )

        unfollow_users(driver, logger,unfollow_wait_time, user_list=following_list)


# method to cut the list of followers to a random 20
def cut_following_list_size(following_list):
    random.shuffle(following_list)
    new_list = []
    for n in range(20):
        new_list.append(following_list[n])
    return new_list


# method to get the program user's following/follower stats
def get_my_stats(driver, logger):
    click_program_user_profile_button(driver, logger)
    time.sleep(3)

    following_value = get_following_value_of_this_profile(driver)
    follower_value = get_follower_value_of_this_profile(driver)

    # update to logger
    logger.update_current_following(following_value)
    logger.update_current_followers(follower_value)

    update_data_file(logger, follower_value, following_value)

    return following_value, follower_value


# method to get a list of followings of a given user
def get_following_list_of_program_user(driver, logger):
    # get to user profile

    click_program_user_profile_button(driver, logger)

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
    new_list = []
    for name in name_list:
        if not name in new_list:
            new_list.append(name)
    return new_list


# method to unfollow a given user
def unfollow_user(driver, logger, user):
    start_time = time.time()
    get_to_user_profile_link(driver, logger, user)
    time.sleep(1)
    if click_unfollow_button_of_profile_page(driver, logger) == "success":
        logger.add_unfollow()
        logger.log(
            message=f"Unfollowed {user} in {str(time.time()-start_time)[:4]} seconds",state='Unfollowing'
        )
    logger.log(
        message=f"Failed to unfollow {user} in {str(time.time()-start_time)[:4]} seconds",state='Unfollowing'
    )


# method to unfollow a given list of users
def unfollow_users(driver, logger,unfollow_wait_time, user_list):
    random.shuffle(user_list)
    for user in user_list:
        unfollow_user(driver, logger, user)
        time.sleep(unfollow_wait_time)


# method to add a line of data to the data file
def update_data_file(logger, follower_value, following_value):
    line = str(follower_value) + "|" + str(get_date_time()) + "|" + str(following_value)
    add_line_to_data_file(line)
    logger.log(message="Updated data file...", state="Unfollowing")


# method to get the current date and time in a readable format
def get_date_time():
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())
