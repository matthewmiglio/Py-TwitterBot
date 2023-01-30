import time
import random
from tfc.auth.auth import make_api
from tfc.auth.auth_file_handler import get_creds
from tfc.targetting.target_finding_file import (
    add_line_to_target_history_file,
    add_line_to_target_list_file,
    check_if_target_in_target_history_file,
    count_targets_in_target_list_file,
)


api = make_api()
creds=get_creds()

# main method for the target finding mode
def target_finder_main(logger, targets_to_find=0, profiles_to_scrape_for_targets=[]):

    logger.change_current_status("Target Finding")

    # null checks
    if targets_to_find == 0:
        logger.change_current_status(
            f"Error in new_target_finder_main(). {targets_to_find} is 0"
        )
    if profiles_to_scrape_for_targets == []:
        logger.change_current_status(
            f"Error in new_target_finder_main(). {profiles_to_scrape_for_targets} is empty"
        )

    # parse the profiles_to_scrape_for_targets arg so its usable
    if len(profiles_to_scrape_for_targets[0]) > 1:
        pass
    else:
        profiles_to_scrape_for_targets = parse_profiles_to_scrape_arg(
            profiles_to_scrape_for_targets
        )

    # randomize order of profiles to scrape for targets
    profiles_to_scrape_for_targets = randomize_string_list(
        profiles_to_scrape_for_targets
    )
    targets_found = 0

    while 1:
        for scrape_target_index in range(len(profiles_to_scrape_for_targets)):
            # get a scrape target
            this_scrape_target = profiles_to_scrape_for_targets[scrape_target_index]

            print(f"Scraping {this_scrape_target}'s follower list for targets...")

            # get a list of followers from the scrape target
            this_follower_list = get_followers_list(
                logger=logger, size=50, screen_name=this_scrape_target, timeout=30
            )

            # for each follower, check if they are a good target
            follower_index=0
            for follower in this_follower_list:
                follower_index+=1

                #every 10 examined potential targets, update the logger values for following and followers
                update_logger_stats(logger)

                # check if enough targets in target_list.txt
                targets_in_target_file = count_targets_in_target_list_file()
                if int(targets_in_target_file) >= int(targets_to_find):
                    logger.change_current_status(
                        f"{targets_in_target_file} targets in target_list.txt... stopping target search..."
                    )
                    return "following"

                is_good_profile = check_if_user_is_good_target(logger, follower)

                if is_good_profile is True:
                    print(f"{follower} is a good target")

                    # increment targets found
                    targets_found += 1

                    # add this target to target_list
                    add_line_to_target_list_file(follower)
                    add_line_to_target_history_file(follower)
                    logger.update_targets_left(count_targets_in_target_list_file())

                    # if we have found enough targets, stop
                    if int(targets_found) >= int(targets_to_find):
                        print(
                            f"Found {targets_found} targets. Stopping target search..."
                        )
                        return "following"

                else:
                    logger.change_current_status(
                        f"{follower} is not a good target for reason: {is_good_profile}"
                    )
    return None


# method to get a list of my followers of a given size
def get_followers_list(logger, size, screen_name, timeout):
    follower_list = []
    try:
        follower_results_list = api.get_followers(screen_name=screen_name, count=size)
        for follower_result in follower_results_list:
            this_name = follower_result.screen_name
            follower_list.append(this_name)
        return follower_list
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error getting followers list for [{screen_name}]...\nWaiting {timeout} sec then retrying..."
        )
        logger.change_current_status(e)
        time.sleep(timeout)
        return get_followers_list(logger, size, screen_name, timeout=int(timeout * 1.3))


# method to get a tweet count given a screen name
def get_tweet_count(logger, profile_name, timeout):
    try:
        follower_count = api.get_user(screen_name=profile_name).statuses_count
        return follower_count
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error getting tweet count...\nWaiting {timeout} sec then retrying..."
        )
        print(f"Error getting profile name {e}")
        time.sleep(timeout)
        return get_tweet_count(logger, profile_name, timeout=int(timeout * 1.3))


# method to get the follower count of a given profile name
def get_follower_count(logger, profile_name, timeout):
    try:
        follower_count = api.get_user(screen_name=profile_name).followers_count
        return follower_count
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error getting follower count...\nWaiting {timeout} sec then retrying..."
        )
        print(f"Error getting follower count {e}")
        time.sleep(timeout)
        return get_follower_count(logger, profile_name, timeout=int(timeout * 1.3))


# method to check if a given user is private
def check_if_private(logger, profile_name, timeout):
    try:
        is_private = api.get_user(screen_name=profile_name).protected
        return is_private
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error checking if private...\nWaiting {timeout} sec then retrying..."
        )
        print(f"Error checking if private {e}")
        time.sleep(timeout)
        return check_if_private(logger, profile_name, timeout=int(timeout * 1.3))


# method to get the following count of a given profile name
def get_following_count(logger, profile_name, timeout):
    try:
        following_count = api.get_user(screen_name=profile_name).friends_count
        return following_count
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error getting following count...\nWaiting {timeout} sec then retrying..."
        )
        print(f"Error getting following count: {e}")
        time.sleep(timeout)
        return get_following_count(logger, profile_name, timeout=int(timeout * 1.3))


# method to check if any blacklisted term appears in a given description text
def check_description_for_blacklist(description_text):
    blacklist = [
        "NBA",
        "never broke",
        "baseball ",
        "http://discord.gg",
        "evolution",
        "genomics",
        "Wrestling",
        "wrestling",
        "Buffalo",
        "bills",
        "Bills",
        "Guitarist",
        "Singer",
        "browns",
        "yanks",
        "yankees",
        "Browns",
        "Brown",
        "ig:",
        "IG:",
        "#GothBoiClique",
        "sigma",
        "CEO",
        "music",
        "clothing",
        "lifestyle",
        "LIFESTYLE",
        "Lifestyle",
        "guns",
        "brown",
        "YANKEES",
        "Yankees",
        "postdoc",
        "Husband",
        "father",
        "sea",
        "seahawks",
        "BASEBALL",
        "twitch",
        "fotógrafo",
        "SOCCER",
        "soccer",
        "Soccer",
        "futbol",
        "Official",
        "official",
        "OFFICIAL",
        "Baseball",
        "baseball",
        "Never broke",
        "Never Broke",
        "twitch",
        "Twitch",
        "TWITCH",
        "notis",
        "NOTIS",
        "Notis",
        ".com",
        "earnings",
        "Earnings",
        "Noti",
        "noti",
        "NOTI",
        "nba",
        "NFL",
        "nfl",
        "football",
        "FOOTBALL",
        "dubnation",
        "Dubnation",
        "DubNation",
        "DUBNATION",
        "fttb",
        "FTTB",
        "titans",
        "onlyfans",
        "raysup",
        "Raysup",
        "RaysUp",
        "NjDevils",
        "NJDevils",
        "njdevils",
        "NJDEVILS",
        "Titans",
        "TITANS",
        "follow back",
        "following back",
        "FOLLOW BACK",
        "follow for follow",
        "f4f",
        "Follow for follow",
        "FOLLOW FOR FOLLOW",
        "I FOLLOW BACK",
        "follow back",
        "ONLYFANS",
        "Onlyfans",
        "top 0",
        "top 1",
        "top 2",
        "top 3",
        "top 4",
        "edtwt",
        "49ers",
        "eating disorder",
        "fatphobes",
        "fee",
        "writer",
        "booktwt",
        "book twitter",
        "booktwitter",
        "reading",
        "thinspo",
        "poly",
        "soundcloud",
        "18+",
        "minors",
        "republican",
        "democrat",
        "anti",
        "crypto",
        "tesla",
        "NFT",
        "TOP5",
        "TOP4",
        "TOP3",
        "TOP2",
        "TOP1",
        "TOP6",
        "TOP7",
        "TOP8",
        "TOP9",
        "investing",
        "invest",
        "INVEST",
        "Invest",
        "Author",
        "Aritist",
        "Founder",
        "founder",
        "artist",
        "website",
        "link",
        "analyst",
        "Analyst",
        "Trump",
        "trump",
        "biden",
        "Biden",
        "america",
        "USA",
        "usa",
        "american",
        "jesus",
        "Jesus",
        "freedom",
        "Freedom",
        "USMC",
        "USAF",
        "usmc",
        "usaf",
        "family",
        "BLM",
        "amosc",
        "historian",
        "Historian",
        "HISTORIAN",
        "podcast",
        "Podcast",
        "PODCAST",
    ]
    for term in blacklist:
        if term in description_text:
            return term
    return "pass"


# given a follower, check various metrics to see if follower is a good target
def check_if_user_is_good_target(logger, follower):
    follower_count = get_follower_count(logger, follower, timeout=30)
    following_count = get_following_count(logger, follower, timeout=30)
    description = get_description(logger, follower, timeout=30)
    tweet_count = get_tweet_count(logger, follower, timeout=30)

    # if the user already exists in target_history_list.txt, then skip
    if check_if_target_in_target_history_file(follower):
        return "Already in target history list"

    follower_count_lower_limit = 50
    if follower_count < follower_count_lower_limit:
        return f"Follower count is {follower_count} (lower limit is {follower_count_lower_limit})"

    following_count_lower_limit = 50
    if following_count < following_count_lower_limit:
        return f"Following count is {following_count} (lower limit is {following_count_lower_limit})"

    ratio = following_count / follower_count

    tweet_count_lower_limit = 15
    if tweet_count < tweet_count_lower_limit:
        return f"Tweet count is {tweet_count}... (lower limit is {tweet_count_lower_limit})"

    if check_if_private(logger, follower, timeout=30):
        return "Private"

    if ratio > 0.99:
        return f"Ratio of {(str(ratio)[0:4])}"

    if follower_count > 1000:
        return "Too many followers"

    description_return = check_description_for_blacklist(description)
    if description_return != "pass":
        return f"[{description_return}] found in description"

    return True


# method to get a given screen name's profile description
def get_description(logger, screen_name, timeout):
    try:
        return (api.get_user(screen_name=screen_name)).description
    except Exception as e:
        if timeout > 3800:
            timeout = 3800

        logger.change_current_status(
            f"Error getting profile's description...\nWaiting {timeout} sec then retrying..."
        )
        logger.change_current_status(f"Error message: {e}")
        time.sleep(timeout)
        return get_description(logger, screen_name, timeout=int(timeout * 1.3))


# method to randomize the order of a list of strings
def randomize_string_list(string_list):
    index = 0

    new_string_list = []
    while len(new_string_list) != len(string_list):
        this_random_string = string_list[random.randint(0, len(string_list) - 1)]
        if this_random_string not in new_string_list:
            new_string_list.append(this_random_string)

    return new_string_list


# method to parse the profiles_to_scrape_for_targets argument from the gui to a usable format
def parse_profiles_to_scrape_arg(arg):
    profiles_top_scrape_string_list = []
    current_string = ""
    for char in arg:
        if char != ",":
            current_string += char
        else:
            profiles_top_scrape_string_list.append(current_string)
            current_string = ""
    if current_string != "":
        profiles_top_scrape_string_list.append(current_string)

    return profiles_top_scrape_string_list




#method to update the stats in the logger for following and unfollowing
def update_logger_stats(logger):
    my_screen_name=api.get_user(user_id=creds[0]).screen_name

    #get values
    follower_count = get_follower_count(logger, profile_name=my_screen_name, timeout=30)
    following_count = get_following_count(logger, profile_name=my_screen_name, timeout=30)

    #update values in logger obj
    logger.update_current_followers_stat(follower_count)
    logger.update_current_following_stat(following_count)
    
    
