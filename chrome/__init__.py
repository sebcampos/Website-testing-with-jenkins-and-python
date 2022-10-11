from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def init_webdriver(headless=None, production=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.headless = True
    if production:
        driver = webdriver.Chrome(options=options, executable_path="/home/thesensisocietydelivery/google-chrome-stable_current_amd64.deb")
    else:
        driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)
    return driver, actions, wait
