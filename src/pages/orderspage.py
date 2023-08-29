# import time
# import logging
# from src.pages.basepage import BasePage
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# class OrdersPage(BasePage):
#     def __init__(self, driver):
#         super().__init__(driver)
#
#
#     def drill_to_online_reports(self):
#
#         try:
#             is_element_clicked = self.wait_for_find_then_click('//*[@id="Reporting_TreeItem_div"]/td[2]/table/tbody/tr[2]/td[2]/a', locator_type=By.XPATH)
#             if not is_element_clicked:
#                 logging.error(f'Could not switch to Online Reports')
#                 return False
#             else:
#                 return True
#
#         except Exception as e:
#             logging.exception(f'An error occurred trying to drill into Online Reports: {e}')
#             return False
#
