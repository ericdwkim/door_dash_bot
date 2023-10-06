import pandas as pd
import re
import json
import csv
from datetime import datetime
import logging

class DataMerger:
    def __init__(self, orders_json):
        self.master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'
        self.orders = orders_json
        self.master_df = None
        self.order_to_location_df = None
        self.merged_df = None
        self.store_num_to_order_ids = {}

    # `orders` passed into constructor of DataMerger cls is a serialized json string
    def deserialize_orders(self):
        self.orders = json.loads(self.orders)

    def read_masterdataset_excel(self):
        self.master_df = pd.read_excel(self.master_dataset_file_path, index_col=0)

    def cast_int_to_str(self):

        # Cast int64 default dtype cols to strings for proper JOINs
        self.master_df['Site #'] = self.master_df['Site #'].astype(str)
        self.master_df['Zip'] = self.master_df['Zip'].astype(str)

    def get_masterdataset_df(self):
        self.read_masterdataset_excel()
        self.cast_int_to_str()

    def is_order_complete(self, order):
        """
        Check if the order is complete based on the number of keys.
        :param order: Dictionary representing an order
        :return: Boolean indicating if the order is complete
        """
        MIN_KEYS = 7  # Minimum keys required for an order to be complete

        if not isinstance(order, dict):
            logging.error(f"Order is not a dictionary: {order}. Deserialization issue suspected.")
            return False

        if len(order) < MIN_KEYS:
            logging.warning(f"Incomplete order detected. Order has fewer than {MIN_KEYS} keys: {order}")
            return False

        # Additional validation checks can be added here if needed
        return True

    def remove_incomplete_orders(self):
        """
        Remove incomplete orders to prevent errors when accessing specific fields.
        """
        complete_orders = [order for order in self.orders if self.is_order_complete(order)]

        if not complete_orders:
            logging.error("No complete orders found. Setting self.orders to an empty list.")

        self.orders = complete_orders

    def validate_and_clean_order_id(self, order):
        if 'Order' not in order:
            logging.error(f' Missing "Order" key in the order dictionary: {order}')
            return None

        order_id = order['Order']
        if len(order_id) > 8:
            logging.warning(f' OrderID is too long. Truncating OrderID to 8 characters...')
            return order_id[:8]
        elif len(order_id) == 0:
            logging.error(f' OrderID is missing. Please evaluate the order: \n{order}')
            return None
        else:
            return order_id

    def validate_and_clean_store_addrs(self, order):
        if 'Pick Up Location' not in order:
            logging.error(f' Missing "Pick Up Location" key in the order dictionary: {order}')
            return None

        store_addrs = order['Pick Up Location']
        if len(store_addrs) == 0:
            logging.warning(f' Pick Up location is missing from Order. Adding placeholder...')
            store_addrs = '000 Placeholder Address'
        return store_addrs

    def order_id_to_pickup_location(self):
        order_id_to_pickup_location_map = {}
        if not self.orders:
            logging.error(' orders_json is empty or None. Please provide a valid orders_json.')
            return None

        for order in self.orders:
            order_id = validate_and_clean_order_id(order)
            if order_id is None:
                continue

            store_addrs = validate_and_clean_store_addrs(order)
            if store_addrs is None:
                continue

            order_id_to_pickup_location_map[order_id] = store_addrs

        if not order_id_to_pickup_location_map:
            logging.error(' No valid orders found. Returning None.')
            return None

        return order_id_to_pickup_location_map

    def get_raw_order_to_location_df(self):
        self.deserialize_orders()
        self.remove_incomplete_orders()
        order_id_to_pickup_location = self.order_id_to_pickup_location()
        order_to_location_pairs = list(order_id_to_pickup_location.items())
        self.order_to_location_df = pd.DataFrame(order_to_location_pairs, columns=['order_id', 'pickup_location'])

    def splitup_pickup_location(self):
        # Preprocess the city names to remove duplicates and convert to set for quick lookup
        unique_cities = set(self.master_df['City'].dropna().unique())

        # Remove commas and 'USA' substring
        self.order_to_location_df['pickup_location'] = self.order_to_location_df['pickup_location'].str.replace(',', '')
        self.order_to_location_df['pickup_location'] = self.order_to_location_df['pickup_location'].str.replace(' USA', '')

        # Initialize lists to hold the extracted parts of the pickup location
        address_list = []
        city_list = []
        state_list = []
        zip_code_list = []

        logging.info(f'\n******************************\n {self.order_to_location_df} \n******************\n')

        # Loop over each row to process
        for pickup_location in self.order_to_location_df['pickup_location']:
            parts = pickup_location.split(" ")
            logging.info(f' \n************************ parts:\n {parts} \n************************\n')
            # logging.info(f' \n************************ length(parts):\n {len(parts)} \n************************\n')
            zip_code = parts[-1]
            logging.info(f' \n************************ zip_code:\n {zip_code} \n************************\n')
            state = parts[-2]


            # Initialize variables to hold potential matches
            longest_city_match = ""

            # Loop over unique cities to find the longest matching city name in the string
            for city in unique_cities:
                if city in pickup_location:
                    if len(city) > len(longest_city_match):
                        longest_city_match = city

            # If a city match is found, then get the address part
            if longest_city_match:
                start_idx = pickup_location.index(longest_city_match)
                address = pickup_location[:start_idx].strip()
            else:
                address = "Unmatched"
                longest_city_match = "Unmatched"

            # Append the extracted data to the lists
            address_list.append(address)
            city_list.append(longest_city_match)
            state_list.append(state)
            zip_code_list.append(zip_code)

        # Create a DataFrame with the lists
        df_extracted = pd.DataFrame({
            'address': address_list,
            'city': city_list,
            'state': state_list,
            'zip_code': zip_code_list
        })

        # Concatenate the extracted DataFrame to the original DataFrame
        self.order_to_location_df = pd.concat([self.order_to_location_df, df_extracted], axis=1)

    def get_order_to_location_df(self):
        self.get_raw_order_to_location_df()
        self.splitup_pickup_location()

    def get_merged_and_organized_master_df(self):
        self.merged_df = pd.merge(self.master_df, self.order_to_location_df, left_on=['Zip'], right_on=['zip_code'], how='inner')

        self.merged_df.drop(['Site Description', 'City', 'County', 'State', 'address', 'city', 'state', 'Zip', 'zip_code', 'Notes'], axis=1, inplace=True)

        self.merged_df = self.merged_df[['Site #', 'order_id', 'Address', 'pickup_location']]


    def get_merged_df(self):
        self.get_masterdataset_df()
        self.get_order_to_location_df()
        self.get_merged_and_organized_master_df()

    # TODO: (feat) instead of going from `order_id: store_num` first from the merged_df , just groupby store_num df col along with address and pickup_location df cols; essentially skip this extra pythonic step of having a mapping to then convert to another mapping; def can do it with the df objects themselves; would be more efficient

    def _get_store_num_to_order_ids(self, order_id_to_store_num):
        """
        groupby `storenum: {order_ids}`
        :return:
        """

        for order_id, store_num in order_id_to_store_num.items():
            if store_num not in self.store_num_to_order_ids:
                self.store_num_to_order_ids[store_num] = set()
            self.store_num_to_order_ids[store_num].add(order_id)

    def get_store_num_to_order_ids_from_merged_df(self):
        order_id_to_store_num = self.merged_df.set_index('order_id')['Site #'].to_dict()
        self._get_store_num_to_order_ids(order_id_to_store_num)

    def get_store_num_to_order_ids(self):
        self.get_merged_df()
        self.get_store_num_to_order_ids_from_merged_df()

    def add_store_numbers_to_orders(self):
        self.get_store_num_to_order_ids()  # calls and gives access to changed mapping instance from order_id:store_num --> store_num: {order_ids}

        for order in self.orders:
            order_id = order.get('Order')
            found = False # var to keep track if order_id was found in set or not

            for store_num, order_id_set in self.store_num_to_order_ids.items():
                if order_id in order_id_set:
                    order['Store Number'] = store_num
                    found = True
                    break  # exit loop if order_id is found
            if not found:
                order['Store Number'] = 'NaN'
        orders_with_store_nums = self.orders
        return orders_with_store_nums