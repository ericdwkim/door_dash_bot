from src.app.drivers import BaseDriver, LoginPageDriver, HomePageDriver
import os
import argparse
import logging

class Main:
    def __init__(self, headless=False):
        # @dev: subclass drivers have and use base_driver
        self.base_driver = BaseDriver(headless=headless)
        self.login_page_driver = LoginPageDriver(self.base_driver)
        self.home_page_driver = HomePageDriver(self.base_driver)
        # self.online_reports_driver = OnlineReportsPageDriver(self.base_driver)

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


    def wrapper(self):
        try:
            launched_and_logged_into_door_dash_homepage = self.launch_and_login_to_door_dash()
            if not launched_and_logged_into_door_dash_homepage:
                logging.error('Could not launch_and_login_to_door_dash')
            switched_to_orders_page = self.switch_to_orders_page()
            if not switched_to_orders_page:
                loggging.error('Could not switch_to_orders_page in wrapper')
        except Exception as e:
            logging.exception(f'An error occurred attempting to launch, login, and switch from home to orders page: {e}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)

    md.wrapper()



