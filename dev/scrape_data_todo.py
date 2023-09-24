import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_table_data(url):
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Navigate to the web page with the table
    driver.get(url)

    results = []

    try:
        # Locate the table body element
        table_body = driver.find_element(By.XPATH, '//*[@id="MerchantApp"]/div/div/div[1]/div/div[2]/div[2]/div/div/div[4]/div/div/div[5]/div[1]/div/table/tbody')

        # Get a list of all table row elements
        table_rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Iterate through each table row
        for table_row in table_rows:
            # Click on the table row to trigger the sidesheetbody
            table_row.click()

            # Wait for the sidesheetbody element to load
            wait = WebDriverWait(driver, 10)
            sidesheetbody = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="MerchantApp"]/div/div/div[3]/div[2]/div[2]/div/div')))

            # Scrape the target content from the sidesheetbody
            target_content = sidesheetbody.text  # You can use any method to extract the content

            # Append the scraped content to the results list
            results.append(target_content)

    finally:
        # Close the WebDriver when done (even if an exception occurred)
        driver.quit()

    return results

# Usage example:
webpage_url = "your_webpage_url_here"
order_contents = scrape_table_data(webpage_url)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')

# Loop through order_contents and create a sheet for each order
for i, order_content in enumerate(order_contents):
    # Convert the order content to a DataFrame
    df = pd.DataFrame([order_content.split('\n')], columns=["Order Content"])

    # Write the DataFrame to the Excel sheet
    df.to_excel(writer, sheet_name=f"Order_{i + 1}", index=False)

# Close the Pandas Excel writer and save the file
writer.save()

""" 
TODO:

1) have main scraping func return list of strings where each string elem is each order content. 
2) create new func to accept this list of strings and to create each orders content as an excel sheet
    2a) create a getter func to be called within this outter func that instantiates each order content string with its Order ID which should be the first line of text in eah order string element and with the order_id variable
    2b) create a setter func that will set this order_id variable as the name of its sheet so that each sheet is named after its order_id
3) save the final excel with all sheets as a single excel file 
"""
