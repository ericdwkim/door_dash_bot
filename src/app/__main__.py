from src.app.drivers import BaseDriver, OrdersPageDriver
import os
import time
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Main:
    def __init__(self, headless=False):
        self.base_driver = BaseDriver(headless=headless)
        self.orders_page_driver = OrdersPageDriver(self.base_driver)



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

    def scrape_orders_data(self):

        try:
            scraped_orders_data = self.orders_page_driver.scrape_orders_data()
            if not scraped_orders_data:
                logging.error('Could not scrape orders data')
                return False, None
            else:
                logging.info('Successfully scraped orders data')
                return True, scraped_orders_data
        except Exception as e:
            logging.exception(f'An error occurred : {e}')
            return False, None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)

    switched_to_history_tab, date_filter_set_to_yesterday = md.switch_to_history_tab_and_set_date_filter_to_yesterday()
    logging.info(
        f'\nswitched_to_history_tab: {switched_to_history_tab}\ndate_filter_set_to_yesterday: {date_filter_set_to_yesterday}')

    # todo: need better bool, list var naming convention; too confusing
    orders_data_scraped, scraped_orders_data = md.scrape_orders_data()
    logging.info(f'orders_data_scraped: {orders_data_scraped}\nscraped_orders_data: {scraped_orders_data}')
