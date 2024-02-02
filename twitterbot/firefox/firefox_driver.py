import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from twitterbot.utils.logger import Logger
from twitterbot.bot.file_handler import get_creds

import psutil


import os
import shutil


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


def login_to_twitter(driver, logger) -> bool:
    start_time = time.time()

    user, password = get_creds()

    logger.change_status("Logging in to twitter...")

    # get to twitter
    if get_to_webpage(driver, "https://twitter.com") is False:
        time.sleep(5)
        return False

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
    if get_to_webpage(driver, "https://twitter.com") is False:
        return False
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


def restart_driver(driver, logger: Logger):
    logger.set_time_of_last_restart()

    close_all_firefox()

    if driver is not None:
        driver.quit()

    driver = create_firefox_driver(logger)

    while login_to_twitter(driver, logger) is False:
        logger.change_status("Failed to login to twitter, retrying...")
        try:
            driver.quit()
        except:
            pass
        close_all_firefox()
        driver = create_firefox_driver(logger)

    logger.add_restart()

    return driver


def delete_scoped_dirs(folder_path):
    deleted_count = 0
    for entry in os.listdir(folder_path):
        entry_path = os.path.join(folder_path, entry)
        if os.path.isdir(entry_path) and "scoped_dir" in entry:
            try:
                shutil.rmtree(entry_path)
                print(f"{entry_path} and its contents deleted successfully.")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {entry_path}: {e}")

    return deleted_count


def delete_old_firefox_data():
    top_level = r"C:\Windows\SystemTemp"

    deleted_count = delete_scoped_dirs(top_level)

    print(
        f'Total {deleted_count} directories containing "scoped_dir" have been deleted.'
    )


def get_firefox_pids():
    pids = []
    for process in psutil.process_iter(["pid", "name"]):
        try:
            # Print the process name and PID
            pid = process.info["pid"]
            name = process.info["name"]
            if "firefox" in name:
                pids.append(pid)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle exceptions that might occur while accessing process information
            pass

    return pids


def close_window_by_pid(pid):
    try:
        psutil.Process(pid).terminate()

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass


def close_all_firefox():
    for _ in range(5):
        pids = get_firefox_pids()
        for pid in pids:
            close_window_by_pid(pid)


def create_firefox_driver(logger):
    start_time = time.time()
    logger.change_status("Creating firefox driver...")

    try:
        # Set Firefox options
        firefox_options = Options()

        # firefox_options.add_argument('-headless')
        firefox_options.add_argument("--mute-audio")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-software-rasterizer")

        driver = webdriver.Firefox(options=firefox_options)

        if configure_driver(driver):
            logger.change_status(
                f"Successfully created and configured firefox driver in {str(time.time() - start_time)[:5]}s"
            )
        else:
            logger.change_status("Failed to create and configure firefox driver")

        return driver
    except:
        logger.change_status("Failed to create firefox driver")
        return False


def create_background_firefox_driver(logger):
    try:
        # Set Firefox options
        firefox_options = Options()

        # firefox_options.add_argument('-headless')
        # firefox_options.add_argument("--start-minimized")
        firefox_options.add_argument("--mute-audio")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--disable-software-rasterizer")
        firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(options=firefox_options)

        configure_background_driver(driver)

        return driver

    except Exception as e:
        print(f"Failed to made driver for reason: {e}")
        return False


def configure_driver(driver) -> bool:
    try:
        driver.set_window_size(800, 800)
        driver.set_window_position(0, 0)
        return True
    except:
        return False


def configure_background_driver(driver) -> bool:
    try:
        driver.set_window_size(800, 800)
        driver.set_window_position(20000, 20000)
        return True
    except:
        return False


def find_element_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)


def get_to_webpage(driver, url) -> bool:
    try:
        driver.get(url)
        time.sleep(0.33)
    except:
        return False

    if check_for_timeout_webpage(driver):
        return False

    return True


def check_for_timeout_webpage(driver) -> bool:
    x_paths = [
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div/span/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div[1]/span",
        "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[1]/span",
    ]

    for xpath in x_paths:
        try:
            element = find_element_by_xpath(driver, xpath)

            text = element.text

            print(element.text)
            print(element.text)

            if "mething went wrong. Try reloading" in text or "Retry" in text:
                return True
        except:
            pass
    return False


def scroll_down_to_load_more(driver, scroll_pause_time=2, num_scrolls=5):
    try:
        # Get current page height
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down multiple times to load more content
        for _ in range(num_scrolls):
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load more content
            time.sleep(scroll_pause_time)

            # Calculate new page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # Break if no more content is loaded
            if new_height == last_height:
                break

            # Update last height
            last_height = new_height

    except Exception as e:
        print(f"Error while scrolling down: {str(e)}")


delete_old_firefox_data()


if __name__ == "__main__":
    logger = Logger()
    print(login_to_twitter(create_firefox_driver(logger), logger))
