from selenium.webdriver.common.by import By
import time


"""
client_interaction.py -> every function related to interaction with the chrome driver client (reading values or clicking elements)
"""


# method to check for the 'signup or login' popup after getting to a new profile page
def check_for_signup_popup_after_getting_to_profile_page(driver):
    """method to check for the 'signup or login' popup after getting to a new profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        bool: True if the popup is found, False if not

    """

    path_list = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/a/div",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/a",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if (
                "ess entr to cont" in text
                or "n’t miss what’s happe" in text
                or "Log in" in text
            ):
                return True
        except:
            pass
    return False


# method to check for the 'turn on notifications' popup after getting to a new profile page
def check_for_notification_popup_after_getting_to_profile_page(driver):
    """method to check for the 'turn on notifications' popup after getting to a new profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        boolean: True if the popup is found, False if not

    """

    for path in [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]",
    ]:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if (
                "miss out on what’s happening by enabl" in text
                or "urn on notificatio" in text
            ):
                return True
        except:
            pass
    return False


# method to check if the profile is private or not
def get_privacy_of_this_profile(driver):
    """method to check if the profile is private or not

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        boolean: True if the profile is private, False if not

    """
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]/svg/g/path",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]/svg/g/path",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]/svg",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]/svg",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if 'aria-label="Protected account"' in text:
                return True
        except:
            pass
    return False


# method to get a user's description value
def get_description_text_of_this_user(driver):
    """method to get a user's description value

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        string: the description text

    """
    description_text = ""
    for index_a in range(1, 10):
        path_list = [
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/span[{index_a}]",
        ]

        for path in path_list:
            try:
                element = driver.find_element(By.XPATH, path)
                this_text = element.get_attribute("innerHTML")
                if "role=" in this_text or 'class="' in this_text:
                    continue
                description_text += this_text
            except:
                pass
    return description_text


# method to get a user's following value
def get_following_value_of_this_profile(driver):
    """method to get a user's following value

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        int: the following value

    """
    input_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/div/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[4]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/div/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[1]/a/span[1]/span",
    ]
    for input in input_list:
        try:
            element = driver.find_element(By.XPATH, input)
            text = element.get_attribute("innerHTML")
            return parse_follower_value(text)
        except:
            pass


# method to get a user's followers value
def get_follower_value_of_this_profile(driver):
    """method to get a user's followers value

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Returns:
        int: the followers value

    """
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[2]/div/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[2]/div/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[4]/div[2]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/a/span[1]/span",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            return parse_follower_value(text)
        except:
            pass


# method to parse a follower value that may be represented as a string containing characters (like 12.3k)
def parse_follower_value(value):
    """method to parse a follower value that may be represented as a string containing characters

    Args:
        value (string): the number value represented as a string that needs to be parsed

    Returns:
        int: the parsed number value

    """
    num = ""
    for char in value:
        if char == ",":
            continue

        elif char == "k" or char == "K":
            num = float(num) * 1000
            break

        elif char == "m" or char == "M":
            num = float(num) * 1000000
            break

        else:
            num += char

    return int(num)


# method to check for the throttle popup that appears after following a user on their profile page
def check_for_throttle_popup(driver, logger):
    """method to check for the throttle popup that appears after following a user on their profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        boolean: True if the throttle popup is present, False otherwise

    """
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/a/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[1]/span",
    ]

    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if "u are unable to follow more people at th" in text:
                return True
        except:
            pass
    return False


# method to read all the username elements from the list of followers/followings page
def get_names_of_followers_on_follower_list_page(driver, logger):
    """method to read all the username elements from the list of followers/followings page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        string[]: the list of usernames that appear on the screen

    """
    username_list = []
    for index in range(0, 100):
        for path in [
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{index}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span",
        ]:

            try:
                element = driver.find_element(By.XPATH, path)
                text2 = element.get_attribute("innerHTML")
                name = text2[1:]
                if name not in username_list:
                    username_list.append(name)
            except:
                pass
    return username_list


# method to check for the login popup that may popup when getting to a new profile page
def check_for_login_popup_after_following_on_profile_page(driver, logger):
    """method to check for the login popup that may popup when getting to a new profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        boolean: True if the popup is present, False otherwise

    """
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/a[2]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if "gn up so you never miss their T" in text:
                return True
        except:
            pass
    return False


# method to check for the unfollow popup that occues when following a user from their profile page
def check_for_unfollow_popup_after_following_on_profile_page(driver, logger):
    """method to check for the unfollow popup that occues when following a user from their profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        boolean: True if the popup is present, False otherwise

    """
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/span[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/h1/span",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            text = element.get_attribute("innerHTML")
            if "eir Tweets will no longer show up in your" in text:
                return True
        except:
            pass
    return False


# method to click the follow button when on a profile page
def click_follow_button_of_profile_page(driver):
    """method to click the follow button when on a profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        string : "success" if the button was clicked, "fail" otherwise

    """
    for index in range(1, 4):
        path_list = [
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div/span/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]",
        ]
        for path in path_list:
            try:
                element = driver.find_element(By.XPATH, path)
                text = element.get_attribute("innerHTML")
                if "Follow" in text:
                    element.click()
                    return "success"
            except:
                pass
    return "fail"


# method to click the unfollow button when on a profile page
def click_unfollow_button_of_profile_page(driver):
    for index in range(1, 5):
        path_list = [
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[{index}]/div[1]/div/div/span/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[2]/div[{index}]/div[1]/div/div/span/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div/span/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div/span/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div/span",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]/div",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]/div[1]",
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[{index}]",
        ]
        for path in path_list:
            try:
                element = driver.find_element(By.XPATH, path)
                text = element.get_attribute("innerHTML")
                if "Following" in text:
                    element.click()
                    return "success"
            except:
                pass
    return "fail"


# method to click the unfollow in the unfollow confrimation popup that occuers after clicking 'following' button on a user's profile page
def click_unfollow_in_unfollow_confirmation_popup(driver):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            element.click()
            return
        except:
            pass


# method to scroll to the bottom of the page as far as it has loaded
def scroll_to_bottom(driver, logger):
    """method to scroll to the bottom of the page as far as it has loaded

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        None

    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# method to get to the profile of a given username
def get_to_user_profile_link(driver, logger, user):
    """method to get to the profile of a given username

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger
        user (string): the username of the user

    Returns:
        recurseive call to itself if the page is not loaded or if problem-indicating popups occur, None otherwise

    """
    try:
        driver.get("https://twitter.com/" + user)
    except:
        if not check_for_internet():
            handle_connection_issues()
        else:
            logger.error("Error getting to user profile page")
            return 'fail'
    time.sleep(3)

    if check_for_notification_popup_after_getting_to_profile_page(driver):
        time.sleep(1)
        return get_to_user_profile_link(driver, logger, user)

    if check_for_signup_popup_after_getting_to_profile_page(driver):
        time.sleep(1)
        return get_to_user_profile_link(driver, logger, user)


# method to get to the follower page from a profile page
def click_follower_button_of_profile_page(driver, logger, attempt=0):
    """method to get to the follower page from a profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger
        attempt (int): the number of attempts to click the button (either 0 or 1 indicating first time or not)

    Returns:
        recursively call itself if the button is not clicked, None otherwise

    """
    try:
        element = driver.find_element(By.PARTIAL_LINK_TEXT, "Followers")
        element.click()
        return
    except:
        pass

    return click_follower_button_of_profile_page(driver, logger, attempt=1)


# method to click the following button that appears on the profile page
def click_following_button_of_profile_page(driver, logger):
    """method to click the following button that appears on the profile page

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger
        attempt (int): the number of attempts to click the button (either 0 or 1 indicating first time or not)

    Returns:
        recursively call itself if the button is not clicked, None otherwise

    """
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[2]",
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH, path)
            element.click()
            return
        except:
            print("fail")
            pass


# method to find elements on a webpage by giving it a list of possible paths, IDs, class names, etc
def element_locator_function(driver):
    """method to find elements on a webpage by giving it a list of possible paths, IDs, class names, etc

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver

    Prints:
        a list of :
            [path_index , element_finder_method] : the index of the path that worked , the method used to find the working element

    """
    elements_found = 0
    input_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[2]",
    ]
    index = 0
    for input in input_list:

        try:
            element = driver.find_element(By.CSS_SELECTOR, input)
            print(f"Input {index} || By.CSS_SELECTOR")
            elements_found += 1
        except:
            pass

        try:
            element = driver.find_element(By.CLASS_NAME, input)
            elements_found += 1
            print(f"Input {index} || By.CLASS_NAME")
        except:
            pass

        try:
            element = driver.find_element(By.TAG_NAME, input)
            elements_found += 1
            print(f"Input {index} || By.TAG_NAME")
        except:
            pass

        try:
            element = driver.find_element(By.NAME, input)
            elements_found += 1
            print(f"Input {index} || By.NAME")
        except:
            pass

        try:
            element = driver.find_element(By.PARTIAL_LINK_TEXT, input)
            elements_found += 1
            print(f"Input {index} || By.PARTIAL_LINK_TEXT")
        except:
            pass

        try:
            element = driver.find_element(By.LINK_TEXT, input)
            elements_found += 1
            print(f"Input {index} || By.LINK_TEXT")
        except:
            pass

        try:
            element = driver.find_element(By.XPATH, input)
            elements_found += 1
            print(f"Input {index} || By.XPATH")
        except:
            pass

        try:
            element = driver.find_element(By.ID, input)
            elements_found += 1
            print(f"Input {index} || By.ID")
        except:
            pass

        index += 1

    if elements_found == 0:
        print("No elements found")


# method to check for internet
def check_for_internet():
    import urllib.request

    try:
        urllib.request.urlopen("http://google.com")  # Python 3.x
        return True
    except:
        return False


#method to handle when connection issues occur
def handle_connection_issues(logger):
    logger.log('Internet connection issues... waiting for connection')
    while not check_for_internet():
        time.sleep(3)
