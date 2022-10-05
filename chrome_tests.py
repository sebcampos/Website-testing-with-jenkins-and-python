import time

import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import Webpages

website_url = "https://thesensisociety.com"

driver, actions, wait = chrome.init_webdriver()


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
    assert valid_age_btn.is_displayed()
    assert invalid_age_btn.is_displayed()
    assert register_btn.is_displayed()


def test_validate_redirect_for_underage():
    driver.get(website_url)
    driver.delete_all_cookies()
    valid_age_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, Webpages.Homepage.younger_than_21_button))
    )
    valid_age_btn.click()
    driver.switch_to.window(driver.window_handles[1])
    assert driver.current_url != "https://thesensisociety.com/?"
    assert "google.com" in driver.current_url


def test_navigate_to_check_out():
    driver.get(website_url)
    driver.delete_all_cookies()
    valid_age_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, Webpages.Homepage.older_than_21_button))
    )
    actions.double_click(valid_age_btn).perform()
    time.sleep(0.5)
    assert not valid_age_btn.is_displayed()
    start_delivery_spn = wait.until(
        EC.element_to_be_clickable((By.XPATH, Webpages.Homepage.start_delivery_spn))
    )
    actions.reset_actions()
    actions.pause(5).move_to_element.(start_delivery_spn).click(start_delivery_spn).perform()
    time.sleep(30)
    tear_down()


def tear_down():
    driver.close()
    driver.quit()
