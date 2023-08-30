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
            is_element_clicked = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div/span[3]'
, locator_type=By.XPATH, timeout=25)

            if not is_element_clicked:
                logging.error(f'Could not switch to History tab')
                return False
            else:
                return True

        except Exception as e:
            logging.exception(f'An error occurred trying to switch to History tab: {e}')
            return False



    def set_date_filter_to_yesterday(self):
        """
        1. wait for date filter button to load on dom
        2. click date filter button to reveal all date filter option elements (today, yesterday, etc...) via xpath locator `//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[4]/div/div/div[2]/div/div[3]/div/div/div/div/button`
        3. wait, find, and click target date filter `yesterday` via xpath locator `//*[@id="Popover-9"]/div/div[2]/button/div/div[2]/span/div`
        4. confirm date filter was set to target date by checking dom (after waiting for UI changes to load on dom) for yesterday `'//span[@class="styles__TextElement-sc-3qedjx-0 bDqyqH" and text()="Yesterday"]'`
        :return: Tuple(bool, bool, bool)
        """
        try:
            # step 1 + 2
            is_btn_element_clicked = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[4]/div/div/div[2]/div/div[3]/div/div/div/div/button', locator_type=By.XPATH, timeout=10)
            if not is_btn_element_clicked:
                logging.error('Could not click date filter button')
                return False, False, False

            # step 3
            is_yesterday_selection_element_clicked = self.wait_for_find_then_click('//div[@class="styles__MenuItemTitleWrapper-sc-8cd41l-3 cSfsq" and contains(text(),"Yesterday")]', locator_type=By.XPATH, timeout=10)
            if not is_yesterday_selection_element_clicked:
                logging.error('Could not select yesterday as date filter')
                return True, False, False

            # step 4
            is_element_present = self.wait_for_presence_of_element_located('//span[@class="styles__TextElement-sc-3qedjx-0 bDqyqH" and text()="Yesterday"]', locator_type=By.XPATH, timeout=10)
            if not is_element_present:
                logging.error('Could not confirm date filter set to yesterday')
                return True, True, False

            if is_btn_element_clicked and is_yesterday_selection_element_clicked and is_element_present:
                logging.info('Successfully set date filter to yesterday')
                return True, True, True

        except Exception as e:
            logging.exception(f'An error occurred trying to set date filter to yesterday: {e}')
            return False, False, False

