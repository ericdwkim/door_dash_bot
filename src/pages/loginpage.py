import os
import logging
from src.pages.basepage import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):

    def __init__(self, base_driver):
        super().__init__(base_driver)
        self.url = os.getenv('DD_MERCHANT_LOGIN_URL')
        self.username = os.getenv('DEV_LOGIN_EMAIL')
        self.password = os.getenv('DEV_LOGIN_PASSWORD')

    def visit(self):
        """
        launch browser and navigate to URL
        :return: bool
        """
        try:
            logging.info('Launching DoorDash Merchant Portal....')
            self.driver.get(self.url)
            return True
        except Exception as e:
            logging.exception(f'Browser could not be launched\nAn error occurred trying to visit "{self.url}". Error message: {e}')

    def enter_username(self):
        try:
            is_element_present, was_clicked, element_selector_clicked = self.wait_for_find_then_click_then_send_keys('//*[@id="FieldWrapper-0"]', keys_to_send=self.username, locator_type=By.XPATH, timeout=10)
            if not is_element_present and not was_clicked and not element_selector_clicked:
                return False, False, None
            else:
                return True, True, element_selector_clicked
        except Exception as e:
            logging.exception(f'An error occurred trying to enter_username: {e}')
            return False, False, None

    def enter_password(self):
        try:
            is_element_present, was_clicked, element_selector_clicked = self.wait_for_find_then_click_then_send_keys('//*[@id="FieldWrapper-1"]', keys_to_send=self.password, locator_type=By.XPATH, timeout=10)
            if not is_element_present and not was_clicked and not element_selector_clicked:
                return False, False, None
            else:
                return True, True, element_selector_clicked
        except Exception as e:
            logging.exception(f'An error occurred trying to enter_username: {e}')
            return False, False, None

    def click_login_button(self):
        try:
            was_clicked = self.wait_for_find_then_click('//*[@id="login-submit-button"]', locator_type=By.XPATH, timeout=10)
            if not was_clicked:
                logging.error('Could not click_login_button')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to click_login_button: {e}')
            return False

    def login(self):
        try:
            username_entered = self.enter_username()
            password_entered = self.enter_password()
            login_btn_clicked = self.click_login_button()
            if username_entered and password_entered and login_btn_clicked:
                logging.info('Successfully logged in!')
                return True
            else:
                logging.error(f'Could not login with provided credentials')
                return False
        except Exception as e:
            logging.exception(f'An error occurred trying to login: {e}')
            return False

    def visit_and_login(self):
        try:
            if not self.visit():
                return False
            if not self.login():
                return False
            else:
                logging.info('Browser launched successfully!')
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to visit_and_login: {e}')



