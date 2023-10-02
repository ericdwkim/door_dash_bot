import pandas as pd
import re
import json
import csv
from datetime import datetime

master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'

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

def get_masterdataset_df(filepath):
    raw_master_df = pd.read_excel(filepath, index_col=0)
    master_df = add_cols_to_masterset_df(raw_master_df)
    return master_df

def map_order_to_location(orders):
    order_id_to_pickup_location  = {}
    for order in orders:
        order_id = order['Order']
        store_addrs = order['Pick Up Location']
        order_id_to_pickup_location[order_id] = store_addrs
    return order_id_to_pickup_location


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


# wrapper func
def get_order_to_pickup_location_df(df):
    order_to_split_pickup_location_df = splitup_pickup_location(df)

    order_to_split_pickup_location_and_street_num_df = add_street_num_col(order_to_split_pickup_location_df)

    return order_to_split_pickup_location_and_street_num_df


def get_merged_and_organized_master_df(df1, df2):

    # inner join on fields
    df = pd.merge(df1, df2, left_on=['Zip', 'street_num'], right_on=['zip_code', 'street_num'], how='inner')

    # clean up unneeded cols
    df.drop(
        ['Site Description', 'City', 'County', 'State', 'address', 'city', 'state', 'Zip', 'zip_code', 'Notes',
         'street_num'], axis=1, inplace=True)

    # reorganize cols
    df = df[['Site #', 'order_id', 'Address', 'pickup_location']]

    return df


def order_id_to_site_num(df):

    order_to_site_num_map = df.set_index('order_id')['Site #'].to_dict()

    return order_to_site_num_map


