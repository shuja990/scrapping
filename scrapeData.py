from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://insafpk.github.io/pticandidates/")

# Wait for the page to load completely
time.sleep(5)  # Wait for 5 seconds. Adjust the time as needed.

# Function to scrape data for a specific constituency
def scrape_data(constituency):
    try:
        # Find the search box and input the constituency
        search_box = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        search_box.clear()
        search_box.send_keys(constituency)
        time.sleep(2) # Wait for the content to load

        # Scrape the required data
        constituency_data = driver.find_element(By.CSS_SELECTOR, "h3").text
        candidate_data = driver.find_element(By.CSS_SELECTOR, "h4").text
        symbolname_data = driver.find_element(By.CSS_SELECTOR, "span").text
        image_url = driver.find_element(By.CSS_SELECTOR, "img.symbol-image").get_attribute("src")
        whatsapp_link = driver.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        return {
            "constituency": constituency_data,
            "candidate": candidate_data,
            "symbolname": symbolname_data,
            "image_url": image_url,
            "whatsapp_link": whatsapp_link
        }
    except NoSuchElementException:
        # Return None if data is not found
        return None

provinces = [{"name": "NA", "seats": 300},{"name": "PK", "seats": 120},{"name": "PB", "seats": 55}, {"name": "PP", "seats": 300}, {"name": "PS", "seats": 175}]

for j in provinces:
    results = []  # Reset results for each province
    for i in range(1, j['seats'] + 1):
        constituency = f"{j['name']}-{i}"
        data = scrape_data(constituency)
        if data:
            results.append(data)

    with open(f"{j['name']}.json", 'w') as json_file:
        json.dump(results, json_file, indent=4)

# Close the WebDriver
driver.quit()
