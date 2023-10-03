import pandas as pd
import re
import json
import csv
from datetime import datetime


orders =  [
    {
        "Order": "42C2A525",
        "Delivered": "The order was delivered at 11:41 PM on October 1, 2023.",
        "Pick Up Location": "5004 Wesley St, Greenville, TX 75402, USA",
        "Order Details": {
            "1 \u00d7 Coca-Cola Can (12 pk-12 oz) (Soda TX)": "$11.29",
            " 1 \u00d7 TXB Water Bottle (24 pk) (16.9 oz) (Water TX)": "$7.49",
            " 1 \u00d7 Coke Classic Bottle (20oz) (Soda TX)": "$3.19"
        },
        "Subtotal": "$21.97",
        "Subtotal Tax": "$1.19",
        "Commission (23%)": "-$5.05",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$18.11",
        "Transaction #8113346069 - Delivery": "$18.11"
    },
    {
        "Order": "AA85B890",
        "Delivered": "The order was delivered at 10:08 PM on October 1, 2023.",
        "Pick Up Location": "5004 Wesley St, Greenville, TX 75402, USA",
        "Order Details": {
            "1 \u00d7 Moon Pie Double Decker Banana (2.75oz) (Pastry TX)": "$2.29",
            " 1 \u00d7 Moon Pie Double Decker Chocolate (2.75oz) (Pastry TX)": "$2.29",
            " 1 \u00d7 TXB Sweet Tea Bottle (16oz) (Tea TX)": "$3.29",
            " 1 \u00d7 TXB Strawberry White Tea Bottle (16oz) (Tea TX)": "$2.59",
            " 1 \u00d7 TXB Premium Electrolyte Water Bottle (12pk 1L) (Water TX)": "$4.09"
        },
        "Subtotal": "$14.55",
        "Subtotal Tax": "$0.59",
        "Commission (16%)": "-$2.33",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$12.81",
        "Transaction #8112864098 - Delivery": "$12.81"
    },
    {
        "Order": "773C7330",
        "Delivered": "The order was delivered at 9:07 PM on October 1, 2023.",
        "Pick Up Location": "5004 Wesley St, Greenville, TX 75402, USA",
        "Order Details": {
            "1 \u00d7 Lone Star Beer Can (16 oz x 6 ct) (Domestic Beer NT)": "$13.79"
        },
        "Subtotal": "$13.79",
        "Subtotal Tax": "$1.14",
        "Commission (16%)": "-$2.21",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$12.72",
        "Transaction #8112394394 - Delivery": "$12.72"
    },
    {
        "Order": "No Delivery has been found."
    },
    {
        "Order": "EDCB46B1",
        "Delivered": "Error Charge The customer reported one or more missing items resulting in an error charge of $5.86. If you believe this was an error, you can dispute the error charge by October 15, 2023.",
        "Pick Up Location": "1001 W Van Alstyne Pkwy, Van Alstyne, TX 75495, USA",
        "Order Details": {
            "1 \u00d7 Michelob Ultra Light Beer Can (12 oz x 12 ct) (Domestic Beer NT)": "$27.49",
            " 1 \u00d7 Truly Hard Seltzer Berry Mix Pack Can (12 oz x 12 ct) (Seltzer NT)": "$28.79"
        },
        "Subtotal": "-$5.30 Error Charge Tax -$0.56 Error Charge Total -$5.86 Order Total $47.98",
        "Commission (23%)": "-$12.94 Order Total $47.98 Error Charges 1 \u00d7 Michelob Ultra Light Beer Can (12 oz x 12 ct) (Domestic Beer NT) Missing Item -$5.30 Error Charge",
        "Estimated Payout": "$42.12",
        "Transaction #8109695187 - Delivery": "$47.98 Transaction #8109811800 - Error Charges -$5.86"
    },
    {
        "Order": "68944F97",
        "Delivered": "The order was delivered at 2:50 PM on October 1, 2023.",
        "Pick Up Location": "800 W Interstate 20, Big Spring, TX 79720, USA",
        "Order Details": {
            "2 \u00d7 Michelob Ultra Light Beer Can (12 oz x 18 ct) (Domestic Beer ST)": "$72.58"
        },
        "Subtotal": "$72.58",
        "Subtotal Tax": "$5.99",
        "Commission (23%)": "-$16.69",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$61.88",
        "Transaction #8108722869 - Delivery": "$61.88"
    },
    {
        "Order": "ED39CFE2",
        "Delivered": "Error Charge The customer reported one or more missing items resulting in an error charge of $8.11. If you believe this was an error, you can dispute the error charge by October 15, 2023.",
        "Pick Up Location": "1301 N U.S. Hwy 281, Marble Falls, TX 78654, USA",
        "Order Details": {
            "1 \u00d7 Ice Large (Fountain, Frozen, & Tea)": "$7.49",
            " 1 \u00d7 Campbells Chicken Noodle Bowl (15.4oz) (Pantry TX)": "$5.29",
            " 2 \u00d7 TXB Premium Electrolyte Water (1 lt) (Water TX)": "$8.78",
            " 1 \u00d7 7 Up Bottle (20 oz) (Soda TX)": "$3.79",
            " 2 \u00d7 Gatorade Cool Blue (28 oz) (Sports Drinks TX)": "$9.58"
        },
        "Subtotal": "-$7.50 Error Charge Tax -$0.61 Error Charge Total -$8.11 Order Total $28.36",
        "Commission (25%)": "-$8.73 Order Total $28.36 Error Charges 1 \u00d7 Ice Large (Fountain, Frozen, & Tea) Missing Item -$7.50 Error Charge",
        "Estimated Payout": "$20.25",
        "Transaction #8107801352 - Delivery": "$28.36 Transaction #8107871093 - Error Charges -$8.11"
    },
    {
        "Order": "78BAE2F8",
        "Delivered": "The order was delivered at 12:41 PM on October 1, 2023.",
        "Pick Up Location": "1001 S State Hwy 16, Fredericksburg, TX 78624, USA",
        "Order Details": {
            "1 \u00d7 Crush Grape Bottle (20oz) (Soda TX)": "$3.79",
            " 1 \u00d7 Turkey & Bacon Wrap (Salads, Wraps, & Cold Sandwiches TXB#61)": "$8.79",
            " Subtotal for Tax Calculations": "$12.58"
        },
        "Subtotal Tax": "$1.04",
        "Commission (16%)": "-$2.01",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$11.61",
        "Transaction #8107649354 - Delivery": "$11.61"
    },
    {
        "Order": "DE4528F2",
        "Delivered": "The order was delivered at 12:39 PM on October 1, 2023.",
        "Pick Up Location": "2320 W Main St, Durant, OK 74701, USA",
        "Order Details": {
            "1 \u00d7 Coke Classic Bottle (20oz) (Soda OK)": "$3.19",
            " 2 \u00d7 Red Bull Energy Drink Can (12 oz) (Energy Drinks OK)": "$11.58"
        },
        "Subtotal": "$14.77",
        "Subtotal Tax": "$1.38",
        "Commission (23%)": "-$3.40",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$11.37",
        "Transaction #8107692197 - Delivery": "$11.37"
    },
    {
        "Order": "F5539B37",
        "Delivered": "The order was delivered at 10:52 AM on October 1, 2023.",
        "Pick Up Location": "3702 FM2147, Horseshoe Bay, TX 78657, USA",
        "Order Details": {
            "2 \u00d7 Chorizo Egg Cheese Quesadilla (Breakfast Tacos & Quesadillas) Salsa: Salsa Roja": "$14.98"
        },
        "Subtotal": "$14.98",
        "Subtotal Tax": "$1.24",
        "Commission (25%)": "-$3.75",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$12.47",
        "Transaction #8106904074 - Delivery": "$12.47"
    },
    {
        "Order": "FE329688",
        "Delivered": "The order was delivered at 10:03 AM on October 1, 2023.",
        "Pick Up Location": "800 W Interstate 20, Big Spring, TX 79720, USA",
        "Order Details": {
            "3 \u00d7 Red Bull Energy Drink Can (12 oz) (Energy Drinks TX)": "$17.37"
        },
        "Subtotal": "$17.37",
        "Subtotal Tax": "$1.43",
        "Commission (16%)": "-$2.78",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$16.02",
        "Transaction #8106720721 - Delivery": "$16.02"
    },
    {
        "Order": "C5A903F0",
        "Cancelled - Paid": "The order was cancelled on October 1, 2023 at 7:31 AM. You\u2019re paid for cancelled orders when you\u2019ve successfully confirmed an order, it was prepared, and you did not initiate or are not at fault for the cancellation.",
        "Pick Up Location": "2503 TX-349, Midland, TX 79706, USA",
        "Order Details": {
            "1 \u00d7 Sausage Egg Cheese Taco (Breakfast Tacos & Quesadillas)": "$3.79"
        },
        "Subtotal": "$3.79",
        "Subtotal Tax": "$0.30",
        "Commission (16%)": "-$0.61",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$3.48",
        "Transaction #8106298092 - Delivery": "$3.48"
    },
    {
        "Order": "782881C7",
        "Delivered": "The order was delivered at 3:08 AM on October 1, 2023.",
        "Pick Up Location": "145 Lehman Rd, Kyle, TX 78640, USA",
        "Order Details": {
            "1 \u00d7 Hostess Powdered Donettes Bag (10.5oz) (Donuts TX)": "$6.39",
            " 1 \u00d7 Fountain Drink (Fountain, Frozen, & Tea) Drink Selection: Sprite": "$0.00",
            " 1 \u00d7 Fountain Drink (Fountain, Frozen, & Tea) Drink Selection: TXB Cherry Limeade": "$0.00",
            " 1 \u00d7 Fountain Drink (Fountain, Frozen, & Tea) Drink Selection: TXB Root Beer": "$0.00"
        },
        "Subtotal": "$6.39",
        "Subtotal Tax": "$0.00",
        "Commission (16%)": "-$1.02",
        "Total Customer Refund": "-$0.00 Refunds $6.99",
        "Estimated Payout": "$12.36",
        "Transaction #8105816170 - Delivery": "$5.37"
    },
    {
        "Order": "ECCAB249",
        "Delivered": "The order was delivered at 2:32 AM on October 1, 2023.",
        "Pick Up Location": "1402 Williams Dr, Georgetown, TX 78628, USA",
        "Order Details": {
            "1 \u00d7 Chicken Tender Meal Kit (Meal Kits TXB#65)": "$9.19"
        },
        "Subtotal": "$9.19",
        "Subtotal Tax": "$0.76",
        "Commission (16%)": "-$1.47",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$8.48",
        "Transaction #8105817488 - Delivery": "$8.48"
    },
    {
        "Order": "8E90EF84",
        "Delivered": "The order was delivered at 1:24 AM on October 1, 2023.",
        "Pick Up Location": "21024 W, 21024 State Hwy 71, Spicewood, TX 78669, USA",
        "Order Details": {
            "1 \u00d7 Pork Tamale Meal Kit (Meal Kits TXB#62)": "$9.19"
        },
        "Subtotal": "$9.19",
        "Subtotal Tax": "$0.76",
        "Commission (16%)": "-$1.47",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$8.48",
        "Transaction #8105638611 - Delivery": "$8.48"
    },
    {
        "Order": "B944ED77",
        "Cancelled - Not Paid": "The order was cancelled on October 1, 2023 at 12:57 AM. You were not paid because you were unable to fulfill the order.",
        "Pick Up Location": "1402 Williams Dr, Georgetown, TX 78628, USA",
        "Order Details": {
            "2 \u00d7 Black Box Pinot Grigio Tetra 500ml Box (12% ABV) (Specialty Wine)": "$12.58"
        },
        "Subtotal": "$12.58",
        "Subtotal Tax": "$1.04",
        "Commission (16%)": "-$2.01",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$0.00"
    },
    {
        "Order": "E7A89C68",
        "Delivered": "The order was delivered at 12:43 AM on October 1, 2023.",
        "Pick Up Location": "1402 Williams Dr, Georgetown, TX 78628, USA",
        "Order Details": {
            "1 \u00d7 Pepcid AC Maximum Strength Tablet (8ct) (Medicine TX)": "$14.39",
            " 1 \u00d7 2% Milk (16 oz) (Milk TX)": "$3.79"
        },
        "Subtotal": "$18.18",
        "Subtotal Tax": "$0.00",
        "Commission (16%)": "-$2.91",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$15.27",
        "Transaction #8105526412 - Delivery": "$15.27"
    },
    {
        "Order": "C41B4C30",
        "Delivered": "The order was delivered at 12:43 AM on October 1, 2023.",
        "Pick Up Location": "21024 W, 21024 State Hwy 71, Spicewood, TX 78669, USA",
        "Order Details": {
            "1 \u00d7 Triple Chocolate Chunk Cookie (Pastries & Desserts)": "$2.49",
            " 1 \u00d7 Chocolate Milk (16 oz) (Milk TX)": "$3.79",
            " 3 \u00d7 Fountain Drink (Fountain, Frozen, & Tea) Drink Selection: Dr Pepper": "$0.00",
            " 1 \u00d7 Dr Pepper Bottle (20 oz) (Soda TX)": "$3.79"
        },
        "Subtotal": "$10.07",
        "Subtotal Tax": "$0.83",
        "Commission (16%)": "-$1.61",
        "Total Customer Refund": "-$0.00",
        "Estimated Payout": "$9.29",
        "Transaction #8105477186 - Delivery": "$9.29"
    }
]
class DataMerger:
    def __init__(self, orders):
        self.master_dataset_file_path = '/Users/ekim/workspace/personal/dd-bot/dev/store_list.xlsx'

        self.orders = orders
        self.master_df = None
        self.order_to_location_df = None
        self.merged_df = None
        self.store_num_to_order_ids = {}

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
            if len(order) >= 7:  # presumes a complete order to have at least 7 keys as brief testing showed 8 - 10 with avg being ~10
                complete_orders.append(order)
        return complete_orders

    def order_id_to_pickup_location(self):
        order_id_to_pickup_location = {}
        for order in self.orders:
            order_id = order['Order']
            store_addrs = order['Pick Up Location']
            order_id_to_pickup_location[order_id] = store_addrs
        return order_id_to_pickup_location

    def get_raw_order_to_location_df(self):
        self.remove_incomplete_orders()
        self.order_id_to_pickup_location()
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


    def store_num_to_order_ids_from_order_id_to_store_num(self, original_dict):
        """
        convert duplicate store_num value from order to site num mapping to aggregated store_num : {order_ids}
        :return:
        """

        for order_id, store_num in original_dict.items():
            if store_num not in store_num_to_order_ids:
                self.store_num_to_order_ids[store_num] = set()
            self.store_num_to_order_ids[store_num].add(order_id)

    def get_store_num_to_order_ids_from_merged_df(self):
        order_id_to_store_num = self.merged_df.set_index('order_id')['Site #'].to_dict()
        self.store_num_to_order_ids_from_order_id_to_store_num(order_id_to_store_num)

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
                order['Store Number'] = 'N/A'

dm = DataMerger(orders)

dm.add_store_numbers_to_orders()

print(orders)