from drivers import BaseDriver
import os
import argparse
import logging

driver = BaseDriver()
# logging.info(f'driver: {driver}')


dd_url = os.getenv('DD_MERCHANT_LOGIN_URL')
driver.get(dd_url)


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='DoorDash Bot V1')
#     parser.add_argument('--headless', required=False, action='store_true', help='Run in headless mode')
