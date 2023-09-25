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
            # Get a list of all table row elements
            table_rows = self.driver.find_elements(By.TAG_NAME, 'tr')

            if not table_rows:
                logging.error(f'Could not locate the table rows for all Orders on DOM. table_Rows: {table_rows}')
                return None

            else:
                logging.info(f'table_rows: {table_rows}')
                return table_rows

        except Exception as e:
            logging.exception(f'An error occurred: {e}')
            return None


    def scrape_orders_table_data(self):
        results = []

        table_rows = self.get_table_rows()

        if not table_rows:
            logging.error(f'Could not find Orders. table_rows:{table_rows}')
            return None

        # Iterate through each table row
        for idx, table_row_element in enumerate(table_rows):
            # skip table header row
            if idx >= 1:
            # Click table row element to trigger sidesheetbody per order
                table_row_element.click()

                sidesheetbody_is_present, sidesheetbody_element = self.wait_for_and_find_element(locator="//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']", locator_type=By.XPATH, timeout=10)

                if not sidesheetbody_is_present and not sidesheetbody_element:
                    logging.error(f'Could not locate sidesheetbody within alloted time on DOM.\nsidesheetbody_is_present: {sidesheetbody_is_present}|sidesheetbody_element:{sidesheetbody_element}')
                    return None

                elif sidesheetbody_is_present and sidesheetbody_element:
                    logging.info(f'Sidesheet element has been found. Scraping content for Order#: {idx} out of {len(table_rows)} orders...')

                    results.append(sidesheetbody_element.text)

        return results


    # todo: loop through `results` ; new func to loop through and create sheets to comprise csv

    """
# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
#
# # Loop through order_contents and create a sheet for each order
# for i, order_content in enumerate(order_contents):
#     # Convert the order content to a DataFrame
#     df = pd.DataFrame([order_content.split('\n')], columns=["Order Content"])
#
#     # Write the DataFrame to the Excel sheet
#     df.to_excel(writer, sheet_name=f"Order_{i + 1}", index=False)
#
# # Close the Pandas Excel writer and save the file
# writer.save()


1) have main scraping func return list of strings where each string elem is each order content.
2) create new func to accept this list of strings and to create each orders content as an excel sheet
    2a) create a getter func to be called within this outter func that instantiates each order content string with its Order ID which should be the first line of text in eah order string element and with the order_id variable
    2b) create a setter func that will set this order_id variable as the name of its sheet so that each sheet is named after its order_id
3) save the final excel with all sheets as a single excel file



"""