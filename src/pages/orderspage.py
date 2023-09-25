import logging
import time
from src.pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrdersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


    def switch_to_history_tab(self):

        try:
            is_element_clicked, history_tab_element = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/span[3]'
, locator_type=By.XPATH, timeout=10)

            if not is_element_clicked and not history_tab_element:
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
            is_btn_element_clicked, button_element = self.wait_for_find_then_click('//*[@id="MerchantApp"]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div/div/div[2]/div/div[3]/div/div/div/div/button', locator_type=By.XPATH, timeout=10)
            if not is_btn_element_clicked and not button_element:
                logging.error('Could not click date filter button')
                return False, False, False

            logging.info('waiting for button click to load on dom ....')
            time.sleep(5)

            # step 3
            is_yesterday_selection_element_clicked, yesterday_selector_element= self.wait_for_find_then_click('//div[@class="styles__MenuItemTitleWrapper-sc-8cd41l-3 cSfsq" and contains(text(),"Yesterday")]', locator_type=By.XPATH, timeout=10)
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


    def get_table_rows(self):
        try:
            # Locate the table body element
            table_body = self.driver.find_element(By.XPATH,
                                             '//*[@id="MerchantApp"]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div/div/div[5]/div[1]/div/table')
            if not table_body:
                logging.error(f'Could not locate the table body of all Orders on DOM. table_body: {table_body}')
                return False, False, None

            logging.info(f'table_body: {table_body}')

            # Get a list of all table row elements
            table_rows = self.driver.find_elements(By.TAG_NAME, 'tr')

            if not table_rows:
                logging.error(f'Could not locate the table rows for all Orders on DOM. table_Rows: {table_rows}')
                return True, False, None
            else:
                logging.info(f'table_rows: {table_rows}')
                return True, True, table_rows

        except Exception as e:
            logging.exception(f'An error occurred: {e}')

    def scrape_orders_table_data(self):
        results = []

        try:
            located_table_body, located_table_rows, table_rows_element = self.get_table_rows()

            if located_table_body and located_table_rows and table_rows_element:


                # Iterate through each table row
                for table_row in table_rows_element:

                    results.append(table_row.text)



                # Click on the table row to trigger the sidesheetbody
                # table_row.click()
                # wait for dom to load sidesheetbody?
                # time.sleep(20)

                # Wait for the sidesheetbody element to load
                # waited_for_sidesheetbody_and_is_visible = self.wait_for_element(locator='//*[@id="MerchantApp"]/div/div/div[3]/div[2]/div[2]/div/div', locator_type=By.XPATH, timeout=10)

                # if not waited_for_sidesheetbody_and_is_visible:
                #     logging.error(f'Tried waiting for sidesheetbody element to be visible, but could not locate within allotted time. waited_for_sidesheetbody_and_is_visible: {waited_for_sidesheetbody_and_is_visible}')
                #     return True, True, False
                # logging.info(f'type(waited_for_sidesheetbody_and_is_visible): {type(waited_for_sidesheetbody_and_is_visible)}') # ideally an element to simply `.text` from, but unlikely...
                # logging.info(f'waited_for_sidesheetbody_and_is_visible.text: {waited_for_sidesheetbody_and_is_visible.text}')


                # else:
                #     logging.info(f'type(waited_for_sidesheetbody_and_is_visible): {type(waited_for_sidesheetbody_and_is_visible)}') # ideally an element to simply `.text` from, but unlikely...
                #     return True, True, True

                return results
        except Exception as e:
            logging.exception(f'An error occurred trying to scrape_orders_table_data: {e}')