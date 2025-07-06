
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

driver = None

def start_browser():
    global driver
    if driver is not None:
        return driver

    options = Options()
    options.binary_location = "/opt/chrome/chrome"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
    driver.get("https://share.google/RiGoUdAWQEkczypqg")
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[1]/fieldset/div/div[1]/div/div[1]/table/tbody/tr[2]/td/div/div/ul/li[1]/span[3]/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div/fieldset/div/div[3]/div/div/div/table/tbody/tr[2]/td/div/ul/div/table/tbody/tr[2]/td[2]/span[1]/a").click()
    time.sleep(2)
    return driver

def fetch_result(roll_number):
    global driver
    if not driver:
        driver = start_browser()

    for f in os.listdir(DOWNLOAD_DIR):
        if f.endswith(".pdf"):
            os.remove(os.path.join(DOWNLOAD_DIR, f))

    input_field = driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div[2]/table/tbody/tr/td[2]/span/input")
    input_field.clear()
    input_field.send_keys(roll_number)
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/form/div[4]/div/div[3]/span[1]/input").click()
    time.sleep(3)

    for _ in range(5):
        pdf_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".pdf")]
        if pdf_files:
            path = os.path.join(DOWNLOAD_DIR, pdf_files[0])
            driver.refresh()
            time.sleep(2)
            return path
        time.sleep(1)
    return None
