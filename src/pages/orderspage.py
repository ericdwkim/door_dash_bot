import logging
import time
import pandas as pd
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

    def get_table_rows_except_header(self):
        try:
            # Get a list of all table row elements
            table_rows = self.driver.find_elements(By.TAG_NAME, 'tr')

            if not table_rows:
                logging.error(f'Could not locate the table rows for all Orders on DOM. table_Rows: {table_rows}')
                return None, False

            else:
                logging.info(f'Table rows elements found:\n {table_rows}\nTotal number of rows from table: {len(table_rows)}\n')

                # Exclude header row elem; inclusive from 1st idx
                table_rows_minus_header = table_rows[1:]
                logging.info(f'Removed header row. Total number of orders: "{len(table_rows_minus_header)}" out of "{len(table_rows)}".')

                return table_rows_minus_header, True

        except Exception as e:
            logging.exception(f'An error occurred: {e}')
            return None, False

    def find_and_click_exit_button(self):
        exit_btn_clicked, _ = self.find_element_and_click(
            locator='//*[@id="MerchantApp"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/nav/div[1]/div[1]/div/button',
            locator_type=By.XPATH)
        return exit_btn_clicked

    def process_row(self, table_row, order_counter):
        table_row.click()
        time.sleep(5)  # wait for ssb to load on dom

        found, elem = self.wait_for_and_find_element(locator="//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']",
                                                locator_type=By.XPATH, timeout=10)

        if not found or not elem:
            logging.error(f'Could not extract order data in process_row for Order #: {order_counter}')
            return None, order_counter

        current_order = elem.text
        if not current_order:
            logging.error(f'Could not get extract data from current order via element.text')
            return None, order_counter

        logging.info(f'Extracted order data for Order #: {order_counter}')

        exit_btn_clicked = self.find_and_click_exit_button()

        if exit_btn_clicked:
            logging.info(f'Exiting sidesheet body for Order #: {order_counter}')
            return current_order, order_counter + 1  #@dev: increment counter
        else:
            logging.error(f'Could not click the exit button for Order #: {order_counter}')
            return None, order_counter

    def _get_orders(self, table_rows):
        orders = []
        order_counter = 1

        if not table_rows:
            logging.error('Received an empty list of table rows.')
            return None

        for table_row in table_rows:
            current_order, new_order_counter = self.process_row(table_row, order_counter)

            if current_order:
                orders.append(current_order)
                logging.info(f'Successfully processed and appended order for Order #: {order_counter}')
            else:
                logging.warning(f'Failed to process Order #: {order_counter}. Skipping to next.')

            if new_order_counter is None:
                logging.error(
                    f'Failed to update the order_counter for Order #: {order_counter}. Keeping the same counter.')
            else:
                order_counter = new_order_counter  #@dev: reassign already incremented counter from process_row to order_counter

        return orders

    def get_orders(self):
        table_rows, table_rows_present = self.get_table_rows_except_header()

        if not table_rows and not table_rows_present:
            logging.error(f'Could not find table_rows: {table_rows}| table_rows_present: {table_rows_present}')

        orders = self._get_orders(table_rows)

        if not orders:
            logging.error(f'Received empty list of orders. orders: {orders}')

        if table_rows and table_rows_present and orders:
            logging.info(f'Successfully scraped all orders. ')

        logging.info(f'\n***********************************\n {orders} \n********************************\n')

        return orders
