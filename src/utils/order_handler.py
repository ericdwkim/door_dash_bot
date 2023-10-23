import json, re, logging
import pandas as pd


class OrderHandler:
    def __init__(self):
        self.known_keys = [
                            r'\bOrder:',
                            r'\bDelivered\b',
                            r'Could Not Deliver\b',
                            r'\bCustomer Picked Up\b',
                            r'\bCancelled - Not Paid\b',
                            r'\bCancelled - Paid\b',
                            r'\bPick Up Location\b',
                            r'\bOrder Details\b',
                            r'\bSubtotal\b(?=\s[^a-zA-Z])',
                            r'\bSubtotal Tax\b',
                            r'Commission \(\d+%\)',
                            r'\bTotal Customer Refund\b',
                            r'\bEstimated Payout\b',
                            r'\bAssociated Transactions \(\d+%\)',
                            r'Transaction #\d+ - Delivery'
                        ]

    @staticmethod
    def clean_order_text(order):
        patterns = [re.compile(r'(Rate Dasher|Learn More|Get help).*?(?=Pick Up Location)', re.DOTALL),
                    re.compile(r'Channel.*?(?=Order Details)', re.DOTALL),
                    re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Delivery)', re.DOTALL),
                    re.compile(r'Associated Transactions \(\d+\).*?(?=Transaction #\d+ - Pickup)', re.DOTALL)]
        for pattern in patterns:
            order = re.sub(pattern, '', order).strip()
        return order.replace('\n', ' ')

    @staticmethod
    def parse_menu_items(price_as_value):
        item_name_to_item_price = {}
        pattern = re.compile(r'(.+?) (\$\d+\.\d+)')
        matches = pattern.findall(price_as_value)
        for item_name, item_price in matches:
            item_name_to_item_price[item_name] = item_price
        return item_name_to_item_price

    def get_mapped_order(self, order):
        order_dict = {}
        positions = []
        for key in self.known_keys:
            for m in re.finditer(key, order):
                positions.append((m.start(), m.end(), m.group()))
        positions.sort(key=lambda x: x[0])

        segments = []
        for i in range(len(positions)):
            start = positions[i][1]
            end = positions[i + 1][0] if i + 1 < len(positions) else len(order)
            key = positions[i][2]
            value = order[start:end].strip().split(' ')[0] if 'Estimated Payout' in key else order[start:end].strip()
            segments.append((key, value))

        for key, value in segments:
            if key == "Order Details":
                value = self.parse_menu_items(value)
            order_dict[key.replace(':', '').strip()] = value

        return order_dict

    @staticmethod
    def get_prettified_results(results):
        logging.info(f'Prettifying data...')
        return json.dumps(results, indent=4)

    def get_prettified_and_mapped_orders(self, orders, is_raw):
        results = []
        for order in orders:
            if is_raw:
                order = self.get_mapped_order(self.clean_order_text(order))
            results.append(order)
        return self.get_prettified_results(results)

    @staticmethod
    def get_flatten_order(d, parent_key='', sep='.'):
        order = {}
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                order.update(OrderHandler.get_flatten_order(v, new_key, sep=sep))
            else:
                order[new_key] = v
        return order

    def get_flattened_orders(self, orders):
        return [self.get_flatten_order(order) for order in orders]

    def convert_orders_to_dataframes(self, flattened_orders):
        return [pd.DataFrame(pd.Series(order)) for order in flattened_orders]

    def convert_flattened_orders_to_df(self, orders):
        flattened_orders = self.get_flattened_orders(orders)
        return self.convert_orders_to_dataframes(flattened_orders)

    def json_str_to_file(self, json_str, output_filepath, log_message):
        with open(output_filepath, 'w') as f:
            logging.info(log_message)
            f.write(json_str)