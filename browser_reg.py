from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from library import  generate_us_name, generate_random_number_by_country, generate_random_1_to_50, save_cookies, random_day, random_month_name,random_year, log_credentials, generate_fake_profiles
from page_load import wait_for_page_load
import time
from get_facebook_otp import check_for_otp
import pickle
import os
import random
def Reg_account_browser(driver):
    
    first_name, last_name = generate_us_name()
    day = random_day()
    my_years = random_year()
    month = random_month_name()
    random_number = generate_random_number_by_country('en_US')
    random_1_to_50 = generate_random_1_to_50()
    wait_for_page_load(driver)
    profile = generate_fake_profiles()
    try:
        first_name_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="First name"]'))
            )

            # Type into the input field
        first_name_input.send_keys(profile["first_name"])
        time.sleep(random.uniform(3, 5))
        last_name_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Last name"]'))
            )

            # Type into the input field
        last_name_input.send_keys(profile["last_name"])
        time.sleep(random.uniform(3, 5))
        month_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Month"]'))
            )

            # Type into the input field
        month_input.send_keys(f"{month}")
        time.sleep(random.uniform(3, 5))
        day_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Day"]'))
            )

            # Type into the input field
        day_input.send_keys(f"{day}")
        time.sleep(random.uniform(3, 5))
        year_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Year"]'))
            )

            # Type into the input field
        year_input.send_keys(f"{my_years}")
        time.sleep(random.uniform(3, 5))
        next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '(//*[@name="sex"])[2]'))
                )

                # Click the "Next" button
        next_button.click()
        time.sleep(random.uniform(3, 5))
        email_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@name="reg_email__"]'))
            )

            # Type into the input field
        email_input.send_keys(profile["email"])
        time.sleep(random.uniform(3, 5))
        passwaord_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@name="reg_passwd__"]'))
            )

            # Type into the input field
        passwaord_input.send_keys("Team@112233")
        time.sleep(random.uniform(3, 5))
        signup_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@name="websubmit"]'))
                )

                # Click the "Next" button
        signup_btn.click()
        wait_for_page_load(driver)
        time.sleep(random.uniform(3, 5))
        try:
            code = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@name="code"]'))
                    )
            code.click()
            time.sleep(random.uniform(3, 5))
            log_credentials(profile["email"], "Team@112233", "No verify", "SUCCESS")
        except Exception as e:
            print("failed")
            
        
       

    except Exception as e:
        print("Failed")

    

    


