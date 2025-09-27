from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from library import  generate_us_name, generate_random_number_by_country, generate_random_1_to_50, save_cookies
from page_load import wait_for_page_load
import time
from get_facebook_otp import check_for_otp
import pickle
import os

def Reg_account(driver):
# Wait for the button to be clickable and click it
    wait = WebDriverWait(driver, 30)
    try:
        wait_for_page_load(driver)
        time.sleep(0.5)
        create_account_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Create new account"]'))
        )
        create_account_button.click()
        
        wait_for_page_load(driver)
        wait_for_page_load(driver)
        time.sleep(0.5)

        get_started_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Get started"]'))
        )
        get_started_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

        first_name, last_name = generate_us_name()
        random_number = generate_random_number_by_country('en_US')
        random_1_to_50 = generate_random_1_to_50()

        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")

        # Wait for the "First name" input field to be visible and interactable
        first_name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="First name"]'))
        )

        # Type into the input field
        first_name_input.send_keys(f"{first_name}")

        wait_for_page_load(driver)
        time.sleep(0.5)

        # Wait for the "Last name" input field to be visible and interactable
        last_name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Last name"]'))
        )

        # Type into the input field
        last_name_input.send_keys(f"{last_name}")

        wait_for_page_load(driver)
        time.sleep(0.5)

        # Wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Next"]'))
        )

        # Click the "Next" button
        next_button.click()

        time.sleep(0.5)

        try:
            # Wait for the element to be visible and get its text
            select_name_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//span[text()="Select your name"]'))
            )

            # Check the text content
            if select_name_text.text == "Select your name":
                print("The text is correct.")
                # You can perform further actions here
                # Wait for the first clickable element to be present and clickable
                wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
                first_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@role='radio'])[1]")))

                # Click the first element
                first_element.click()

                wait_for_page_load(driver)
                time.sleep(0.5)

                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))

                # Click the button
                next_button.click()
            else:
                print("The text is not correct. It's: " + select_name_text.text)

        except Exception as e:
            print(f"Error loading cookies: {e}")

        # # Wait for the date input field to be clickable
        # birthday_input = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Birthday (0 year old)"]'))
        # )

        # # Set a new value for the birthday (e.g., "2000-01-01")

        # birthday_input.send_keys(f"{random_day}")
        # time.sleep(0.5)
        # birthday_input.send_keys(f"{random_month}")
        # time.sleep(0.5)
        # birthday_input.send_keys(f"{random_year}")

        wait_for_page_load(driver)
        time.sleep(0.5)

        try:
            # Wait for the "Next" button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Next"]'))
            )

            # Click the "Next" button
            next_button.click()

            time.sleep(1)

            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Next"]'))
            )

            # Click the "Next" button
            next_button.click()

        except Exception as e:
            print(f"Error loading cookies: {e}")


        age_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@aria-label="Age"]'))
        )

        # Clear the input field (if needed) and type the age value
        age_input.send_keys(f"{random_1_to_50}")  # Change this value as needed

        wait_for_page_load(driver)
        time.sleep(0.5)

        # Wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/ancestor::div[@role="button"]'))
        )

        # Click the "Next" button
        next_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

               # Wait until the "OK" button is clickable
        try:
            ok_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(text(), "OK")]'))
            )
            ok_button.click()
            print("OK button clicked successfully.")
        except Exception as e:
            print(f"Failed to click OK button: {e}")

        wait_for_page_load(driver)
        time.sleep(0.5)


        # Wait for the "Female" radio button to be clickable
        female_radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Female"]'))
        )

        # Click the "Female" radio button
        female_radio_button.click()
        
        wait_for_page_load(driver)
        time.sleep(0.5)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))

        # Click the button
        next_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

        # mobile_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Mobile number']")))

        # # Fill in the mobile number
        # mobile_input.send_keys(f"{random_number}")

        signup_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@role='button' and @aria-label='Sign up with email']"
        )))
        
        # Click the button
        signup_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

          # Locate the email input by traversing its parent container
        email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email' and @aria-label='Email']")))
        
        # Alias email (you can change it as needed)
        alias_email = f"n3w.mmo+{first_name}{last_name}@yandex.com"  # Example alias email
        
        # Call the function and pass the alias email
        
        # Enter an email into the input field
        email_input.send_keys(f"{alias_email}")

        wait_for_page_load(driver)
        time.sleep(0.5)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next']")))

        # Click the "Next" button
        next_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

        # Wait until the "OK" button is clickable

        try: 
                password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Password']")))

                # Enter the password into the input field
                password_input.send_keys("Mmo@112233")

                wait_for_page_load(driver)
                time.sleep(0.5)

                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next']")))

                # Click the "Next" button
                next_button.click()

                wait_for_page_load(driver)
                time.sleep(0.5)
        except Exception as e:

            print("Alert action")
            try:
                ok_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and contains(text(), "OK")]'))
                )
                ok_button.click()
                print("OK button clicked successfully.")
            except Exception as e:
                print(f"No Alert Ok")

            wait_for_page_load(driver)
            time.sleep(0.5)


            try:
                continue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Continue creating account"]'))
                )
                # Click the "Continue creating account" button
                continue_button.click()

            except Exception as e:
                print(f"No Action Continue creating account")

            wait_for_page_load(driver)
            time.sleep(0.5)
            
            password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Password']")))

            # Enter the password into the input field
            password_input.send_keys("Mmo@112233")

            wait_for_page_load(driver)
            time.sleep(0.5)

            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next']")))

            # Click the "Next" button
            next_button.click()

            wait_for_page_load(driver)
            time.sleep(0.5)

        try: 

            not_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Not now']")))

            # Click the "Not now" button
            not_now_button.click()

        except Exception as e:
            save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Save']")))

            # Click the "Save" button
            save_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)

        agree_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='I agree']")))

        # Click the "I agree" button
        agree_button.click()

        wait_for_page_load(driver)
        time.sleep(0.5)
            # Track how much time has passed
        try:
            # Explicit wait until the OTP input field is visible
            otp_input = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Confirmation code']"))
            )
            otp = check_for_otp(f"{alias_email}")
            print("Got the otp waiting 30s")
            time.sleep(2)
            
            print("OTP input field is visible")
            # Enter the OTP (replace with actual OTP)
            otp_input.send_keys(f"{otp}")
            
            wait_for_page_load(driver)
            time.sleep(0.5)
        
                # Explicit wait for the "Next" button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            print("Next button is clickable")

            # Click the "Next" button
            next_button.click()

            wait_for_page_load(driver)
            time.sleep(0.5)

            # time.sleep(120)
            
            try: 

                try:
                    # Explicit wait for the button to be clickable
                    notification_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[text()='Turn on notifications'])[2]"))
                    )
                    print("Turn on notifications button is clickable")

                    # Click the "Turn on notifications" button
                    notification_button.click()

                    wait_for_page_load(driver)

                except Exception as e:
                    print("Not click notification")
                    notification_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[text()='Turn on notifications'])"))
                    )
                    print("Turn on notifications button is clickable")

                    # Click the "Turn on notifications" button
                    notification_button.click()

                    wait_for_page_load(driver)

                try:
                    # Explicit wait for the button to be clickable
                    notification_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "(//span[text()='Turn on notifications'])[2]"))
                    )
                    print("Turn on notifications button is clickable")

                    # Click the "Turn on notifications" button
                    notification_button.click()

                    wait_for_page_load(driver)

                except Exception as e:
                    # Explicit wait for the "Skip" button to be clickable
                    skip_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[text()='Skip']"))
                    )
                    print("Skip button is clickable")

                    # Click the "Skip" button
                    skip_button.click()

                    # Wait for any further action to complete (if necessary)
                    time.sleep(0.5)

                    wait_for_page_load(driver)
                

                

                try:
                    # Explicit wait for the "Skip" button to be clickable
                    skip_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[text()='Skip']"))
                    )
                    print("Skip button is clickable")

                    # Click the "Skip" button
                    skip_button.click()

                    # Wait for any further action to complete (if necessary)
                    time.sleep(0.5)

                except Exception as e:
                                    # Explicit wait for the "Skip" button to be clickable
                    skip_button = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[text()='Skip']"))
                    )
                    print("Skip button is clickable")

                    # Click the "Skip" button
                    skip_button.click()

                    # Wait for any further action to complete (if necessary)
                    time.sleep(0.5)

                
                
                wait_for_page_load(driver)
                time.sleep(0.5)

                try:
                    # Explicit wait for the "Skip" button to be clickable using the span element text
                    skip_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Skip']"))
                    )
                    print("Skip button is clickable")

                    # Click the "Skip" button
                    skip_button.click()

                    # Wait for any further action to complete (if necessary)
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error: {e}")

                wait_for_page_load(driver)
                time.sleep(0.5)
            
            except Exception as e:
                print(f"Error loading cookies: {e}")
            
            wait_for_page_load(driver)
            time.sleep(0.5)
            
            folder_path = "D:\\software\\tool reg\\cookies"
            file_name = f"n3w.mmo+{first_name}{last_name}"

            # save_cookies(driver, folder_path, file_name)
            save_cookies(driver, folder_path, f"{file_name}.pkl")
            print("save cookies success")
            # time.sleep(250)
        
        except Exception as e:
            print(f"Acc Check Point")

    except Exception as e:
        print(f"Error loading cookies: {e}")
