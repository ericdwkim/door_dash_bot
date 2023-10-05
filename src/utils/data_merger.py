import pandas as pd
import re
import json
import csv
from datetime import datetime
import logging

class DataMerger:
    def __init__(self, orders):
        self.master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'
        self.orders = orders
        self.master_df = None
        self.order_to_location_df = None
        self.merged_df = None
        self.store_num_to_order_ids = {}

    # `orders` passed into constructor of DataMerger cls is a serialized json string
    def deserialize_orders(self):
        self.orders = json.loads(self.orders)

    def read_masterdataset_excel(self):
        self.master_df = pd.read_excel(self.master_dataset_file_path, index_col=0)

    def add_cols_to_masterset_df(self):
        # Create pattern for street_num col
        street_num_pattern = r'(?P<street_num>\b\d{3,5}\b)'
        street_num_df = self.master_df['Address'].str.extract(street_num_pattern)

        # Add street_num col to df
        self.master_df = pd.concat([self.master_df, street_num_df], axis=1)

        # Cast int64 default dtype cols to strings for proper JOINs
        self.master_df['Site #'] = self.master_df['Site #'].astype(str)
        self.master_df['Zip'] = self.master_df['Zip'].astype(str)
        self.master_df['street_num'] = self.master_df['street_num'].astype(str)

    def get_masterdataset_df(self):
        self.read_masterdataset_excel()
        self.add_cols_to_masterset_df()


    def remove_incomplete_orders(self):
        """
        prevents incomplete order dicts from causing NoneType errors when accessing specific fields
        :param orders:
        :return:
        """
        complete_orders = []

        for order in self.orders:
            # @dev: mainly to help catch potential de/serialization issues
            # todo: this needs to be much cleaner/robust for other edge cases, such as if len(order) is b/w 2 - 6
            if len(order) <= 1:
                logging.error(f'Deserialization did not work properly. Please confirm proper dtype of `orders` instance')
            if len(order) >= 7:  # presumes a complete order to have at least 7 keys as brief testing showed 8 - 10 with avg being ~10
                complete_orders.append(order)

        self.orders = complete_orders


    def order_id_to_pickup_location(self):
        order_id_to_pickup_location = {}
        for order in self.orders:
            order_id = order['Order']
            store_addrs = order['Pick Up Location']
            order_id_to_pickup_location[order_id] = store_addrs
        return order_id_to_pickup_location

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

        # Loop over each row to process
        for pickup_location in self.order_to_location_df['pickup_location']:
            parts = pickup_location.split(" ")
            zip_code = parts[-1]
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

    def add_street_num_col(self):
        street_num_pattern = r'(?P<street_num>\b\d{3,5}\b)'

        addrs_extracted_df = self.order_to_location_df['address'].str.extract(street_num_pattern)

        self.order_to_location_df = pd.concat([self.order_to_location_df, addrs_extracted_df], axis=1)

    def get_order_to_location_df(self):
        self.get_raw_order_to_location_df()
        self.splitup_pickup_location()
        self.add_street_num_col()

    def get_merged_and_organized_master_df(self):
        self.merged_df = pd.merge(self.master_df, self.order_to_location_df, left_on=['Zip', 'street_num'], right_on=['zip_code', 'street_num'], how='inner')

        self.merged_df.drop(['Site Description', 'City', 'County', 'State', 'address', 'city', 'state', 'Zip', 'zip_code', 'Notes',
         'street_num'], axis=1, inplace=True)

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