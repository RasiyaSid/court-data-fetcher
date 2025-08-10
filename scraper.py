from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_court_data(case_type1, case_number, case_year):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://thrissur.dcourts.gov.in/court-orders-search-by-case-number/')

    # Wait for the court_complex dropdown
    wait = WebDriverWait(driver, 15)
    court_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "est_code"))))
    court_dropdown.select_by_visible_text("DISTRICT COURT THRISSUR")

    # 3. Select Case Type
    WebDriverWait(driver, 10).until(lambda d: case_type1 in [o.text.strip() for o in Select(d.find_element(By.ID, "case_type")).options])
    Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type1)
    # 4. Enter Case Number
    case_number_input = driver.find_element(By.ID, "reg_no")
    case_number_input.send_keys(case_number)  # Replace with your case number

    # 5. Enter Year
    year_input = driver.find_element(By.ID, "reg_year")
    year_input.send_keys(case_year)  # Replace with actual year

    # 6. Pause for manual captcha entry
    input("👉 Please fill the captcha manually and press Enter to continue...")
    time.sleep(30)
    # 7. Click Search
    search_button = driver.find_element(By.XPATH, '//*[@id="ecourt-services-court-order-case-number-order"]/div[8]/div[2]/input[1]')
    search_button.click()

    # 8. Optional: Wait and then scrape data (you can add scraping logic here)
    time.sleep(30)
    result={}
    try:
        try:
            no_records_msg = driver.find_element(By.XPATH, "//*[contains(text(),'No Record Found')]")
            result = {"error": "⚠️ No case records found."}
            driver.quit()
            return result
        except:
            pass 
        # Wait for table
        table = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="KLTR01"]/table')))
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        if rows:
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 4:
                    case_info = cells[1].text.strip()
                    order_date = cells[2].text.strip()
                    try:
                        pdf_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, ".//td[@data-th='Order Details']//a")))
                        pdf_link = pdf_element.get_attribute("href")
                        result = {
                            "case_info": case_info,
                            "order_date": order_date,
                            "pdf_link": pdf_link
                        }
                        break  # Take the first PDF found (most recent)
                    except:
                        continue
        else:
            result = {"error": "⚠️ No case records found."}

    except Exception as e:
        result = {"error": f"Could not extract case details: {str(e)}"}

    driver.quit()
    return result


#Crl.MP / 103822 / 2025
#RCA/100079/2025
#EP / 100087 / 2025