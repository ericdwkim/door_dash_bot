from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from src.pages.basepage import BasePage
import os
import logging
from selenium.webdriver.common.by import By


class TestDriver:

    def __init__(self):
        self.url = os.getenv('DD_MERCHANT_LOGIN_URL')
        self.setup_driver()

    def setup_driver(self):
        options = self._get_chrome_options()
        chromedriver_exe_path = '/opt/homebrew/bin/chromedriver'


        self.driver = webdriver.Chrome(
            service=Service(executable_path=chromedriver_exe_path),
            options = options
        )

    def _get_chrome_options(self):
        options = ChromeOptions()
        options.add_argument('--remote-debugging-port=9222')

        return options

    def visit(self):
        self.driver.get(self.url)
        print(f'=----------------------------')


class OrdersPage(BasePage):

    def __init__(self, driver):
        super(). __init__(driver)
    def switch_to_history_tab(self):

        try:
            is_element_clicked = self.wait_for_find_then_click(
                '//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/span[3]'
                , locator_type=By.XPATH, timeout=25)

            if not is_element_clicked:
                logging.error(f'Could not switch to History tab')
                return False
            else:
                return True

        except Exception as e:
            logging.exception(f'An error occurred trying to switch to History tab: {e}')
            return False


td = TestDriver()

td.visit()

op = OrdersPage(td)

op.switch_to_history_tab()

