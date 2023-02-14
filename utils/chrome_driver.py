from selenium.webdriver.chrome.options import Options
from selenium import webdriver

#method to make a chrome webpage driver object using selenium and chromedriver v1.0.9
def make_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    try:
        return webdriver.Chrome(
            # executable_path=r"C:\Users\matt\Desktop\chromedriver.exe",
            options=chrome_options,
        )
    except:
        return webdriver.Chrome(
            # executable_path=r"C:\Users\matmi\OneDrive\Desktop\chromedriver.exe",
            options=chrome_options,
        )
