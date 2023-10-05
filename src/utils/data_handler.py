import json
import re
import csv
import logging
import pandas as pd

# todo: C7B1DB1A edge case; turn into oop via order_handler
def clean_order_text(order):
    # Define the patterns in a list
    patterns = [
        re.compile(r'(Rate Dasher|Learn More|Get help).*?(?=Pick Up Location)', re.DOTALL),
        re.compile(r'Channel.*?(?=Order Details)', re.DOTALL),
        re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Delivery)', re.DOTALL),
        re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Pickup)', re.DOTALL)

    ]

    # Remove irrelevant data using regex patterns
    for pattern in patterns:
        order = re.sub(pattern, '', order).strip()

    # Replace newline characters with spaces
    _order = order.replace('\n', ' ')

    return _order


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


def get_mapped_order(order):
    # Define the known keys with their regex patterns
    known_keys = [r'\bOrder: \b', r'\bDelivered\b', r'\bCustomer\sPicked\sUp\b', r'\bCancelled\s-\sNot\sPaid\b',
                  r'\bCancelled\s-\sPaid\b', r'\bPick Up Location\b', r'\bOrder Details\b',
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


# todo: move to separate module
def get_prettified_results(results):
    logging.info(f'Prettifying data...')
    return json.dumps(results, indent=4)

# todo: move to separate module
def get_prettified_and_mapped_orders(raw_orders, with_store_nums=False):
    """
    Takes in a deserialized string (Python object of list of dicts)
    and returns a serialized JSON string.
    """
    results = []

    for order in raw_orders:
        if not with_store_nums:
            order = get_mapped_order(clean_order_text(order))
        results.append(order)

    return get_prettified_results(results)


def get_flatten_order(d, parent_key='', sep='.'):
    order = {}
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            order.update(get_flatten_order(v, new_key, sep=sep))
        else:
            order[new_key] = v
    return order

def get_flattened_orders(orders):
    flattened_orders = []
    for order in orders:
        flattened_order = get_flatten_order(order)
        flattened_orders.append(flattened_order)
    return flattened_orders


def convert_orders_to_dataframes(flattened_orders):
    dfs = []
    for order in flattened_orders:
        s = pd.Series(order)
        df = pd.DataFrame(s)
        dfs.append(df)

    return dfs

def convert_flattened_orders_to_df(orders):
    flattened_orders = get_flattened_orders(orders)
    dfs = convert_orders_to_dataframes(flattened_orders)

    return dfs


# todo: move to separate module
def json_str_to_file(json_str, output_filepath, log_message):
    with open(output_filepath, 'w') as f:
        logging.info(log_message)
        f.write(json_str)