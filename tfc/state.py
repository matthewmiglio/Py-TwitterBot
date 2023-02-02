from tfc.auth.auth import make_api
from tfc.auth.auth_file_handler import get_creds
from tfc.following.following import following_main
from tfc.targetting.target_finding import target_finder_main
from tfc.unfollowing.unfollowing import unfollowing_main
import time

api=make_api()
creds=get_creds()

# method to count how many people a given screen name is following
def count_following(user_id="", timeout=0):
    try:
            return api.get_user(user_id=user_id).friends_count
    except:
        if timeout > 3800:
            timeout = 3800

        print(
            f"Error getting following count for user account. Waiting {timeout} seconds before trying again...",)
        time.sleep(timeout)
        return count_following(user_id=user_id,timeout = (timeout*1.5))

# method to count the followers of a given ID
def count_followers(user_id="", timeout=0):

    try:
        return api.get_user(user_id=user_id).followers_count
    except:
        if timeout > 3800:
            timeout = 3800

        print(
            f"Error getting followers count for user account. Waiting {timeout} seconds before trying again...",
            
        )
        time.sleep(timeout)
        return count_followers(
            user_id=user_id, timeout=int(timeout * 1.75)
        )



    


def state_tree(
    logger,
    state,
    following_lower_limit,
    following_upper_limit,
    profiles_to_scrape_for_targets,
    follow_wait_time,
    unfollow_wait_time,
):
    # (Logger      object) of logger Class in utils folder
    # (String)     state is the current state of the program which is recursively passed as the program loops infinitely. (unfollowing, following, get_targets)
    # (INT)        following lower limit is the minimum amount of people your bot should be following
    # (INT)        following upper limit is the maximum amount of people your bot should be following
    # (String[])   profiles_to_scrape_for_targets is a list of profiles to look through for targets. (A larger list implies a more diverse target list)(Using one's own profile is reccomended)
    # (INT)        follow_wait_time is the amount of time to wait between following users (86 -> 1000 follows/day)
    # (INT)        unfollow_wait_time is the amount of time to wait between unfollowing users (lower values like 1-10 work fine but still cause throttling when following again)

    #code to run every state loop
    print(f"This loops state is : {state}")
    following_count=count_following(user_id=creds[0], timeout=30)
    follower_count=count_followers(user_id=creds[0], timeout=30)
    logger.update_starting_following_stat(following_count)
    logger.update_starting_followers_stat(follower_count)


    if state == "start":
        #placeholder state for any first runtime operations that may need to be implemented
        logger.update_current_state('Starting...')
        state = "following"
    
    elif state == "unfollowing":
        logger.update_current_state('Unfollowing')
        state = unfollowing_main(
            logger=logger,
            following_lower_limit=following_lower_limit,
            unfollow_wait_time=unfollow_wait_time,
        )

    elif state == "following":
        logger.update_current_state('Following')
        state = following_main(
            logger=logger,
            following_upper_limit=following_upper_limit,
            follow_wait_time=follow_wait_time,
        )

    elif state == "get_targets":
        logger.update_current_state('Getting targets')
        state = target_finder_main(
            logger=logger,
            profiles_to_scrape_for_targets=profiles_to_scrape_for_targets,
        )


    print(f'Finished state loop. Next state is: {state}')
    return state
