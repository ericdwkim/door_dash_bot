import logging
from src.pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrdersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


    def switch_to_history_tab(self):

        try:
            is_element_clicked = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/span[3]', locator_type=By.XPATH, timeout=20)
            if not is_element_clicked:
                logging.error(f'Could not switch to History tab')
                return False
            else:
                return True

        except Exception as e:
            logging.exception(f'An error occurred trying to switch to History tab: {e}')
            return False

