from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


def init_webdriver(headless=None, production=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.headless = True
    if production:
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    else:
        driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)
    return driver, actions, wait
