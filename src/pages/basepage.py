from selenium import webdriver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class BasePage(object):
    def __init__(self, base_driver):
        """

        :param base_driver: instance of `BaseDriver` class
        `base_driver.driver`: instance of `ChromeDriver` class
        :return:
        """
        self.driver = base_driver.driver
        self.action = ActionChains(self.driver)

    def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
        """
        Finds element and clicks it using `WebElement.click()`
        :param locator:
        :param locator_type:
        :return: Tuple(bool, WebElement)
        """
        try:
            element = self.driver.find_element(locator_type, locator)
            if not element:
                logging.error(f'Could not locate element via locator "{locator}".')
            element.click()
            return True, element
        except NoSuchElementException:
            logging.exception(f'Element {locator} was not found.')
            return False, None
        except Exception as e:
            logging.exception(f'Error occurred when trying to find and click element with locator: "{locator}" resulting in error message: {str(e)}')
            return False, None

    def find_element_and_click_and_send_keys(self, locator, locator_type, keys_to_send):
        """
        Find element by locator string, click on element, and send keys
        :param locator:
        :param keys_to_send:
        :return: bool
        """
        try:
            was_clicked, element_selector_clicked = self.find_element_and_click(locator, locator_type)
            if not was_clicked:
                logging.error(f'Failed to send keys to element: {locator}')
                return False
            else:
                element_selector_clicked.send_keys(keys_to_send)
                return True
        except Exception as e:
            logging.exception(f'An error occurred: {str(e)}')
            return False

    def wait_for_element(self, locator, locator_type, timeout):
        """
        Waits for element by locator string using locator_type with a timeout
        :param locator:
        :param locator_type:
        :param timeout:
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((locator_type, locator))
            )
            return True # If element is found within `timeout`
        except TimeoutException:
            return False # If exception raised

    def wait_for_and_find_element(self, locator, locator_type, timeout):
        try:
            wait = self.wait_for_element(locator, locator_type, timeout)
            if not wait:
                logging.error(f'Tried to wait to locate element via locator "{locator}", but timed out')
                return False, None
            element = self.driver.find_element(locator_type, locator)
            if not element:
                logging.error(f'Could not find element via locator "{locator}"')
                return True, None
            if wait and element:
                logging.info(f'Found and located element via locator "{locator}"')
                return True, element

        except Exception as NoSuchElementException:
            logging.exception(f'An unexpected error occurred: {NoSuchElementException}')



    def wait_for_find_then_click_then_send_keys(self, locator, keys_to_send, locator_type, timeout):
        """

        :param locator:
        :param keys_to_send:
        :param locator_type:
        :return: Tuple(Bool, Bool, WebElement | None) `is_element_present`, `was_clicked`, `element_selector_clicked`
        """

        try:
            is_element_present = self.wait_for_element(locator, locator_type, timeout)
            if not is_element_present:
                logging.error(f'Could not wait for element with locator: "{locator}" to be present on DOM')
                return False, False, None
            was_clicked, element_selector_clicked = self.find_element_and_click(locator, locator_type)
            if not was_clicked and not element_selector_clicked:
                logging.error(f'Could not find_element_and_click for element with locator: "{locator}" using locator_type: "{locator_type}"')
                return True, False, None
            else:
                logging.info(f'Successfully waited, found, and clicked on element with locator: "{locator}" with clicked WebElement: "{element_selector_clicked}"\nSending keys: "{keys_to_send}"....')
                element_selector_clicked.send_keys(keys_to_send)
                return True, True, element_selector_clicked
        except NoSuchElementException:
            logging.exception(f'NoSuchElementException: The element "{locator}" was not found.')
            return False, False, None

    def wait_for_find_then_click(self, locator, locator_type, timeout):
        """
        `wait_for_element()` + `find_element_and_click()`\n wrapper using `WebElement.click()`
        :param locator_type: default to CSS SELECTOR
        :param locator: locator string for element to wait and click
        :return: bool, WebElement | None
        """
        try:
            is_element_present = self.wait_for_element(locator, locator_type, timeout)
            if not is_element_present:
                logging.error(f'Element "{locator}" was not present.')
                return False, None
            else:
                element = self.find_element_and_click(locator, locator_type)
                return True, element
        except NoSuchElementException:
            logging.exception(f'NoSuchElementException: The element "{locator}" was not found.')
            return False, None

    def wait_for_presence_of_element_located(self, locator, locator_type, timeout):
        """
        Checking for element to be visible
        :param locator:
        :param locator_type:
        :param timeout:
        :return: bool
        """

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator))
            )
            return True
        except (NoSuchElementException, TimeoutException):
            logging.exception(f'Tried to check visibility of WebElement: {locator} using locator type: {locator_type}')
            return False
