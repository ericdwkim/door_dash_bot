import os
import logging
from src.pages.basepage import BasePage

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
            self.driver.get(self.url)
            return True
        except Exception as e:
            logging.exception(f'Browser could not be launched\nAn error occurred trying to visit "{self.url}". Error message: {e}')

    def enter_username(self):
        try:
            was_clicked = self.find_element_and_click_and_send_keys("#FieldWrapper-0", self.username)
            if not was_clicked:
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to enter_username: {e}')
            return False

    def enter_password(self):
        try:
            was_clicked = self.find_element_and_click_and_send_keys("#FieldWrapper-1", self.password)
            if not was_clicked:
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to enter_password: {e}')
            return False

    def click_login_button(self):
        try:
            was_clicked, element_selector_clicked = self.find_element_and_click("#cmdGo")
            if not was_clicked:
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



