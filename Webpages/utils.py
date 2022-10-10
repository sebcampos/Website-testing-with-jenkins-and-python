from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from . import Homepage
from . import StartDeliveryPage

import logging
from DummyData import Customer


def set_up_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


def select_valid_age_popup_option(driver, actions, wait):
    driver.delete_all_cookies()
    valid_age_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, Homepage.older_than_21_button))
    )
    actions.double_click(valid_age_btn).perform()
    actions.reset_actions()
    wait.until(
        EC.invisibility_of_element_located((By.XPATH, Homepage.older_than_21_button))
    )
    assert not valid_age_btn.is_displayed()
    return True


def navigate_to_start_delivery(driver, actions, wait, logger):
    select_valid_age_popup_option(driver, actions, wait)
    start_delivery_spn = wait.until(
        EC.element_to_be_clickable((By.XPATH, Homepage.start_delivery_spn))
    )

    driver.execute_script("arguments[0].click();", start_delivery_spn)
    meadow_frames = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, StartDeliveryPage.shopping_iframes))
    )
    driver.switch_to.frame(meadow_frames[1])
    address_label = wait.until(
        EC.visibility_of_element_located((By.XPATH, StartDeliveryPage.address_input_label))
    )
    if address_label.is_displayed():
        logger.info("[PASSED] Navigated to start Delivery page")
        return True
    else:
        logger.warning("[FAILED] Unable to navigate to start Delivery page")
        return False
