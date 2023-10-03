import pandas as pd
import re
import json
import csv
from datetime import datetime


class DataMerger:
    # def __init__(self, orders): # prod; pass in orders list of dicts to alter (add store number k/v in each dict) in mem
    def __init__(self):
        self.master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'
        self.json_output_filepath = '/Users/ekim/workspace/personal/dd-bot/dev/build/orders_json.csv'  # testing purposes only from disk
        self.orders = orders  # prod ; from mem (equivalen tto json_output_filepath)
        self.master_df = None
        self.order_to_location_df = None
        self.merged_df = None

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

    #todo: disable when done testing
    def read_orders(self):
        with open(self.json_output_filepath, 'r') as f:
            orders = json.load(f)
        return orders

    # todo: change to self.orders and remove param when done testing
    def order_id_to_pickup_location(self, orders):
        order_id_to_pickup_location = {}
        for order in orders:
            order_id = order['Order']
            store_addrs = order['Pick Up Location']
            order_id_to_pickup_location[order_id] = store_addrs
        return order_id_to_pickup_location

    def get_raw_order_to_location_df(self):
        orders = self.read_orders()
        raw_orders_to_location = self.order_id_to_pickup_location(orders)
        order_to_location_pairs = list(raw_orders_to_location.items())
        self.order_to_location_df = pd.DataFrame(order_to_location_pairs, columns=['order_id', 'pickup_location'])

    def splitup_pickup_location(self):
        # Remove all commas
        self.order_to_location_df['pickup_location'] = self.order_to_location_df['pickup_location'].str.replace(',', '')

        # Remove "USA" substring
        self.order_to_location_df['pickup_location'] = self.order_to_location_df['pickup_location'].str.replace('USA', '')

        pattern = r'(?P<address>^.+?)\s(?P<city>\w+\s*\w*)\s(?P<state>[A-Z]{2})\s(?P<zip_code>\d{5})'
        df_extracted = self.order_to_location_df['pickup_location'].str.extract(pattern)

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

    def get_order_id_to_site_num_from_merged_df(self):
        order_id_to_site_num = self.merged_df.set_index('order_id')['Site #'].to_dict()
        print(f'*****************************************\n{order_id_to_site_num}\n*****************************************')


    def get_order_id_to_site_num(self):
        self.get_merged_df()
        self.get_order_id_to_site_num_from_merged_df()

    # todo: change to self.orders when done testing
    def add_store_numbers_to_orders(self):
        order_id_to_site_name = self.get_order_id_to_site_num()

        # loop through orders
        orders = self.read_orders()
        for order in orders:
            order_id = order.get('Order')
            if order_id in order_id_to_site_name:
                store_num = order_id_to_site_name[order_id]
                order['Store Number'] = store_num
            else:
                order['Store Number'] = 'N/A'

