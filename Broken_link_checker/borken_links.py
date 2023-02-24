import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

website_url="https://testerscafe.in/"


options = webdriver.ChromeOptions()
options.add_argument('--headless')
# Start the web driver with headless mode using options
driver = webdriver.Chrome(options=options)

errors=[]

# Set maximum time to wait for a page to load
WAIT_TIME = 10

# Navigate to the website that we want to test
driver.get(website_url)

# Wait for the page to load
WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Find all links on the page
links = driver.find_elements(By.TAG_NAME,'a')

# Loop through the links and check for broken links
for link in links:
    url = link.get_attribute('href')
    if url:
        if url.startswith('http'):
            # Check if the link is valid
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    pass
                else:
                    errors.append(f"{url} is broken! Status code: {response.status_code}\nSource code: {link.get_attribute('outerHTML')}\n\n")
            except requests.exceptions.RequestException:
                errors.append(f"{url} is not valid.\nSource code: {link.get_attribute('outerHTML')}\n\n")
        else:
            errors.append(f"{url} is not a valid external link. \nSource is: {link.get_attribute('outerHTML')}\n\n")
    else:
        errors.append(f"{url} the href is blank. \nSource code is:{link.get_attribute('outerHTML')}\n\n")
if not errors:
    driver.quit()
    # Close the web driver
    assert True
else:
    logging.error(("URLS:\n\n{}".format("".join(errors)))) #Log all the errors in format
