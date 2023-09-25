from selenium import webdriver
# import the Keys class
# from selenium.webdriver.common import keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException



options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(service=Service(executable_path="/opt/homebrew/bin/chromedriver"), options=options)

# driver

driver.get("https://www.doordash.com/merchant/orders?business_id\=11495418")
table_rows = driver.find_elements(By.TAG_NAME, 'tr')

# type(table_rows)
# len(table_rows)
# table_rows

def wait_for_element(locator, locator_type, timeout):
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((locator_type, locator)))
        return True
    except TimeoutException:
        return False


def find_element_and_click(locator ,locator_type=By.CSS_SELECTOR):
    """
    Finds element and clicks it using `WebElement.click()`
    :param locator:
    :param locator_type:
    :return: Tuple(bool, WebElement)
    """
    try:
        element = driver.find_element(locator_type, locator)
        # element.click() #TODO
        return True, element
    except NoSuchElementException:
        print(f'Element {locator} was not found.')
        return False, None
    except Exception as e:
        print(f'Error occurred when trying to find and click element with locator: "{locator}" resulting in error message: {str(e)}')
        return False, None

# TODO
results = []
for idx, table_row in enumerate(table_rows):
    if idx >= 1:
        table_row.click()

        ssp_found = wait_for_element(locator="//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']",
                                     locator_type=By.XPATH, timeout=10)

        # elem = driver.find_element(By.XPATH, "//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']")

        found, elem = find_element_and_click(locator="//*[@class='styles__SidesheetContent-sc-czzuxh-2 hKVVOI']",
                                             locator_type=By.XPATH)

        # print(elem)
        # print(type(elem))
        # print(elem.text)
        results.append(elem.text)

        exit_btn = driver.find_element(By.XPATH,
                                       '//*[@id="MerchantApp"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/nav/div[1]/div[1]/div/button')

        exit_btn.click()




print(results)







