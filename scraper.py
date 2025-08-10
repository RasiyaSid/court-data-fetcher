
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os
import time
import requests
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")  
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")



def select_case_type_safe(driver, case_type):
    wait = WebDriverWait(driver, 10).until(lambda d: case_type in [o.text.strip() for o in Select(d.find_element(By.ID, "case_type")).options])
    select_element = Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

def get_captcha_image(case_type, case_number, case_year):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://thrissur.dcourts.gov.in/court-orders-search-by-case-number/')
    wait = WebDriverWait(driver, 15)
    court_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "est_code"))))
    court_dropdown.select_by_visible_text("DISTRICT COURT THRISSUR")

    select_case_type_safe(driver, case_type)
    driver.find_element(By.ID, "reg_no").send_keys(case_number)
    driver.find_element(By.ID, "reg_year").send_keys(case_year)

    captcha_img = driver.find_element(By.ID, "siwp_captcha_image_0")
    captcha_src = captcha_img.get_attribute("src")

    # Download captcha
    img_data = requests.get(captcha_src, verify=False).content
    captcha_path = os.path.join("static", "captcha.png")
    os.makedirs("static", exist_ok=True)
    with open(captcha_path, "wb") as f:
        f.write(img_data)

    driver.quit()
    return captcha_path

def scrape_court_data(case_type, case_number, case_year, captcha_text):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://thrissur.dcourts.gov.in/court-orders-search-by-case-number/')
    wait = WebDriverWait(driver, 15)
    court_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "est_code"))))
    court_dropdown.select_by_visible_text("DISTRICT COURT THRISSUR")

    select_case_type_safe(driver, case_type)
    driver.find_element(By.ID, "reg_no").send_keys(case_number)
    driver.find_element(By.ID, "reg_year").send_keys(case_year)
    driver.find_element(By.ID, "siwp_captcha_value_0").send_keys(captcha_text)

    driver.find_element(By.XPATH, '//*[@id="ecourt-services-court-order-case-number-order"]/div[8]/div[2]/input[1]').click()

    time.sleep(3)
    result = {}
    try:
        # Wait for either "No Record Found" or a results table
        wait.until(lambda d: 
            d.find_elements(By.XPATH, "//*[contains(text(),'No Record Found')]") or
            d.find_elements(By.XPATH, "//*[contains(text(),'The captcha code entered was incorrect.')]")or 
            d.find_elements(By.TAG_NAME, "table")
        )
        
        # Check if "No Record Found" is present
        if driver.find_elements(By.XPATH, "//*[contains(text(),'No Record Found')]"):
            return {"error": "⚠️ No case records found."}
        if driver.find_elements(By.XPATH, "//*[contains(text(),'The captcha code entered was incorrect.')]"):
            return {"error": "Invalid captcha"}
        # Otherwise, get the first table found
        table = driver.find_element(By.TAG_NAME, "table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        if len(rows) > 1:
            cells = rows[1].find_elements(By.TAG_NAME, "td")
            return {
                "case_info": cells[1].text.strip(),
                "order_date": cells[2].text.strip(),
                "pdf_link": cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")
            }
        else:
            return {"error": "⚠️ No data rows found in table."}

    except TimeoutException:
        return {"error": "⏳ Search results did not load in time."}
    finally:
        driver.quit()
