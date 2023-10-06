import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ..pages.orderspage import OrdersPage


class BaseDriver:
    def __init__(self, headless=False):
        self.headless = headless
        self.os_type = platform.system()
        self.setup_driver()

    def setup_driver(self):
        print('Initializing BaseDriver...')
        # logging.info('Initializing BaseDriver...')
        options = self._get_chrome_options()
        chromedriver_executable_path = self._get_chromedriver_executable_path()

        self.driver = webdriver.Chrome(
            service=Service(executable_path=chromedriver_executable_path),
            options=options
        )

        # logging.info(
        #     f'Using operating system: "{self.os_type}".\nConstructing chromedriver instance using executable_path: "{chromedriver_executable_path}"'
        # )

        print(
            f'Using operating system: "{self.os_type}".\nConstructing chromedriver instance using executable_path: "{chromedriver_executable_path}"'
        )

    def _get_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        if self.headless:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--start-maximized')
        return options

    def _get_chromedriver_executable_path(self):
        return '/opt/homebrew/bin/chromedriver' if self.os_type == 'Darwin' else 'C:\\Users\\ekima\\AppData\\Local\\anaconda3\\envs\\bots\\Lib\\site-packages\\seleniumbase\\drivers\\chromedriver.exe'

    def teardown_driver(self):
        self.driver.quit()

class OrdersPageDriver:

    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.orders_page = OrdersPage(self.base_driver)


    def switch_to_history_tab(self):
        try:
            switch_to_history_tab = self.orders_page.switch_to_history_tab()
            if not switch_to_history_tab:
                logging.error('Could not orders_page.switch_to_history_Tab')
                return False
            else:
                logging.info('Successfully orders_page.switch_to_history_tab')
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to orders_page.switch_to_history_tab: {e}')

    def set_date_filter_to_yesterday(self):
        try:
            set_date_filter_to_yesterday = self.orders_page.set_date_filter_to_yesterday()
            if not set_date_filter_to_yesterday:
                logging.error('Could not orders_page.set_date_filter_to_yesterday')
                return False
            else:
                logging.info('Successfully orders_page.set_date_filter_to_yesterday')
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to orders_page.set_date_filter_to_yesterday: {e}')


    def get_orders(self):
        try:
            orders = self.orders_page.get_orders()
            if not orders:
                logging.error('Could not orders_page.scrape_orders_table_data')
                return None
            else:
                # logging.info('Successfully orders_page.get_orders')
                return orders
        except Exception as e:
            logging.exception(f'An error occurred trying to orders_page.scrape_orders_table_data: {e}')
            return None

