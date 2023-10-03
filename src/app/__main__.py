from src.app.drivers import BaseDriver, OrdersPageDriver
import os
import time
import argparse
import pandas as pd
from datetime import datetime
import logging
from src.utils.data_handler import get_prettified_and_mapped_orders, convert_flattened_orders_to_df, json_str_to_csv
from src.utils.data_merger import DataMerger
from src.utils.excel_formatter import ExcelFormatter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Main:
    def __init__(self, headless=False):
        self.base_driver = BaseDriver(headless=headless)
        self.orders_page_driver = OrdersPageDriver(self.base_driver)
        self.today = datetime.today().strftime('%m.%d.%y')
        self.excel_file_name = f'DD {self.today}.xlsx'



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
        """

        :return: Tuple(bool, bool)
        """
        try:

            switched_to_history_tab = self.switch_to_history_tab()
            if not switched_to_history_tab:
                logging.error('Could not switch_to_history_tab in switch_to_history_tab_and_set_date_filter_to_yesterday')
                return False, False

            date_filter_set_to_yesterday = self.set_date_filter_to_yesterday()
            if not date_filter_set_to_yesterday:
                logging.error('Could not set_date_filter_to_yesterday in switch_to_history_tab_and_set_date_filter_to_yesterday')
                return True, False

            if switched_to_history_tab and date_filter_set_to_yesterday:
                logging.info(f'Successfully switched_to_history_tab and date_filter_set_to_yesterday')
                return True, True

        except Exception as e:
            logging.exception(f'An error occurred attempting to switch_to_history_tab_and_set_date_filter_to_yesterday {e}')
            return False, False

    def get_orders(self):

        try:
            orders = self.orders_page_driver.get_orders()
            if not orders:
                logging.error('Could not scrape orders data')
                return None
            else:
                # logging.info('Successfully scraped orders data')
                return orders
        except Exception as e:
            logging.exception(f'An error occurred : {e}')
            return None

    def get_excel_output(self, orders_dfs):
        with pd.ExcelWriter(self.excel_file_name, engine='xlsxwriter') as writer:
            for idx, df in enumerate(orders_dfs):
                sheet_name = f'sheetname'
                df.to_excel(writer, sheet_name, header=False, index=True)

                formatter = ExcelFormatter(writer, sheet_name, df)
                formatter.apply_sheet_formats()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)

    switched_to_history_tab, date_filter_set_to_yesterday = md.switch_to_history_tab_and_set_date_filter_to_yesterday()
    logging.info(
        f'\nswitched_to_history_tab: {switched_to_history_tab}\ndate_filter_set_to_yesterday: {date_filter_set_to_yesterday}')

    orders = md.get_orders()
    # logging.info(f'\n***********************************\n {orders} \n********************************\n')

    orders_json = get_prettified_and_mapped_orders(orders)
    # stdout as csv; will be good to have for debugging purposes
    json_str_to_csv(orders_json)

    # create orders dfs
    orders_dfs = convert_flattened_orders_to_df(orders)

    md.get_excel_output(orders_dfs)

    # write_json_to_csv(orders_json)
    logging.info(f'\n***********************************\n {orders_json} \n********************************\n')


    # data_merger = DataMerger()
    # data_merger.add_store_numbers_to_orders()