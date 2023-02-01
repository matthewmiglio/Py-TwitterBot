import time
import tweepy
from tfc.auth.auth import get_creds, make_api
from tfc.data import add_line_to_data_file


api = make_api()
creds = get_creds()


# main method for the unfollowing mode of the state tree
def unfollowing_main(logger, following_lower_limit=100,unfollow_wait_time=0):
    unfollow_wait_time=int(unfollow_wait_time)
    while True:
        this_list = get_following_list()
        if this_list is None:
            print('Error getting following list... sleeping 10 seconds')
            time.sleep(10)
            continue

        logger.change_current_status(f"Got a list of size  {len(this_list)}")

        # unfollow all users
        for user in this_list:
            unfollow_user(logger, 30, user)
            add_line_to_data_file(make_data_string(logger))

            logger.change_current_status(
                f"Waiting {unfollow_wait_time} seconds before unfollowing next user"
            )
            print(f'Sleeping {unfollow_wait_time} after unfollowing {user}...')
            time.sleep(unfollow_wait_time)

        friends_count = get_following_count_of_user(logger, timeout=15)
        logger.change_current_status(f"Still following {friends_count} users")

        if int(friends_count) < int(following_lower_limit):
            logger.change_current_status(
                f"Stopping unfollow mode because hit manual limit of {following_lower_limit}"
            )
            return "following"


# method to get a list of people that follow me
def get_following_list():
    try:
        following_list = api.get_friends()
        screen_name_list = []
        for user in following_list:
            screen_name_list.append(user.screen_name)
        return screen_name_list
    except Exception as e:
        print(f"Error getting following list: {e}")
        return None


# method to unfollow a user
def unfollow_user(logger, timeout, user):
    try:
        api.destroy_friendship(screen_name=user)
        logger.change_current_status(f"Unfollowed {user}")
        print(f"Unfollowed {user}")
        
        logger.add_unfollow()
    except:
        print(
            f"Error unfollowing {user}. Sleeping {timeout} "
        )
        return unfollow_user(logger, int(timeout * 1.5), user)


# method to get my following count
def get_following_count_of_user(logger, timeout):
    this_screen_name = api.get_user(user_id=creds[0]).screen_name

    try:
        return api.get_user(screen_name=this_screen_name).friends_count
    except:
        logger.change_current_status(
            f"Error getting following count... waiting {timeout} seconds"
        )
        time.sleep(timeout)
        return get_following_count_of_user(logger, timeout * 1.5)


# method to count the followers of a given ID
def count_followers(logger, screen_name="", timeout=0):
    try:
        return api.get_user(screen_name=screen_name).followers_count
    except:
        if timeout > 3800:
            timeout = 3800

        print(
            "Error getting followers count for [{screen_name}]. Waiting {timeout} seconds before trying again..."
        )
        time.sleep(timeout)
        return count_followers(
            logger=logger, screen_name=screen_name, timeout=int(timeout * 1.75)
        )


# method to count how many people a given screen name is following
def count_following(screen_name=""):
    return api.get_user(screen_name=screen_name).friends_count


# method to get the current date and time in a readable format
def get_date_time():
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())


# method to construct the data string that is written to the data file
def make_data_string(logger):
    user_id = creds[0]
    user_screen_name = api.get_user(user_id=user_id).screen_name

    followers_count=count_followers(logger=logger, screen_name=user_screen_name, timeout=15)
    following_count=count_following(api.get_user(user_id=creds[0]).screen_name)

    #update the followers and following stats in the logger obj
    logger.update_current_followers_stat(followers_count)
    logger.update_current_following_stat(following_count)

    
    return (
        str(followers_count)
        + "|"
        + str(get_date_time())
        + "|"
        + str(following_count)
        )
