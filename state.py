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
        state = following_main(
            driver, logger, following_upper_limit, follow_wait_time, username
        )

    elif state == "unfollowing":
        state = unfollowing_main(
            driver, logger, following_lower_limit, unfollow_wait_time, username
        )

    elif state == "targetting":
        state = targetting_main(
            driver,
            logger,
            scrape_list,
            username,
            targets_to_find,
            following_maximum=following_upper_limit,
        )

    logger.set_current_state(state)
    cache_program_state(state)
    return state
