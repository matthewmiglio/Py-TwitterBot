import random
import re
import time

from targetting.target_file import (
    add_line_to_target_history_file,
    add_line_to_target_list_file,
    check_if_target_in_target_history_file,
    count_targets_in_target_list_file,
)
from utils.client_interaction import (
    click_follower_button_of_profile_page,
    click_program_user_profile_button,
    get_description_text_of_this_user,
    get_follower_value_of_this_profile,
    get_following_value_of_this_profile,
    get_names_of_followers_on_follower_list_page,
    get_privacy_of_this_profile,
    get_to_user_profile_link,
    scroll_to_bottom,
)
from utils.data import add_line_to_data_file


"""
targetting.py -> every function related to the targetting state of the program
"""


# method to find suitable targets to follow from
def targetting_main(driver, logger, scrape_list, username, targets_to_find=3):
    """main method for targetting mode

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (utils.logger.Logger): the logger object
        scrape_list (list): the list of users to scrape
        username (string): the username of the program user
        targets_to_find (int, optional): the number of targets to find per cycle. Defaults to 3. Developer tool.

    Returns:
        string: the next state of the program

    """

    scrape_list = parse_scrape_target_argument(scrape_list)

    if count_targets_in_target_list_file() >= targets_to_find:
        logger.log(
            message="Have enough targets, moving to following state.",
            state="Targetting",
        )
        return "following"

    suitable_target_list = []


    while 1:
        # random.shuffle(scrape_list)
        for scrape_target in scrape_list:
            logger.log(
                message=f"Searching through [{scrape_target}]'s follower list for suitable targets.",
                state="Targetting",
            )

            # get a list of this user's followers
            this_follower_list = get_followers_of_user(driver, logger, scrape_target)

            # check each user for suitability
            logger.log(
                message=f"Checking a list of {len(this_follower_list)} users for potential targets.",
                state="Targetting",
            )
            for user in this_follower_list:
                this_user_check_start_time = time.time()
                get_to_user_profile_link(driver, logger, user)

                # check this user's stuff for suitability
                suitability_check = check_if_user_is_suitable_target(
                    driver, logger, user
                )

                if suitability_check == True:
                    logger.log(
                        message=f"Scraping {scrape_target} ||Verified {user} is a suitable target in {str(time.time()-this_user_check_start_time)[:4]} seconds.",
                        state="Targetting",
                    )
                    # add user to return list
                    suitable_target_list.append(user)
                    # add user to target_list.txt
                    add_line_to_target_list_file(user)
                    # add user to target_list_history.txt
                    add_line_to_target_history_file(user)
                    # increment logger's target's added count
                    logger.add_new_target_found()
                    # if we have enough targets, pass to following state
                    if len(suitable_target_list) == targets_to_find:
                        logger.log(
                            message="Have enough targets, moving to following state.",
                            state="Following",
                        )
                        return "following"
                else:
                    logger.log(
                        message=f"Scraping {scrape_target} ||Verified {user} is not a suitable target in {str(time.time()-this_user_check_start_time)[:4]} seconds for reason: {suitability_check}",
                        state="Targetting",
                    )


# method to parse the scrape target argument from the frontend GUI
def parse_scrape_target_argument(line):
    """

    Args:
        line

    Returns:
        string[]: the list of users who's follower lists will be scraped

    """
    target_list = []
    this_name = ""
    for char in line:
        if char == " ":
            continue
        if char == ",":
            target_list.append(this_name)
            this_name = ""
            continue
        this_name += char
    return target_list


# method to check for any blacklist text in a user's description text
def check_description_text_for_blacklist(user_description):
    """method to check for any blacklist text in a user's description text

    Args:
        user_description (string): the description text of the user to check

    Returns:
        bool: whether or not the user is suitable for targetting

    """

    if user_description == "" or user_description is None:
        return False

    blacklist = [
        "NBA",
        "never broke",
        "baseball ",
        "http://discord.gg",
        "evolution",
        "genomics",
        "Wrestling",
        "Contributions",
        "wrestling",
        "Buffalo",
        "bills",
        "UGA",
        "Atlanta",
        "Sports",
        "Tigers",
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
        "University",
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
        "insta",
        "instagram",
        "fttb",
        "fanpage",
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
        "journalist",
        "journalism",
        "soundclooud",
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

    for bad_string in blacklist:
        if re.search(bad_string, user_description, re.IGNORECASE):
            return bad_string
        else:
            pass
    return False


# method to check if a user is a suitable target for following followers of
def check_if_user_is_suitable_target(driver, logger, user):
    """method to check if a user is a suitable target for following followers of

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logger): the logger to use
        user (string): the profile username to check

    Returns:
        None

    """

    description_text = get_description_text_of_this_user(driver)
    following_value = get_following_value_of_this_profile(driver)
    follower_value = get_follower_value_of_this_profile(driver)

    # if failed to read any of the values, just return and go to the next profile
    if (
        following_value == "fail"
        or follower_value == "fail"
        or following_value is None
        or follower_value is None
    ):
        return "Failed reading"

    # if this user exists in the target_history.txt file in appdata/Py-TwitterBot then return false
    if check_if_target_in_target_history_file(user):
        return "Target history"

    # user must follow more than 50 people
    user_following_lower_limit = 50

    if int(following_value) < int(user_following_lower_limit):
        return f"Following<{user_following_lower_limit}"

    # user must have more than 50 followers
    user_followers_lower_limit = 50
    if follower_value < user_followers_lower_limit:
        return f"50<followers"

    # user must not have more than 1000 followers
    user_followers_upper_limit = 1000
    if follower_value > user_followers_upper_limit:
        return f"1000<followers"

    # user must have more than 15 tweets

    # user must NOT be private
    if get_privacy_of_this_profile(driver):
        return "Private"

    # user's follow ratio must be above 1 (following/followers)
    ratio = following_value / follower_value

    if ratio > 1.5:
        return f"Ratio of {str(ratio)[:4]}"

    # user's description must NOT contain any of the blaclisted words
    text_check = check_description_text_for_blacklist(description_text)
    if text_check != False:
        return f"Description blacklist: {text_check}"

    return True


# method to get a list of followers of a given user
def get_followers_of_user(driver, logger, user):
    """method to get a list of followers of a given user

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logger): the logger to use
        user (string): the profile username to check

    Returns:
        string[]: a list of usernames of the followers of the given user

    """
    # get to user profile

    logger.log(
        message=f"Getting to {user}'s profile to get their follower list",
        state="Targetting",
    )
    get_to_user_profile_link(driver, logger, user)

    # click followers button
    click_follower_button_of_profile_page(driver, logger)
    time.sleep(3)

    # scroll down to load follower elements
    for _ in range(8):
        logger.log(message="Loading more followers...", state="Targetting")
        scroll_to_bottom(driver, logger)
        time.sleep(2)

    name_list = get_names_of_followers_on_follower_list_page(driver, logger)
    return remove_duplicates_from_list(name_list)


# method to remove dupe strings from a list of string
def remove_duplicates_from_list(name_list):
    """method to remove dupe strings from a list of string

    Args:
        name_list (string[]): the list of strings to remove duplicates from

    Returns:
        string[]: new string list without dupes

    """
    new_list = []
    for name in name_list:
        if not name in new_list:
            new_list.append(name)
    return new_list



# method to add a line of data to the data file
def update_data_file(logger, follower_value, following_value):
    """method to add a line of data to the data file

    Args:
        logger (logger): the logger to use
        follower_value (int): the current follower value of the program user
        following_value (int): the current following value of the program user

    Returns:
        None

    """
    line = str(follower_value) + "|" + str(get_date_time()) + "|" + str(following_value)
    add_line_to_data_file(line)
    logger.log(message="Updated data file...", state="following")


# method to get the current date and time in a readable format
def get_date_time():
    """method to get the current date and time in a readable format

    Args:
        None

    Returns:
        string: the current date and time in a readable format

    """
    return time.strftime("%m/%d/%Y|%H:%M:%S", time.localtime())
