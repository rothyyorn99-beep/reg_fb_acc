import threading
import time
import logging
import os
from library import load_device_credentials, save_cookies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from page_load import wait_for_page_load
from reg_action import Reg_account
from browser_reg import Reg_account_browser
from fake_useragent import UserAgent
from library import switch_wifi_or_dcom, connect_nordvpn

# Load Random User Agent
ua = UserAgent()

# Path to your Firefox Driver executable
chromedriver_path = r"D:\Automate master\firefox_profile\chromedriver.exe"

# Screen dimensions
screen_width, screen_height = 1920, 1080
x_offset, y_offset = 0, 0
width, height = 315, 530  # Desired content size
per_row = 6

# Global variables
MAX_THREADS = 12
active_threads = 0
lock = threading.Lock()
available_positions = []

# Helper to measure outer window size (titlebar + borders)

# Calculate grid positions for browsers
def calculate_positions():
  """
  Calculate all positions for browsers based on screen size and window dimensions.
  """
  positions = []
  for row in range(screen_height // height):
    for col in range(per_row):
      pos_x = x_offset + col * width
      pos_y = y_offset + row * height

      # Ensure that position is within screen bounds
      if pos_y + height > screen_height or pos_x + width > screen_width:
        break
      positions.append((pos_x, pos_y))

  return positions

# Open a single browser in a thread
def open_browser_in_thread(browser_id,device,user_agent, pos_x, pos_y):
  global active_threads
  driver = None # Initialize driver to None
 
  try:
    with lock:
      active_threads += 1
    # --- SWITCH Wi-Fi / DCOM ---
    print(user_agent)

    # Set Chrome options
    options = Options()
    
    options.add_argument("--headless=new")   # or "--headless" for older versions
    options.add_argument(f"--window-size={width},{height}") # Set window size before browser opens
    options.add_argument(f"--window-position={pos_x},{pos_y}") # Optional: Set window position
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(f'https://web.facebook.com/r.php?entry_point=login')
        logging.info("Home page refreshed.")
    except Exception as e:
        logging.error(f"Error refreshing home page: {e}")
    wait_for_page_load(driver)

    # time.sleep(5000)
    # view_youtube(driver)
    Reg_account_browser(driver)

    # time.sleep(5)

  except Exception as e:
    print(f"Error opening browser {browser_id}: {e}")
  finally:
    if driver:
      driver.quit() # Close the browser session if it was started
    print(f"Browser {browser_id} closed.")

    # Update thread count and re-add position after the browser is closed
    with lock:
      available_positions.append((pos_x, pos_y))
      time.sleep(0.5)
      active_threads -= 1
    print(f"Active Threads after closing browser {browser_id}: {active_threads}")

# Manage all browsers with threading
def manage_browsers(num_browsers, file_device):
    global active_threads
    threads = []
    total_positions = calculate_positions()

    with lock:
        available_positions.extend(total_positions)

    next_browser_id = 0

    while next_browser_id < num_browsers or any(t.is_alive() for t in threads):
        with lock:
            if active_threads < MAX_THREADS and next_browser_id < num_browsers:
                if available_positions:
                    pos_x, pos_y = available_positions.pop(0)
                    device = load_device_credentials(file_device, randomize=True)
                    user_agent = ua.firefox

                    thread = threading.Thread(
                        target=open_browser_in_thread,
                        args=(next_browser_id, device, user_agent, pos_x, pos_y)
                    )
                    threads.append(thread)
                    thread.start()
                    next_browser_id += 1
        time.sleep(0.5)

    for thread in threads:
        thread.join()

    print("All browsers are closed.")

# Main execution
if __name__ == "__main__":
    num_browsers = 500  # Number of browsers to open
    file_device = r'D:\Automate master\firefox_profile\user_agent.txt'
    manage_browsers(num_browsers, file_device)
