from utils.logger import Logger
import PySimpleGUI as sg

import random
import time
from firefox.firefox_driver import (
    find_element_by_xpath,
    get_to_webpage,
    scroll_down_to_load_more,
)
from data.file_handler import (
    add_to_blacklist_file,
    get_creds,
    add_to_greylist_file,
    count_greylist_profiles,
    count_whitelist_profiles,
    get_name_from_greylist_file,
    add_to_whitelist_file,
    check_if_line_exists_in_whitelist,
    check_if_line_exists_in_blacklist,
    get_name_from_whitelist_file,
    count_blacklist_profiles,
    add_line_to_data_file,
)
from firefox.firefox_driver import check_for_timeout_webpage


BOT_USER_FOLLOWING_LIMIT = 3000
GREYLIST_LOWER_LIMIT = 100
WHITELIST_LOWER_LIMIT = 30
FOLLOW_TIMEOUT_TIME = 300  # s


# Set the option to suppress error popups
sg.set_options(suppress_error_popups=True)
SCRAPE_TARGET_URLS = [
    "https://twitter.com/whatsaplat/followers",
    "https://twitter.com/RUNYOMONEY/followers",
    "https://twitter.com/jupitersembrace/followers",
    "https://twitter.com/steventaughtme/followers",
    "https://twitter.com/di3tcoladrinker/followers",
    "https://twitter.com/thejadamoae/followers",
    "https://twitter.com/OnikaPoppin/followers",
    "https://twitter.com/bklynb4by/followers",
    "https://twitter.com/ayeejuju/followers",
    "https://twitter.com/PicturesFoIder/followers",
    "https://twitter.com/kirawontmiss/followers",
    "https://twitter.com/W_B_Rick/followers",
    "https://twitter.com/bcbender/followers",
    "https://twitter.com/maonu10/followers",
    "https://twitter.com/cumcurse/followers",
    "https://twitter.com/toxictxts/followers",
    "https://twitter.com/c4ra_/followers",
    "https://twitter.com/fasc1nate/followers",
    "https://twitter.com/ThebestFigen/followers",
    "https://twitter.com/xigotsoul/followers",
    "https://twitter.com/theashleyray/followers",
    "https://twitter.com/TvkeOfff/followers",
    "https://twitter.com/historyinmemes/followers",
    "https://twitter.com/beyoncegarden/followers",
    "https://twitter.com/FearedBuck/followers",
    "https://twitter.com/haworthes/followers",
    "https://twitter.com/FadeHubb/followers",
    "https://twitter.com/kirawontmiss/followers",
    "https://twitter.com/JackWilliamRtF/followers",
    "https://twitter.com/LILBTHEBASEDGOD/followers",
    "https://twitter.com/PookiesParadise/followers",
    "https://twitter.com/puddlecow/followers",
    "https://twitter.com/itgirlposts/followers",
    "https://twitter.com/anymnesis/followers",
    "https://twitter.com/BestHoodComedy/followers",
    "https://twitter.com/HoodComedyEnt/followers",
    "https://twitter.com/HOODC0MEDY/followers",
    "https://twitter.com/daaamncomedy/followers",
    "https://twitter.com/Ipsofacto123/followers",
    "https://twitter.com/Rap/followers",
    "https://twitter.com/BTS_twt/followers",
    "https://twitter.com/bts_bighit/followers",
    "https://twitter.com/MattyBRaps/followers",
    "https://twitter.com/ERBofHistory/followers",
    "https://twitter.com/RapMais/followers",
    "https://twitter.com/MIAuniverse/followers",
    "https://twitter.com/Drake/followers",
    "https://twitter.com/thegame/followers",
    "https://twitter.com/chancetherapper/followers",
    "https://twitter.com/psy_oppa/followers",
    "https://twitter.com/sarkodie/followers",
    "https://twitter.com/Wale/followers",
    "https://twitter.com/taylorswift13/followers",
    "https://twitter.com/BustaRhymes/followers",
    "https://twitter.com/SnoopDogg/followers",
    "https://twitter.com/BrunoMars/followers",
    "https://twitter.com/selenagomez/followers",
    "https://twitter.com/katyperry/followers",
    "https://twitter.com/kanyewest/followers",
    "https://twitter.com/VectorThaViper/followers",
]
SCRAPE_TARGET_USERNAMES = [
    "lameyzzz_",
    "TySpiritual",
    "SlimeAnime",
    "AnimeExpo",
    "Dj_AniMe",
    "animecentral",
    "_ANIMEse",
    "animeunitedBR",
    "LoKoKaBoosTeR69",
    "TheSliceofAnime",
    "HuinGuillaume",
    "GelicaJayy",
    "Chiitan_Osaka",
    "Sacb0y",
]
for n in SCRAPE_TARGET_USERNAMES:
    SCRAPE_TARGET_URLS.append(f"https://twitter.com/{n}/followers")


def check_for_failed_login(driver):
    xpaths = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/a/div",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]/span",
    ]

    for xpath in xpaths:
        try:
            element = find_element_by_xpath(driver, xpath)
            text = element.text

            if (
                "Sign up" in text
                or "Log in" in text
                or "People on X are the first to know." in text
                or "Don’t miss what’s happening" in text
            ):
                return True

        except:
            pass

    return False


def login_to_twitter(driver, logger) -> bool:
    start_time = time.time()

    user, password = get_creds()

    logger.change_status("Logging in to twitter...")

    # get to twitter
    get_to_webpage(driver, "https://twitter.com")

    # click login button
    if click_sign_in_button(driver) is True:
        # logger.change_status('CLicked "Sign in" button')
        time.sleep(0.5)
    else:
        logger.change_status("Failed to click login button Returning False")
        return False

    # type username
    if type_username_into_input(driver, user):
        # logger.change_status("Typed username")
        pass
    else:
        logger.change_status("Failed to type username Returning False")
        return False

    # click next
    if click_next_after_username_input(driver):
        # logger.change_status("Clicked next")
        time.sleep(0.5)
    else:
        logger.change_status("Failed to click next Returning False")
        return False

    # type password
    if type_password_into_input(driver, password):
        # logger.change_status("Typed password")
        time.sleep(0.5)
    else:
        logger.change_status("Failed to type password Returning False")
        return False

    # click login button
    if click_log_in_after_password_input(driver):
        # logger.change_status("Clicked login button")
        pass
    else:
        logger.change_status("Failed to click login button Returning False")
        return False
    time.sleep(2)

    # get back to twitter.com
    get_to_webpage(driver, "https://twitter.com")
    time.sleep(3)

    if check_for_failed_login(driver):
        logger.change_status("Failed to login")
        return False
    else:
        logger.change_status("Good login!")
        time.sleep(0.33)

    time_taken = str(time.time() - start_time)[:5]
    logger.change_status(f"Logged in to twitter in {time_taken}s")

    return True


def click_log_in_after_password_input(driver):
    xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.click()
            return True
        except:
            continue

    return False


def type_password_into_input(driver, password):
    xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.send_keys(password)
            return True
        except:
            continue

    return False


def click_next_after_username_input(driver):
    xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.click()
            return True
        except:
            continue

    return False


def type_username_into_input(driver, username):
    xpath = "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.send_keys(username)
            return True
        except:
            continue

    return False


def click_sign_in_button(driver):
    xpaths = [
        "/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a/div",
        "",
        "",
        "",
    ]

    timeout = 30  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        for xpath in xpaths:
            try:
                element = find_element_by_xpath(driver, xpath)
                element.click()
                return True
            except:
                continue

    return False


def click_followers_button_on_profile(driver):
    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[2]/span"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.click()
            return True
        except:
            continue

    return False


def wait_for_followers_page(driver):
    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            return True
        except:
            continue

    return False


def scrape_follower_usernames_from_followers_list_page(driver, logger):
    scroll_down_to_load_more(driver, scroll_pause_time=0.1, num_scrolls=1)
    time.sleep((random.randint(1, 3) / 3))

    these_names = read_follower_name_elements_on_this_page(driver)
    logger.change_status(f"Found {len(these_names)} names")

    return these_names


def read_follower_name_elements_on_this_page(driver):
    names = []
    for index in range(200):
        try:
            path = f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{index}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span"
            element = find_element_by_xpath(driver, path)
            text = element.text
            text = str(text)
            text = text.replace("@", "")
            names.append(text)
        except:
            pass

    return names


def remove_dupes_from_list(string_list):
    new_list = []

    for string in string_list:
        if string not in new_list or len(new_list) == 0:
            new_list.append(string)

    return new_list


def scrape_users_from_profile(driver, logger, scrape_target_profile_url, scrape_count):
    logger.change_status("Initiating scraping followers from profile")
    names = []

    for _ in range(scrape_count):
        if get_to_webpage(driver, scrape_target_profile_url) is False:
            print("Found a timeout #351")
            return "timeout"

        # click follwoers button on followers page
        if wait_for_followers_page(driver):
            pass
        else:
            logger.change_status("Failed to load follwers page")
            continue
        time.sleep(1)

        # scrape names for a duration
        these_names = scrape_follower_usernames_from_followers_list_page(driver, logger)

        for n in these_names:
            names.append(n)

    names = remove_dupes_from_list(names)

    return names


def scrape_for_profiles(driver, logger):
    while count_greylist_profiles() < 1000:
        logger.change_status(
            f"There are {(count_greylist_profiles())} accounts in greylist file. Scraping more..."
        )
        update_data_list_logger_values(logger)
        url = random.choice(SCRAPE_TARGET_URLS)
        these_names = scrape_users_from_profile(driver, logger, url, 2)
        if these_names == "timeout":
            print("Found a timeout #1265")
            return "timeout"

        for n in these_names:
            add_to_greylist_file(n)

    logger.change_status(
        f"There are {(count_greylist_profiles())} accounts in greylist file. Stopping"
    )
    update_data_list_logger_values(logger)


def parse_follower_count(value):
    if value is False:
        return False

    value = str(value)
    value = value.replace(" ", "")
    value = value.replace(",", "")

    if "K" in value or "k" in value:
        value = value.replace("K", "")
        value = value.replace("k", "")
        value = float(value) * 1000
        return int(value)

    if "M" in value or "m" in value:
        value = value.replace("M", "")
        value = value.replace("m", "")
        value = float(value) * 1000000
        return int(value)

    return int(value)


def vet_profile(driver, logger, profile_username):
    url = f"https://twitter.com/{profile_username}"

    # if name in good list, return BAD
    if check_if_line_exists_in_whitelist(profile_username):
        logger.change_status("Already in whitelist")
        return "Already in whitelist"

    # if name already in bad list, return BAD
    if check_if_line_exists_in_blacklist(profile_username):
        logger.change_status("Already in blacklist")
        return "Already in blacklist"

    # go to the profile
    if not get_to_webpage(driver, url):
        return "timeout"
    time.sleep(2)

    # if private account, skip it
    if check_for_private_account(driver):
        logger.change_status("Private account")
        return "Private account"

    if check_for_timeout_webpage(driver):
        logger.change_status("Timeout page")
        return "timeout"

    # read following count
    following_count = parse_follower_count(read_following_count(driver))
    if following_count is False:
        return "Fail Read following_count"

    # read follower count
    follower_count = parse_follower_count(read_follower_count(driver))
    if follower_count is False:
        return "Fail Read follower_count"

    # if following less than 10 people, return False
    FOLLOWING_COUNT_LOWER_LIMIT = 10
    if int(following_count) < FOLLOWING_COUNT_LOWER_LIMIT:
        return f"Follow count <{FOLLOWING_COUNT_LOWER_LIMIT}"

    # if ratio is bad, return bad
    ratio = following_count / follower_count
    if ratio > 1.5:
        logger.change_status("Bad ratio")
        return f"Bad ratio: {str(ratio)[:4]}"

    # if following count is greater than 1k, return FALSE
    FOLLOWING_COUNT_LIMIT = 1000
    if int(following_count) > FOLLOWING_COUNT_LIMIT:
        return f"Follow count >{FOLLOWING_COUNT_LIMIT}"

    # if follower count is greater than 3k, return False
    FOLLOWER_COUNT_LIMIT = 5000
    if int(follower_count) > FOLLOWER_COUNT_LIMIT:
        return f"Follower count >{FOLLOWER_COUNT_LIMIT}"

    # if follower count is less than 100, return False
    FOLLOWER_COUNT_LOWER_LIMIT = 50
    if int(follower_count) < FOLLOWER_COUNT_LOWER_LIMIT:
        return f"Follower count <{FOLLOWER_COUNT_LOWER_LIMIT}"

    return True


def read_follower_count(driver):
    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span"
    xpath2 = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/a/span[1]/span"

    timeout = 5  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            return element.text
        except:
            pass
        try:
            element = find_element_by_xpath(driver, xpath2)
            return element.text
        except:
            pass

    return False


def read_following_count(driver):
    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span"
    xpath2 = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[1]/a/span[1]/span"

    timeout = 5  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            return element.text
        except:
            pass
        try:
            element = find_element_by_xpath(driver, xpath2)
            return element.text
        except:
            pass

    return False


def check_for_private_account(driver):
    xpath = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[2]/div/div[1]/span"

    timeout = 3  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            text = element.text
            if "hese posts are protected" in text:
                return True
        except:
            continue

    return False


def vet_a_profile(driver, logger):
    if count_greylist_profiles() < 1:
        logger.change_status("Greylist is too low, scraping for more profiles...")
        if scrape_for_profiles(driver, logger) == "timeout":
            print("Found a timeout white scraping for profiles for greylist")
            return "timeout"

    # get a random name from greylist
    name = get_name_from_greylist_file()

    logger.change_status(f"Vetting [{name}]...")

    vet_start_time = time.time()

    # vet the profile
    profile_check = vet_profile(driver, logger, name)

    vet_time_taken = str(time.time() - vet_start_time)[:5]

    logger.change_status(f'Took {vet_time_taken} to vet profile "{name}"')

    # if timeout occured during check, retunr 'timeout'
    if profile_check == "timeout" or check_for_timeout_webpage(driver):
        logger.change_status("Timeout page #2456")
        return "timeout"

    # if profile check vetted the profile as bad, add name to blacklist, return True
    if profile_check is not True:
        logger.change_status(f"Username [{name}] failed for reason: {profile_check}")
        add_to_blacklist_file(name)
        return False

    logger.change_status("Good profile!")
    add_to_whitelist_file(name)
    return True


def vet_profiles(driver, logger, whitelist_count):
    logger.change_status(f"Whitelist count is {count_whitelist_profiles()}")

    count = 0

    while count_whitelist_profiles() < whitelist_count:
        logger.change_status("Vetting a profile...")
        update_data_list_logger_values(logger)

        if vet_a_profile(driver, logger) == "timeout":
            logger.change_status("Foudn a timeout while vetting a profile")
            return "timeout"

    logger.change_status(
        f"There are {(count_whitelist_profiles())} accounts in whitelist file. Stopping"
    )

    update_data_list_logger_values(logger)

    return count


def click_follow_button_on_this_profile(driver):
    x_paths = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/span/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div/div[1]/div[2]/div[3]/div[1]/div/div/span/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/span/span",
        "",
        "",
        "",
    ]

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        for xpath in x_paths:
            try:
                element = find_element_by_xpath(driver, xpath)
                text = element.text
                text = str(text)
                if "Following" in text:
                    return False

                if "Follow" in text:
                    element.click()
                    return True
            except:
                pass

    return False


def follow_a_profile(driver, logger):
    start_time = time.time()

    logger.change_status("Following a random profile")

    if count_whitelist_profiles() < 2:
        logger.change_status("Whitelist is empty, vetting profiles")
        while vet_a_profile(driver, logger) is not True:
            print('Vetting profiles until it gets 1 so bot can continue to follow...')

    profile_username = get_name_from_whitelist_file()
    logger.change_status(f"Following a [{profile_username}]")

    logger.change_status(f"Following {profile_username}")

    # get to profile
    url = f"https://twitter.com/{profile_username}"
    if not get_to_webpage(driver, url):
        logger.change_status("Timeout page")
        return "timeout"

    # click follow button
    if click_follow_button_on_this_profile(driver) is True:
        time_taken = str(time.time() - start_time)[:5]
        logger.change_status(f"Followed a profile in {time_taken}")
        logger.add_follow()
        logger.set_time_of_last_follow()
        return True

    logger.change_status(f"Failed to follow {profile_username}")
    input("Enter to continue")
    return False


def find_unfollow_elements(driver):
    elements = []
    for index in range(200):
        xpath = f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{index}]/div/div/div/div/div[2]/div[1]/div[2]/div/div/span/span"
        try:
            element = find_element_by_xpath(driver, xpath)
            text = element.text
            if "Following" in text:
                elements.append(element)
        except:
            pass

    return elements


def click_confirm_unfollow_button(driver):
    xpath = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div"

    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            element = find_element_by_xpath(driver, xpath)
            element.click()
            return True
        except:
            continue

    return False


def click_unfollow_elements(driver, logger, count):
    elements = find_unfollow_elements(driver)
    unfollows = 0

    # cut elements to a random {count}
    if count < len(elements):
        elements = random.sample(elements, count)

    for element in elements:
        element.click()
        if click_confirm_unfollow_button(driver) is False:
            continue
        unfollows += 1
        logger.add_unfollow()

    logger.change_status(f"Unfollowed {unfollows} users")
    return unfollows


def wait_for_following_page(driver):
    timeout = 10  # s
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(find_unfollow_elements(driver)) > 0:
            return True

    return False


def unfollow_users(driver, logger, users_to_unfollow):
    username = get_creds()[0]

    users_left_to_unfollow = users_to_unfollow

    while users_left_to_unfollow > 0:
        # get to profile
        url = f"https://twitter.com/{username}/following"
        if get_to_webpage(driver, url) is False:
            return "timeout"
        time.sleep(1)

        # wait for unfollow buttons to apppear
        if wait_for_following_page(driver) is False:
            logger.change_status("Failed waiting for following page")
            return False

        # click unfollow buttons
        unfollows = click_unfollow_elements(driver, logger, users_left_to_unfollow)

        logger.change_status(f"Just unfollowed {unfollows} users")

        users_left_to_unfollow -= unfollows

        logger.change_status(f"New users left to unfollow: {users_left_to_unfollow}")

    return True


def count_bot_user_following_stats(driver):
    username = get_creds()[0]
    url = f"https://twitter.com/{username}"

    get_to_webpage(driver, url)

    following_count = parse_follower_count(read_following_count(driver))
    follower_count = parse_follower_count(read_follower_count(driver))

    return following_count, follower_count


def update_data_list_logger_values(logger):
    logger.set_greylist_count(count_greylist_profiles())
    logger.set_whitelist_count(count_whitelist_profiles())
    logger.set_blacklist_count(count_blacklist_profiles())


def update_bot_user_following_stats(logger, following, followers):
    logger.set_bot_user_follower_value(followers)
    logger.set_bot_user_following_value(following)
    add_line_to_data_file(followers, following)


def main_loop(driver, logger):
    # update whitelist, blacklist values
    print("Updating logger's whitelist/blacklist values")
    update_data_list_logger_values(logger)

    # update following, followers values for bot user
    print("Updating logger's followers/following values")
    following, followers = count_bot_user_following_stats(driver)
    update_bot_user_following_stats(logger, following, followers)

    # if following is too high, unfollow users till at 1/3 of limit
    if following > BOT_USER_FOLLOWING_LIMIT:
        if (
            unfollow_users(driver, logger, int(0.3333 * BOT_USER_FOLLOWING_LIMIT))
            == "timeout"
        ):
            # if timeout occures while unfollowing users, return False
            return False

        # if unfollowed users without timeout, return True
        return True
    print("User following count is below the limit... continuing")

    # if its been long enough, follow a profile
    if logger.check_if_can_follow():
        if follow_a_profile(driver, logger) == "timeout":
            logger.change_status("Experienced a timeout while following a profile")
            return False

        # if followed a user correctly, return True
        return True
    print("Hasn't been long enough to follow a profile... continuing")

    # otherwise just vet a profile
    if vet_a_profile(driver, logger) == "timeout":
        logger.change_status("Experienced a timeout while vetting a profile")
        return False

    print("Vetted a profile in the meantime...")
    # if completed all checks and tasks without timeout, return True
    return True
