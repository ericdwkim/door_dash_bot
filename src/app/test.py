from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
# from src.pages.basepage import BasePage
import os
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class WebDriverManager:

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

    def basic_find(self, locator, locator_type):
        logging.info('trying to basic find')
        elem = self.driver.find_element(locator_type, locator)
        elem.click()
        logging.info(f'----{self.driver}')


    #
    # def find_element_and_click(self, locator ,locator_type=By.CSS_SELECTOR):
    #     """
    #     Finds element and clicks it using `WebElement.click()`
    #     :param locator:
    #     :param locator_type:
    #     :return: Tuple(bool, WebElement)
    #     """
    #     try:
    #         logging.info(f'self.driver in find_element_and_click: {self.driver}')
    #         element = self.driver.find_element(locator_type, locator)
    #         element.click()
    #         return True, element
    #     except NoSuchElementException:
    #         print(f'Element {locator} was not found.')
    #         return False, None
    #     except Exception as e:
    #         print(f'Error occurred when trying to find and click element with locator: "{locator}" resulting in error message: {str(e)}')
    #         return False, None
    #
    # def wait_for_element(self, locator, locator_type, timeout):
    #     """
    #     Waits for element by locator string using locator_type with a timeout
    #     :param locator:
    #     :param locator_type:
    #     :param timeout:
    #     :return: bool
    #     """
    #     try:
    #         logging.info(f'self.driver in wait_for_element: {self.driver}')
    #         WebDriverWait(self.driver, timeout).until(
    #             EC.visibility_of_element_located((locator_type, locator))
    #         )
    #         return True # If element is found within `timeout`
    #     except TimeoutException:
    #         return False # If exception raised


driver_manager = WebDriverManager()

driver_manager.visit()
# driver_manager.wait_for_element(locator='//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/span[3]', locator_type=By.XPATH, timeout=25)
time.sleep(30)
driver_manager.basic_find(locator='//*[@id="MerchantApp"]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/span[3]', locator_type=By.XPATH)

