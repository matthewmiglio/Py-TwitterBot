from selenium.webdriver.common.by import By
import time

# READING SECTION_______________________________________________________________


def check_for_signup_popup_after_getting_to_profile_page(driver):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/span",
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


def check_for_notification_popup_after_getting_to_profile_page(driver):
    for path in [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span",
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
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]/svg/g/path",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]/svg",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/span[2]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]/svg/g/path",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]/svg",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span[2]",
    ]
    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if 'aria-label="Protected account"' in text:
                return True
        except:
            pass
    return False


# method to get a user's description value
def get_description_text_of_this_user(driver):
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
    input_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/div/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div[1]/div[2]/div[5]/div[1]/div/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div[2]/div[4]/div[1]/a/span[1]/span",
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


def parse_follower_value(value):
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
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[1]/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div[2]/a/span",
    ]

    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if "u are unable to follow more people at th" in text:
                return True
        except:
            pass
    return False


# method to read all the username elements from the list of followers/followings page
def get_names_of_followers_on_follower_list_page(driver, logger):
    username_list = []
    for index in range(0, 100):
        for path in [
            f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{index}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span",
            # f"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[{index}]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/a/div/div/span",
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


# method to check for the unfollow confirmation popup that arises when following a user from their profile page
def check_for_unfollow_confirmation_popup(driver):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]",
    ]
    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            return True
        except:
            return False


# method to check for the login popup that may popup when getting to a new profile page
def check_for_login_popup_after_following_on_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/a[2]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/span",
    ]
    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if "gn up so you never miss their T" in text:
                return True
        except:
            pass
    return False


# method to check for the unfollow popup that occues when following a user from their profile page
def check_for_unfollow_popup_after_following_on_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/h1/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/span[1]",
        '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/span[1]',
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH ,path)
            text = element.get_attribute("innerHTML")
            if "eir Tweets will no longer show up in your" in text:
                return True
        except:
            pass
    return False


# method to check for the unfollow confirmatino popup when unfollowing a user from their profile page
def check_for_unfollow_confirmation_popup_on_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/h1/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/span[1]",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div",
    ]

    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if "ir Tweets will no longer show up in your home tim" in text:
                return True
        except:
            pass
    return False


# method to check for the signup popup that occurs when getting to a new profile page
def check_for_signup_buttons_on_bottom_of_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/a/div",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div/span/span",
        "/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div[2]/a/div/span/span",
    ]
    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if "Sign up" in text:
                return True
        except:
            pass
    return False


# ACTION SECTION_______________________________________________________________

# method to click confirm unfollow button in the unfollow confirmation popup that occuers when unfollowing a user from their profile page
def click_unfollow_confirmation_popup_on_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div",
        "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]",
    ]
    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            element.click()
            return "success"
        except:
            pass
    return "fail"


# method to click the follow button when on a profile page
def click_follow_button_of_profile_page(driver, logger):
    path_list = [
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/span/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div/span',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div',
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div  ',
    ]
    for path in path_list:
        try:
            element = driver.find_element(By.XPATH,path)
            text = element.get_attribute("innerHTML")
            if 'Follow' in text:
                element.click()
                return "success"
        except:
            pass
    return "fail"


# method to click the unfollow button when on a profile page
def click_unfollow_button_of_profile_page(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div/span/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div/div",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]/div",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[4]/div[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/span/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span/span",
    ]

    for path in path_list:
        try:
            element = driver.find_element_by_xpath(path)
            text = element.get_attribute("innerHTML")
            if "following" in text.lower():
                element.click()

                if check_for_unfollow_confirmation_popup_on_profile_page(
                    driver, logger
                ):
                    click_unfollow_confirmation_popup_on_profile_page(driver, logger)

                return "success"
        except:
            pass
    return "fail"


# method to get to the follower page from a profile page
def click_program_user_profile_button(driver, logger):
    path_list = [
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]/div/div/svg",
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]/div",
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]/div",
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]/div/div[2]",
        "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]/div/div[1]",
    ]

    for p in path_list:
        try:
            element = driver.find_element(By.XPATH, p)
            element.click()
        except:
            pass


# method to scroll to the bottom of the page as far as it has loaded
def scroll_to_bottom(driver, logger):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# method to get to the profile of a given username
def get_to_user_profile_link(driver, logger, user):
    driver.get("https://twitter.com/" + user)
    time.sleep(3)

    if check_for_notification_popup_after_getting_to_profile_page(driver):
        time.sleep(1)
        return get_to_user_profile_link(driver, logger, user)

    if check_for_signup_popup_after_getting_to_profile_page(driver):
        time.sleep(1)
        return get_to_user_profile_link(driver, logger, user)


# method to get to the follower page from a profile page
def click_follower_button_of_profile_page(driver, logger, attempt=0):
    try:
        element = driver.find_element(By.PARTIAL_LINK_TEXT, "Followers")
        element.click()
        return
    except:
        pass

    return click_follower_button_of_profile_page(driver, logger, attempt=1)


# method to click the following button that appears on the profile page
def click_following_button_of_profile_page(driver, logger, attempt=0):

    path = "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[2]/span"
    try:
        element = driver.find_element_by_xpath(path)
        element.click()
        return
    except:
        pass

    return click_following_button_of_profile_page(driver, logger, attempt=1)


# UTILS SECTION_______________________________________________________________


# method to check if a given element's string is an html element
def check_if_string_is_html_element(string):
    if 'dir="' in string:
        return True
    if "css-" in string:
        return True
    if "href=" in string:
        return True
    if "class=" in string:
        return True
    if "role=" in string:
        return True

    return False


def element_locator_function(driver):
    elements_found = 0
    input_list = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a",
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
