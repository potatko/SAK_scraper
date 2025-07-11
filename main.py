from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException  
import time
import csv

url = "https://www.sak.sk/web/sk/cms/lawyer/adv"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

advocate_details = []

total_pages = 551


total_rows = len(driver.find_elements(By.CSS_SELECTOR, "tbody > tr"))



for page in range(total_pages):
 
    total_rows = len(WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody > tr"))
    ))
    # Scrape the current page
    for index in range(total_rows):
       
        advocate_rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody > tr"))
        )

        row = advocate_rows[index]

        name = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2) a").text

        # Navigate to the detail page
        row.find_element(By.CSS_SELECTOR, "td:nth-of-type(2) a").click()

        # Wait for the detail page and find the email element using XPath
        try:
            telephone_xpath = "/html/body/form/div/div[2]/div[1]/main/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[4]"
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, telephone_xpath))
            )
            telephone_full_text = driver.find_element(By.XPATH, telephone_xpath).text
            telephone = telephone_full_text.split('\n')[1] if '\n' in telephone_full_text else telephone_full_text
        except TimeoutException:
            telephone = 'Not Available'
            print("Telephone not found for:", name)
            

        # Extracting the email
        try:
            email_xpath = "/html/body/form/div/div[2]/div[1]/main/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[7]"
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, email_xpath))
            )
            email_full_text = driver.find_element(By.XPATH, email_xpath).text
            email = email_full_text.split('\n')[1] if '\n' in email_full_text else email_full_text
        except TimeoutException:
            email = 'Not Available'
            print("Email not found for:", name)

        # Extracting the mobile number 
        try:
            mobile_xpath = "/html/body/form/div/div[2]/div[1]/main/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[6]/div"
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, mobile_xpath))
            )
            mobile_full_text = driver.find_element(By.XPATH, mobile_xpath).text
            mobile = mobile_full_text.split('\n')[1] if '\n' in mobile_full_text else mobile_full_text
        except TimeoutException:
            mobile = 'Not Available'
            print("Mobile not found for:", name)
            

        # Store the details
        advocate_details.append({'Name': name, 'Telephone': telephone,'Mobile': mobile, 'Email': email})

        driver.get(url)

    # Navigate to the next page
    if page < total_pages - 1:
        try:
            next_page_xpath = "/html/body/form/div/div[2]/div[1]/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div[1]/nav/ul/li[3]/a"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, next_page_xpath))
            ).click()
        except TimeoutException:
            print("Unable to navigate to the next page.")
            break

    time.sleep(1)
driver.quit()

for detail in advocate_details:
    print(detail)


#csv export
csv_file_path = 'advocate_details.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Telephone', 'Mobile', 'Email'])
    writer.writeheader()
    for detail in advocate_details:
        writer.writerow(detail)

print(f"Data has been written to {csv_file_path}")
