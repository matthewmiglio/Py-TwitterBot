from selenium.webdriver.common.by import By
import time


# method to write a given username to the username input box on the login page
def write_to_username_input_box(driver, text):
    try:
        element = driver.find_element(By.NAME, "text")
        element.send_keys(text)
    except:
        return write_to_username_input_box(driver, text)


def click_next_button_after_username_input(driver):
    try:
        element = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span",
        )
        element.click()
    except:
        return click_next_button_after_username_input(driver)


def write_password_to_password_text_box(driver, password):
    try:
        element = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input",
        )
        element.send_keys(password)
    except:
        return write_password_to_password_text_box(driver, password)


def click_log_in_button_after_password_input(driver):
    try:
        element = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span",
        )
        element.click()
    except:
        return click_log_in_button_after_password_input(driver)


# main method for logging in to twitter.com
def log_in_to_twitter(driver, logger, username, password):
    logger.set_current_state("Login")

    start_time = time.time()
    link = "https://twitter.com/login"
    logger.log(message=f"Initializing chrome driver on webpage {link}", state="login")
    driver.get(link)
    # time.sleep(5)

    logger.log(message="starting sequence", state="Login")

    write_to_username_input_box(driver, username)

    click_next_button_after_username_input(driver)

    write_password_to_password_text_box(driver, password)

    click_log_in_button_after_password_input(driver)

    logger.log(
        message=f"Logged in to twitter in {str(time.time()-start_time)[:4]} seconds",
        state="login",
    )
    time.sleep(5)
