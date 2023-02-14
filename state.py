import time
from following.following import following_main
from targetting.targetting import targetting_main
from unfollowing.unfollowing import unfollowing_main
from utils.caching import cache_program_state
from utils.client_interaction import get_to_user_profile_link

"""
state.py -> a file for managing the states of the program.
    targetting state -> Looking through the follower lists of users in the scrape_target_list to find users who's accounts would be suitable follow-spam targets
    following state -> Follow 100 users of every target in target list until following upper limit is reached, or targets run out
    unfollowing state -> Unfollow users until following lower limit is reached

"""


def state_tree(
    driver,
    logger,
    state,
    scrape_list,
    targets_to_find,
    following_upper_limit,
    following_lower_limit,
    follow_wait_time,
    unfollow_wait_time,
    username,
):
    # states: start, following, unfollowing, targetting

    # logger.log(message=f"Current state is: [{state}]", state=state)
    logger.set_current_state(state)

    if state == "start":
        # placeholder state for now
        pass
    elif state == "following":
        state = following_main(driver, logger, following_upper_limit, follow_wait_time)

    elif state == "unfollowing":
        state = unfollowing_main(
            driver, logger, following_lower_limit, unfollow_wait_time
        )

    elif state == "targetting":
        state = targetting_main(driver, logger, scrape_list, username, targets_to_find)

    logger.set_current_state(state)
    cache_program_state(state)
    return state


def get_initial_stats(driver, logger, username):
    # get following and follower values of your own profile
    print("Getting initial stats...")

    # get to your own profile
    get_to_user_profile_link(driver, logger, user=username)

    logger.update_current_followers(read_my_follower_value(driver))
    logger.update_current_following(read_my_following_value(driver))


def read_my_follower_value(driver):
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span",
    ]

    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text1 = element.get_attribute("innerHTML")
            return text1
        except:
            pass


def read_my_following_value(driver):
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
    ]

    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text1 = element.get_attribute("innerHTML")
            return text1
        except:
            pass
