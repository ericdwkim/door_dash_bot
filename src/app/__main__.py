from src.app.drivers import BaseDriver
import os
import argparse
import logging

class Main:
    def __init__(self, headless=False):
        # @dev: subclass drivers have and use base_driver
        self.base_driver = BaseDriver(headless=headless)
        self.login_page_driver = LoginPageDriver(self.base_driver)
        # self.home_page_driver = HomePageDriver(self.base_driver)
        # self.online_reports_driver = OnlineReportsPageDriver(self.base_driver)

    def launch_and_login_to_door_dash(self):
        login_to_cash = self.login_page_driver.visit_and_login()
        if not login_to_cash:
            logging.error('Could not login_page_driver.launch_and_login_to_door_dash')
            return False
        else:
            logging.info('Successfully launched and logged into Door Dash.')
            return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DoorDash Bot V1')
    parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
    args = parser.parse_args()

    md = Main(headless=args.headless)

    md.wrapper()



