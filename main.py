from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# Set up Chrome options for headless browsing
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set the path to the chromedriver (Render's default location)
driver_path = "/usr/bin/chromedriver"

# Set the path to Chrome itself
options.binary_location = "/usr/bin/google-chrome"  # Add this line to specify the Chrome binary

# Create a service object using the chromedriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Base URL
base_url = "https://laws.moj.gov.sa/en/legislations-regulations?pageNumber=1&pageSize=9&sortingBy=7"
driver.get(base_url)

# Wait for page to load
wait = WebDriverWait(driver, 10)

# Find all links to inner pages
links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/legislations/']")

pdf_folder = "pdfs"
os.makedirs(pdf_folder, exist_ok=True)

for link in links:
    url = link.get_attribute("href")
    driver.get(url)
    time.sleep(2)  # Wait for page to load

    try:
        pdf_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export to PDF')]")))
        pdf_button.click()
        time.sleep(5)  # Wait for download

        # Get PDF link after clicking
        pdf_link = driver.find_element(By.CSS_SELECTOR, "a[href$='.pdf']").get_attribute("href")
        pdf_name = pdf_link.split("/")[-1]

        # Download the PDF
        pdf_data = requests.get(pdf_link).content
        with open(os.path.join(pdf_folder, pdf_name), "wb") as f:
            f.write(pdf_data)

        print(f"Downloaded: {pdf_name}")

    except Exception as e:
        print(f"Failed on {url}: {e}")

driver.quit()
