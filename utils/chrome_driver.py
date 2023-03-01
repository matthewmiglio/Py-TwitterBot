from selenium.webdriver.chrome.options import Options
from selenium import webdriver


"""
chrome_driver.py ->  function for making a chrome driver object (a fresh browser window that can be interacted with using selenium calls)
"""


# method to make a chrome webpage driver object using selenium and chromedriver v1.0.9
def make_chrome_driver():
    """

    Args:
        None

    Returns:
        selenium.webdriver.chrome.webdriver.WebDriver: the selenium chrome driver

    """

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('log-level=3')

    return webdriver.Chrome(
        options=chrome_options,
    )
