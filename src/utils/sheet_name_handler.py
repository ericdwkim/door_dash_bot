import pandas as pd
import re
import json
import csv
from datetime import datetime

master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'

json_output_filepath = '/Users/ekim/workspace/personal/dd-bot/dev/json.csv'

# excel --> dataframe
def read_masterdataset_excel(file_path):
    return pd.read_excel(file_path, index_col=0)


def add_cols_to_masterset_df(master_df):

    # Create pattern for street_num col
    street_num_pattern = r'(?P<street_num>\b\d{3,5}\b)'
    street_num_df = master_df['Address'].str.extract(street_num_pattern)

    # Add street_num col to df
    master_df = pd.concat([master_df, street_num_df], axis=1)

    # Cast int64 default dtype cols to strings for proper JOINs
    master_df['Site #'] = master_df['Site #'].astype(str)
    master_df['Zip'] = master_df['Zip'].astype(str)
    master_df['street_num'] = master_df['street_num'].astype(str)

    return master_df

def get_masterdataset_df(file_path):
    raw_master_df = read_masterdataset_excel(file_path)
    master_df = add_cols_to_masterset_df(raw_master_df)
    return master_df

# list of json orders --> order_id : pickup_location --> dataframe
def read_orders(file_path):
    with open(file_path, 'r') as f:
        orders = json.load(f)

    return orders

def order_id_to_pickup_location(orders):
    order_id_to_pickup_location  = {}
    for order in orders:
        order_id = order['Order']
        store_addrs = order['Pick Up Location']
        order_id_to_pickup_location[order_id] = store_addrs
    return order_id_to_pickup_location

def get_raw_order_to_location_df(file_path):

    orders = read_orders(file_path)
    raw_orders_to_location = order_id_to_pickup_location(orders)

    order_to_location_pairs = list(raw_orders_to_location.items())

    raw_orders_to_location = pd.DataFrame(order_to_location_pairs, columns=['order_id', 'pickup_location'])

    return raw_orders_to_location


def splitup_pickup_location(df):
    pattern = r'(?P<address>^.+?)\s(?P<city>\w+\s*\w*)\s(?P<state>[A-Z]{2})\s(?P<zip_code>\d{5})'

    df_extracted = df['pickup_location'].str.extract(pattern)

    order_to_split_pickup_location_df = pd.concat([df, df_extracted], axis=1)
    return order_to_split_pickup_location_df


def add_street_num_col(df):
    street_num_pattern = r'(?P<street_num>\b\d{3,5}\b)'

    addrs_extracted_df = df['address'].str.extract(street_num_pattern)

    order_to_split_pickup_location_and_street_num_df = pd.concat([df, addrs_extracted_df], axis=1)

    return order_to_split_pickup_location_and_street_num_df


# internal wrapper func
def _get_order_to_location_df(raw_df):
    order_to_location_df = splitup_pickup_location(raw_df)

    order_to_location_df = add_street_num_col(order_to_location_df)

    return order_to_location_df

# main wrapper func
def get_order_to_location_df(file_path):
    raw_orders_to_location = get_raw_order_to_location_df(file_path)

    order_to_location_df = _get_order_to_location_df(raw_orders_to_location)

    return order_to_location_df


def get_merged_and_organized_master_df(master_df, df2):

    # inner join on fields
    merged_df = pd.merge(master_df, df2, left_on=['Zip', 'street_num'], right_on=['zip_code', 'street_num'], how='inner')

    # clean up unneeded cols
    merged_df.drop(
        ['Site Description', 'City', 'County', 'State', 'address', 'city', 'state', 'Zip', 'zip_code', 'Notes',
         'street_num'], axis=1, inplace=True)

    # reorganize cols
    merged_df = merged_df[['Site #', 'order_id', 'Address', 'pickup_location']]

    return merged_df

# internal getter
def get_order_id_to_site_num(df):

    order_id_to_site_num = df.set_index('order_id')['Site #'].to_dict()

    return order_id_to_site_num

# main merger df wrapper func
def get_merged_df(master_file_path, orders_file_path):
    master_df = get_masterdataset_df(master_file_path)
    order_to_location_df = get_order_to_location_df(orders_file_path)
    merged_df = get_merged_and_organized_master_df(master_df, order_to_location_df)
    return merged_df


merged_df = get_merged_df(master_dataset_file_path, json_output_filepath)

order_id_to_site_num = get_order_id_to_site_num(merged_df)
print(order_id_to_site_num)