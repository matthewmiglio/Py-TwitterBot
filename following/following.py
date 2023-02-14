import random
import time

from targetting.target_file import get_next_target

from utils.client_interaction import (
    check_for_login_popup_after_following_on_profile_page,
    check_for_throttle_popup,
    check_for_unfollow_popup_after_following_on_profile_page,
    click_follow_button_of_profile_page,
    click_follower_button_of_profile_page,
    click_program_user_profile_button,
    get_follower_value_of_this_profile,
    get_following_value_of_this_profile,
    get_names_of_followers_on_follower_list_page,
    get_to_user_profile_link,
    scroll_to_bottom,
)
from utils.data import add_line_to_data_file

# main method for the following state of the program
def following_main(driver, logger, following_upper_limit, follow_wait_time):
    while 1:
        # get a new target
        this_target = get_next_target()
        logger.log(message=f"Next target is {this_target}", state="Following")

        # if target is empty pass to targetting state
        if this_target is None:
            logger.log(
                message="Ran out of targets in following state... passing to targetting state",
                state="following",
            )
            return "targetting"

        logger.add_account_targetted()
        follower_list_of_this_target = get_followers_of_user(
            driver, logger, user=this_target
        )

        my_stats = get_my_stats(driver, logger)
        my_following_value = my_stats[1]
        if int(my_following_value) > int(following_upper_limit):
            logger.log(
                message=f"Following limit reached. Stopping following",
                state="following",
            )
            return "targetting"

        users_followed = follow_users(
            driver,
            logger,
            user_list=follower_list_of_this_target,
            wait_time=follow_wait_time,
        )
        logger.log(
            message=f"Successfully followed {users_followed} users this loop...",
            state="Following",
        )


# method to get the program user's following/follower stats
def get_my_stats(driver, logger):
    click_program_user_profile_button(driver, logger)
    time.sleep(3)

    following_value = get_following_value_of_this_profile(driver)
    follower_value = get_follower_value_of_this_profile(driver)

    # update to logger
    logger.update_current_following(following_value)
    logger.update_current_followers(follower_value)

    update_data_file(
        logger=logger, follower_value=follower_value, following_value=following_value
    )

    return follower_value, following_value


# method to get a list of followers of a given user
def get_followers_of_user(driver, logger, user):
    # get to user profile

    logger.log(
        message=f"Getting to {parse_string(user)}'s profile to get their follower list",
        state="Following",
    )
    get_to_user_profile_link(driver, logger, user)

    # click followers button
    click_follower_button_of_profile_page(driver, logger)
    time.sleep(3)

    # scroll down to load follower elements
    for _ in range(8):
        logger.log(message="Loading more followers...", state="following")
        scroll_to_bottom(driver, logger)
        time.sleep(2)

    name_list = get_names_of_followers_on_follower_list_page(driver, logger)
    return remove_duplicates_from_list(name_list)


# method to remove problematic chars from a string
def parse_string(string):
    new_string = ""
    for char in string:
        if char != " " and char != "\n" and char != "\t":
            new_string += char
    return new_string


# method to remove duplicate strings from a list of strings
def remove_duplicates_from_list(name_list):
    new_list = []
    for name in name_list:
        if not name in new_list:
            new_list.append(name)
    return new_list


# method to follow a given username
def follow_user(driver, logger, user):
    get_to_user_profile_link(driver, logger, user)
    time.sleep(3)
    if (
        click_follow_button_of_profile_page(driver, logger) == "success"
        and not check_for_login_popup_after_following_on_profile_page(driver, logger)
        and not check_for_unfollow_popup_after_following_on_profile_page(driver, logger)
    ):
        time.sleep(1.5)
        if not check_for_throttle_popup(driver, logger):
            logger.add_follow()
            return "success"
    return "fail"


# method to follow a given list of usernames
def follow_users(driver, logger, user_list, wait_time=0):
    
    users_followed = 0
    random.shuffle(user_list)
    for user in user_list:
        start_time = time.time()
        follow_return = follow_user(driver, logger, user)
        end_time = time.time()
        if follow_return == "success":
            users_followed += 1
            logger.log(
                message=f"Followed {user} in {str(end_time-start_time)[:4]} seconds",
                state="Following",
            )
            logger.log(
                message=f"Sleeping [{wait_time}] seconds after following [{user}]...",
                state="Following",
            )
            time.sleep(wait_time)
        else:
            logger.log(
                message=f"Failed to follow {user} in {str(end_time-start_time)[:4]} seconds",
                state="Following",
            )

        if random.randint(0,2)==0:
            logger.log(message='Taking profile data in between following users...',state='Following')
            my_stats=get_my_stats(driver, logger)
            update_data_file(logger, follower_value=my_stats[0], following_value=my_stats[1])

    return users_followed


# method to add a line of data to the data file
def update_data_file(logger, follower_value, following_value):


    line = str(follower_value) + "|" + str(get_date_time()) + "|" + str(following_value)
    add_line_to_data_file(line)
    logger.log(message="Updated data file...", state="following")


# method to get the current date and time in a readable format
def get_date_time():
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())
