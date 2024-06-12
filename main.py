from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

def get_new_listings(urls, log_path='listings.log'):
    # Load previously found listings from log file if it exists
    if os.path.exists(log_path):
        with open(log_path, 'r') as file:
            logged_urls = set(line.strip() for line in file)
    else:
        logged_urls = set()

    # Set up the Selenium WebDriver
    options = Options()
    options.add_argument("--disable-notifications")
    service = Service(executable_path='./chromedriver')  # Update this to your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)

    for url in urls:
        driver.get(url)
        time.sleep(5)  # Wait for any dynamic content to load

        # Check for CAPTCHA and manually solve if needed
        if 'CAPTCHA' in driver.page_source:
            print("Please solve the CAPTCHA manually...")
            input("Press Enter in this console once the CAPTCHA is solved...")

        # After CAPTCHA is solved, proceed to scrape the page
        links = driver.find_elements(By.TAG_NAME, 'a')
        new_listings = []
        for link in links:
            href = link.get_attribute('href')
            if href and href.startswith('https://www.yad2.co.il/realestate/item/'):
                listing_url = href.split('?')[0]
                if listing_url not in logged_urls:
                    new_listings.append(listing_url)

        # Log new listings to file and print them
        with open(log_path, 'a') as file:
            for listing in new_listings:
                print(listing)
                file.write(f"{listing}\n")

    driver.quit()

# List of URLs to scrape
urls = [
    'https://www.yad2.co.il/realestate/rent?topArea=19&area=54&city=9700&price=-1-7500&parking=1&shelter=1&EnterDate=1722470400--1&zoom=13',
    'https://www.yad2.co.il/realestate/rent?city=5000&price=-1-7500&parking=1&shelter=1&EnterDate=1722470400--1&zoom=13'
]

get_new_listings(urls)
