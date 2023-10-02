import csv

def write_json_to_csv(json_list, output_filepath):
    # Check if the list is empty
    if not json_list:
        print("The JSON list is empty. Exiting.")
        return

    # Use the keys in the first dictionary as the header row
    headers = json_list[0].keys()

    with open(output_filepath, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the rows
        for row in json_list:
            writer.writerow(row)

# Assuming orders_json is your list of dictionaries
orders_json = get_prettified_and_mapped_orders(orders)


# Output the list of dictionaries to CSV
write_json_to_csv(orders_json, 'output.csv')
