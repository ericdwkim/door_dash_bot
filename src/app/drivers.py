import logging
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from ..pages.loginpage import LoginPage
from ..pages.homepage import HomePage
# from ..pages.onlinereportspage import OnlineReportsPage
# from ..pages.dailysummaryascii import DailySummaryASCIIPage


class BaseDriver:
    def __init__(self, headless=False):
        self.headless = headless
        self.setup_driver()

    def setup_driver(self):
        logging.info('Initializing BaseDriver...')
        options = self._get_chrome_options()
        os_type = platform.system()
        chromedriver_executable_path = self._get_chromedriver_executable_path(os_type)

        self.driver = webdriver.Chrome(
            service=Service(executable_path=chromedriver_executable_path),
            options=options
        )

        logging.info(
            f'Using operating system: "{os_type}".\nConstructing chromedriver instance using executable_path: "{chromedriver_executable_path}"'
        )

    def _get_chrome_options(self):
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--start-maximized')
        return options

    def _get_chromedriver_executable_path(self, os_type):
        return '/opt/homebrew/bin/chromedriver' if os_type == 'Darwin' else 'C:\\Users\\ekima\\AppData\\Local\\anaconda3\\envs\\bots\\Lib\\site-packages\\seleniumbase\\drivers\\chromedriver.exe'

    def teardown_driver(self):
        self.driver.quit()

class LoginPageDriver:
    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.login_page = LoginPage(self.base_driver)


    def visit_and_login(self):
        try:
            visit_and_login = self.login_page.visit_and_login()
            if not visit_and_login:
                return False
            else:
                return True
        except Exception as e:
            print(f'An error occurred trying to visit_and_login: {e}')

class HomePageDriver:

    def __init__(self, base_driver):
        self.base_driver = base_driver
        self.home_page = HomePage(self.base_driver)

    def switch_to_orders_page(self):
        try:
            switch_to_orders_page = self.home_page.switch_to_orders_page()
            if not switch_to_orders_page:
                logging.error('Could not home_page.switch_to_orders_page')
                return False
            else:
                return True
        except Exception as e:
            logging.exception(f'An error occurred trying to switch_to_orders_page: {e}')

