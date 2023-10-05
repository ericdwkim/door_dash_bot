from src.app.drivers import BaseDriver, OrdersPageDriver
import os
import time
import argparse
import pandas as pd
from datetime import datetime
import logging
from src.utils.log_config import setup_logger
from src.utils.data_handler import get_prettified_and_mapped_orders, convert_flattened_orders_to_df, json_str_to_file
from src.utils.data_merger import DataMerger
from src.utils.excel_formatter import ExcelFormatter

class Main:

    # ---------------------------------- Instance attributes ----------------------------------
    def __init__(self, headless=False):
        self.base_driver = BaseDriver(headless=headless)
        self.orders_page_driver = OrdersPageDriver(self.base_driver)
        self.today = datetime.today().strftime('%m.%d.%y')
        self.excel_file_name = f'DD {self.today}.xlsx'
        self.excel_output_file_path = f"/Users/ekim/workspace/txb/mock/g-drive/imports/ir/Door Dash/DD Daily Order Details/{self.excel_file_name}"

        # G:\Imports\IR\Door Dash\DD Daily Order Details # prod

    # ---------------------------------- Instance attributes ----------------------------------

    def switch_to_history_tab(self):
        switched_to_history_tab = self.orders_page_driver.switch_to_history_tab()
        if not switched_to_history_tab:
            logging.error('Could not orders_page_driver.switch_to_history_tab')
            return False
        else:
            logging.info('Successfully orders_page_driver.switch_to_history_tab')
            return True

    def set_date_filter_to_yesterday(self):
        date_filter_set_to_yesterday = self.orders_page_driver.set_date_filter_to_yesterday()
        if not date_filter_set_to_yesterday:
            logging.error('Could not orders_page_driver.set_date_filter_to_yesterday')
            return False
        else:
            logging.info('Successfully orders_page_driver.set_date_filter_to_yesterday')
            return True

    def switch_to_history_tab_and_set_date_filter_to_yesterday(self):
        try:

            switched_to_history_tab = self.switch_to_history_tab()
            if not switched_to_history_tab:
                logging.error(
                    'Could not switch_to_history_tab in switch_to_history_tab_and_set_date_filter_to_yesterday')
                return False, False

            date_filter_set_to_yesterday = self.set_date_filter_to_yesterday()
            if not date_filter_set_to_yesterday:
                logging.error(
                    'Could not set_date_filter_to_yesterday in switch_to_history_tab_and_set_date_filter_to_yesterday')
                return True, False

            if switched_to_history_tab and date_filter_set_to_yesterday:
                logging.info(f'Successfully switched_to_history_tab and date_filter_set_to_yesterday')
                return True, True

        except Exception as e:
            logging.exception(
                f'An error occurred attempting to switch_to_history_tab_and_set_date_filter_to_yesterday {e}')
            return False, False

    def get_sheet_name(self, order_df):
        try:
            store_num = order_df[0]['Store Number']
            sheet_name = f'#{store_num}'

            if sheet_name == '#NaN':
                logging.warning(
                    f"Order: '{order_df[0]['Order']}'\'s Store Number could not be properly matched using Pick Up Location: '{order_df[0]['Pick Up Location']}'. Sheet name has been set to NaN.")

            return sheet_name, True
        except Exception as e:
            logging.exception(f"An error occurred while getting sheet name: {e}")
            return None, False

    def get_orders(self):
        try:
            orders = self.orders_page_driver.get_orders()
            if not orders:
                logging.error('Could not scrape orders data')
                return None
            else:
                return orders
        except Exception as e:
            logging.exception(f'An error occurred: {e}')
            return None

    # 
    def get_excel_output(self, orders_dfs):
        try:
            with pd.ExcelWriter(self.excel_output_file_path, engine='xlsxwriter') as writer:
                for idx, order_df in enumerate(orders_dfs):
                    sheet_name, success = self.get_sheet_name(order_df)
                    if not success:
                        return False

                    order_df.to_excel(writer, sheet_name, header=False, index=True)

                    formatter = ExcelFormatter(writer, sheet_name, order_df)
                    formatter.apply_sheet_formats()

            return True
        except Exception as e:
            logging.exception(f"An error occurred while generating Excel output: {e}")
            return False

    def run_main(self):
        self.setup()
        if not self.switch_to_history_tab_and_set_date_filter_to_yesterday():
            logging.error("Failed to initialize DoorDash Bot")
            return

        raw_orders = self.get_raw_orders()
        if raw_orders is None:
            logging.error("Failed to fetch orders")
            return

        orders_with_store_nums = self.merge_data(raw_orders)
        orders_dfs = self.convert_to_dataframes(orders_with_store_nums)

        self.export_to_excel(orders_dfs)
        logging.info(f'Orders Spreadsheet has been saved to: {self.excel_output_file_path}')

    def setup(self):
        setup_logger()

    def get_raw_orders(self):
        return self.get_orders()

    def merge_data(self, raw_orders):
        orders_json = get_prettified_and_mapped_orders(raw_orders)
        self.output_json(orders_json, 'orders_json.csv', 'Writing orders_json stdout...')

        dm = DataMerger(orders_json)
        return dm.add_store_numbers_to_orders()

    def output_json(self, json_str, filepath, log_message):
        output_filepath = os.path.join('/Users/ekim/workspace/personal/dd-bot/dev/build', filepath)
        json_str_to_file(json_str=json_str, output_filepath=output_filepath, log_message=log_message)

    def convert_to_dataframes(self, orders_with_store_nums):
        orders_json_with_store_nums = get_prettified_and_mapped_orders(orders_with_store_nums, with_store_nums=True)
        self.output_json(orders_json_with_store_nums, 'orders_json_with_store_nums.csv',
                         'Writing orders_json with store_num to stdout...')

        return convert_flattened_orders_to_df(orders_with_store_nums)

    def export_to_excel(self, orders_dfs):
        self.get_excel_output(orders_dfs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)
    md.run_main()