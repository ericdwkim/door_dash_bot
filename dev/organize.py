from orders import orders
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import pandas as pd
import re
import json
import csv



def clean_order_text(order):
    # Define the patterns in a list
    patterns = [
        re.compile(r'(Rate Dasher|Learn More|Get help).*?(?=Pick Up Location)', re.DOTALL),
        re.compile(r'Channel.*?(?=Order Details)', re.DOTALL),
        re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Delivery)', re.DOTALL),
        re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Pickup)', re.DOTALL)

    ]

    # Apply each pattern
    for pattern in patterns:
        order = re.sub(pattern, '', order).strip()

    # Replace newline characters with spaces
    order = order.replace('\n', ' ')

    return order



def parse_menu_items(price_as_value):
    # Initialize a dictionary for the nested order details
    item_name_to_item_price = {}

    # Regular expression pattern to match an item and its corresponding price
    pattern = re.compile(r'(.+?) (\$\d+\.\d+)')

    # Find all matches in the string
    matches = pattern.findall(price_as_value)

    # Loop through all the matches and populate the dictionary
    for item_name, item_price in matches:
        item_name_to_item_price[item_name] = item_price

    return item_name_to_item_price


def parse_order(order):
    # Define the known keys with their regex patterns
    known_keys = [r'\bOrder: \b', r'\bDelivered\b', r'\bCustomer\sPicked\sUp\b', r'\bCancelled\s-\sNot\sPaid\b', r'\bCancelled\s-\sPaid\b', r'\bPick Up Location\b', r'\bOrder Details\b',
                  r'\bSubtotal\b(?=\s[^a-zA-Z])', r'\bSubtotal\sTax\b', r'Commission \(\d+%\)',
                  r'\bTotal Customer Refund\b', r'\bEstimated Payout\b', r'\bAssociated Transactions \(\d+%\)',
                  r'Transaction #\d+ - Delivery']

    # Initialize the dictionary to store our parsed values
    order_dict = {}

    # Find positions of known keys
    positions = []
    for key in known_keys:
        for m in re.finditer(key, order):
            positions.append((m.start(), m.end(), m.group()))

    # Sort positions by their start index
    positions.sort(key=lambda x: x[0])
    # print(positions)

    # Create segments based on positions
    segments = []

    for i in range(len(positions)):
        start = positions[i][1]
        end = positions[i + 1][0] if i + 1 < len(positions) else len(order)
        key = positions[i][2]
        value = order[start:end].strip().split(' ')[0] if 'Estimated Payout' in key else order[start:end].strip()
        segments.append((key, value))

    # Parse segments into dictionary
    for key, value in segments:
        if key == "Order Details":
            value = parse_menu_items(value)
        order_dict[key.replace(':', '').strip()] = value

    return order_dict


def main_looper_func(orders):

    results = []

    for order in orders:
        # 1. Get order strings squeaky clean!
        order_cleaned = clean_order_text(order)

        # 2. Parse each cleaned order string into formatted key/value pairs
        parsed_order = parse_order(order_cleaned)

        results.append(parsed_order)

    return results



results = main_looper_func(orders)

# print(results)

def prettify_list_of_dicts(list_of_dicts):
    return json.dumps(list_of_dicts, indent=4)


print(prettify_list_of_dicts(results))
# ---------------------------------------------------------------------
import time
from selenium.webdriver.common.by import By
import logging


def wait_for_element(locator, locator_type=By.XPATH, timeout=10):
    # Implement the actual wait logic here
    found, elem = wait_for_and_find_element(locator, locator_type, timeout)
    return found, elem


def find_and_click_exit_button():
    exit_btn_clicked = find_element_and_click(
        locator='//*[@id="MerchantApp"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/nav/div[1]/div[1]/div/button',
        locator_type=By.XPATH)
    return exit_btn_clicked


def process_row(table_row, orders):
    table_row.click()
    time.sleep(5)  # wait for ssb to load on dom

    found, elem = wait_for_element("//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']")

    if found:
        start_length = len(orders)
        orders.append(elem.text)
        end_length = len(orders)

        if end_length > start_length:
            exit_btn_clicked = find_and_click_exit_button()

            if exit_btn_clicked:
                logging.info(f'Exiting sidesheetbody for Order #: {len(orders)}')
                return True
    return False


def iterate_table_rows(table_rows, orders):
    idx = 1
    while idx < len(table_rows):
        table_row = table_rows[idx]

        if process_row(table_row, orders):
            idx += 1
        else:
            logging.error(f"Failed to process Order #: {idx}")


def orders_scraper_wrapper():
    orders = []
    table_rows = get_table_rows_somehow()  # Implement this function to get table rows

    iterate_table_rows(table_rows, orders)

    return orders