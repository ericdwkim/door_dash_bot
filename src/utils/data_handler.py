import json
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


def get_prettified_results(results):
    return json.dumps(results, indent=4)


def get_prettified_and_mapped_orders(orders):
    
    results = []
    
    for order in orders:
        
        order_cleaned = clean_order_text(order)

        mapped_order = get_mapped_order(order_cleaned)

        results.append(mapped_order)


    prettified_results = get_prettified_results(results)

    return prettified_results

        
        
    
    