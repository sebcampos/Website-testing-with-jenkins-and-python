import requests
import chrome
import Webpages
import asyncio
from Webpages import utils
from Webpages.utils import EC, By

HEADLESS = True
PRODUCTION = True

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    global driver, actions, wait, website_url, chrome_logger
    chrome_logger = utils.set_up_logger("chrome_tests")
    website_url = "https://thesensisociety.com"
    driver, actions, wait = chrome.init_webdriver(HEADLESS, PRODUCTION)


def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    driver.close()
    driver.quit()


def test_validate_website_certificate():
    async def ping_website():
        proc = await asyncio.create_subprocess_shell(
            "openssl s_client -connect thesensisociety.com:443",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()
        stdout = stdout.decode()
        if "Verify return code: 0 (ok)" in stdout:
            chrome_logger.info("[PASSED] OpenSSL returned 0 (ok) for website certificate")
            return True
        else:
            chrome_logger.warning("[FAILED] OpenSSL returned 1 (fail) for website certificate")
            return False
    assert asyncio.run(ping_website())


def test_validate_website_returns_status_code_200():
    r = requests.get(website_url, verify=False)
    if r.status_code == 200:
        chrome_logger.info("[PASSED] Website returns 200 code")
    else:
        chrome_logger.warning("[FAILED] Website is not returning 200 code")
    assert r.status_code == 200

def test_chrome_age_and_registration_verification_pop_up_appears():
    driver.get(website_url)
    driver.delete_all_cookies()
    valid_age_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, Webpages.Homepage.younger_than_21_button))
    )
    invalid_age_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, Webpages.Homepage.older_than_21_button))
    )
    register_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, Webpages.Homepage.become_a_member_button))
    )
    if valid_age_btn.is_displayed():
        chrome_logger.info("[PASSED] 'Older than 21' is displayed on the pop up")
    else:
        chrome_logger.warning("[FAILED] 'Older than 21' is NOT displayed on the pop up")
    if invalid_age_btn.is_displayed():
        chrome_logger.info("[PASSED] 'Younger than 21' is displayed on the pop up")
    else:
        chrome_logger.warning("[FAILED] 'Younger than 21' is NOT displayed on the pop up")
    if register_btn.is_displayed():
        chrome_logger.info("[PASSED] 'Register' button is displayed on the pop up")
    else:
        chrome_logger.warning("[FAILED] 'Register' button is NOT displayed on the pop up")

    assert valid_age_btn.is_displayed()
    assert invalid_age_btn.is_displayed()
    assert register_btn.is_displayed()


def test_validate_redirect_for_underage():
    driver.get(website_url)
    driver.delete_all_cookies()
    invalid_age_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, Webpages.Homepage.younger_than_21_button))
    )
    invalid_age_btn.click()
    chrome_logger.info("[PASSED] Selected Younger than 21 option")
    if len(driver.window_handles) != 1:
        driver.switch_to.window(driver.window_handles[1])
        chrome_logger.info("[PASSED] Navigated to newly opened window")
    else:
        chrome_logger.warning("[FAILED] No new window detected")

    assert len(driver.window_handles) != 1
    assert driver.current_url != "https://thesensisociety.com/?"
    assert "google.com" in driver.current_url
    chrome_logger.info("[PASSED] Selecting younger than 21 navigates to a new chrome window")


def test_navigate_to_check_out():
    driver.get(website_url)
    assert utils.navigate_to_start_delivery(driver, actions, wait, chrome_logger)
