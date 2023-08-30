from src.app.drivers import BaseDriver, LoginPageDriver, HomePageDriver, OrdersPageDriver
import os
import time
import argparse
import logging

class Main:
    def __init__(self, headless=False):
        # @dev: subclass drivers have and use base_driver
        self.base_driver = BaseDriver(headless=headless)
        self.login_page_driver = LoginPageDriver(self.base_driver)
        self.home_page_driver = HomePageDriver(self.base_driver)
        self.orders_page_driver = OrdersPageDriver(self.base_driver)

    def launch_and_login_to_door_dash(self):
        login_to_dash = self.login_page_driver.visit_and_login()
        if not login_to_dash:
            logging.error('Could not login_page_driver.launch_and_login_to_door_dash')
            return False
        else:
            logging.info('Successfully launched and logged into Door Dash.')
            return True

    def switch_to_orders_page(self):
        switched_to_orders_page = self.home_page_driver.switch_to_orders_page()
        if not switched_to_orders_page:
            logging.error('Could not switch_to_orders_page')
            return False
        else:
            logging.info('Successfully switched to orders page from homepage')
            return True

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


    def wrapper(self):
        """

        :return: Tuple(bool, bool, bool)
        """
        try:
            launched_and_logged_into_door_dash_homepage = self.launch_and_login_to_door_dash()
            if not launched_and_logged_into_door_dash_homepage:
                logging.error('Could not launch_and_login_to_door_dash')
                return False, False, False, False
            switched_to_orders_page = self.switch_to_orders_page()
            if not switched_to_orders_page:
                logging.error('Could not switch_to_orders_page in wrapper')
                return True, False, False, False
            # wait for ui to load dom prior to switching tabs
            switched_to_history_tab = self.switch_to_history_tab()
            if not switched_to_history_tab:
                logging.error('Could not switch_to_history_tab in wrapper')
                return True, True, False, False
            date_filter_set_to_yesterday = self.set_date_filter_to_yesterday()
            time.sleep(30000)
            if not date_filter_set_to_yesterday:
                logging.error('Could not set_date_filter_to_yesterday in wrapper')
                return True, True, True, False
            if launched_and_logged_into_door_dash_homepage and switched_to_orders_page and switched_to_history_tab and date_filter_set_to_yesterday:
                logging.error('Successfully wrapped!')
                return True, True, True, True
        except Exception as e:
            logging.exception(f'An error occurred attempting to 1) launch & login 2) switch from home to orders page 3) switch to history tab: {e}')
            return False, False, False, False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)

    md.wrapper()



