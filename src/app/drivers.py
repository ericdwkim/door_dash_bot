import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class BaseDriver:

    def __init__(self, headless=False):
        logging.info('Initializing BaseDriver...')
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        else:
            options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(service=Service(), options=options)

    def teardown_driver(self):
        self.driver.quit()
