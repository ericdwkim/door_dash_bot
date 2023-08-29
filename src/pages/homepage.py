import time
import logging
from src.pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


    def switch_to_orders_page(self):

        try:
            is_element_clicked = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div[1]/ul/div[3]/div/div/span[5]/a/div/div', locator_type=By.XPATH)
            if not is_element_clicked:
                logging.error(f'Could not switch to Orders page')
                return False
            else:
                return True

        except Exception as e:
            logging.exception(f'An error occurred trying to switch to Orders page: {e}')
            return False

