import random
from datetime import datetime
from faker import Faker
from dateutil.relativedelta import relativedelta
import os
import pickle
import json
import csv
import subprocess
import platform
import time
# pip install faker
import random
import string
from datetime import date, timedelta
from faker import Faker

fake = Faker('en_US')

def connect_nordvpn(server=None):
    """Connect to NordVPN before launching browser."""
    try:
        if server is None:
            # random US server example
            server = "United_States"
        subprocess.run(["nordvpn", "connect", server], check=True)
        print(f"[VPN] Connected to {server}")
        time.sleep(5)  # wait for VPN to stabilize
        return True
    except Exception as e:
        print(f"[VPN ERROR] {e}")
        return False

def disconnect_nordvpn():
    try:
        subprocess.run(["nordvpn", "disconnect"], check=True)
        print("[VPN] Disconnected")
        return True
    except Exception as e:
        print(f"[VPN ERROR] {e}")
        return False

def switch_wifi_or_dcom(profile_name=None):
    """
    Switch Wi-Fi / DCOM network before launching browser.
    On Windows: uses `netsh` to switch Wi-Fi profile.
    profile_name: string of the saved Wi-Fi profile. If None, randomize.
    """
    os_type = platform.system()
    
    if os_type != "Windows":
        print("[WARN] DCOM/Wi-Fi switch currently only implemented for Windows.")
        return False

    try:
        # Get list of available Wi-Fi profiles
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, text=True
        )
        profiles = []
        for line in result.stdout.splitlines():
            if "All User Profile" in line:
                prof = line.split(":")[1].strip()
                profiles.append(prof)
        if not profiles:
            print("[WARN] No Wi-Fi profiles found.")
            return False

        if profile_name is None:
            profile_name = random.choice(profiles)

        # Connect to the chosen Wi-Fi
        subprocess.run(["netsh", "wlan", "connect", f"name={profile_name}"])
        print(f"[INFO] Switching to Wi-Fi profile: {profile_name}")
        time.sleep(5)  # Give the network a few seconds to connect
        return True
    except Exception as e:
        print(f"[ERROR] Failed to switch Wi-Fi/DCOM: {e}")
        return False
def _rand_e164_phone(force_415_555=False):
    if force_415_555:
        sub = f"{random.randint(0, 9999):04d}"
        return f"+1415555{sub}"
    # generate a realistic-looking NANP phone in +1XXXXXXXXXX
    def rand_nxx():
        return str(random.randint(2,9)) + ''.join(str(random.randint(0,9)) for _ in range(2))
    while True:
        area = rand_nxx()
        exch = rand_nxx()
        if exch[1:] != "11":
            break
    subscriber = f"{random.randint(0,9999):04d}"
    return f"+1{area}{exch}{subscriber}"

def _random_dob(min_age=18, max_age=60):
    """Return dob as YYYY-MM-DD and components. Ages inclusive."""
    today = date.today()
    start = today - timedelta(days=365*max_age)
    end   = today - timedelta(days=365*min_age)
    random_day = fake.date_between(start_date=start, end_date=end)
    return {
        "dob": random_day.isoformat(),
        "dob_year": random_day.year,
        "dob_month": random_day.month,
        "dob_day": random_day.day
    }

def _random_password(length=12):
    """Generate a password with mixed upper/lower/digits/symbols."""
    # ensure at least one of each required type
    chars = {
        "upper": random.choice(string.ascii_uppercase),
        "lower": random.choice(string.ascii_lowercase),
        "digit": random.choice(string.digits),
        "symbol": random.choice(string.punctuation),
    }
    # fill the rest
    remaining = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation)
                        for _ in range(max(0, length - len(chars))))
    pwd_list = list(remaining + ''.join(chars.values()))
    random.shuffle(pwd_list)
    return ''.join(pwd_list)[:length]

def generate_fake_profiles(n=1,
                           force_415_555_phone=False,
                           include_sensitive=False,
                           unique_emails=True,
                           password_length=12):
    """
    Generate n fake user profiles suitable for form-filling (returns dict or list of dicts).
    Args:
        n (int): number of profiles to generate
        force_415_555_phone (bool): if True, phone will be +1415555XXXX pattern
        include_sensitive (bool): if True, include SSN-like placeholder (fake only)
        unique_emails (bool): ensure emails are unique (username-based)
        password_length (int): length of generated password
    Returns:
        dict if n==1 else list[dict]
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    profiles = []
    seen_emails = set()

    for i in range(n):
        name = fake.name()
        parts = name.split()
        first = parts[0]
        last = parts[-1] if len(parts) > 1 else parts[0]
        username = (first + "." + last + str(random.randint(0,999))).lower().replace("'", "")

        # ensure email uniqueness if requested
        if unique_emails:
            email = f"{username}{random.randint(0,9999)}@{fake.free_email_domain()}"
            while email in seen_emails:
                email = f"{username}{random.randint(0,9999)}@{fake.free_email_domain()}"
            seen_emails.add(email)
        else:
            email = f"{username}@{fake.free_email_domain()}"

        dob = _random_dob()
        phone = _rand_e164_phone(force_415_555=force_415_555_phone)

        addr_lines = fake.address().split("\n")
        street = addr_lines[0]
        city = fake.city()
        state = fake.state_abbr()
        zipcode = fake.zipcode()

        profile = {
            "name": name,
            "first_name": first,
            "last_name": last,
            "username": username,
            "email": email,
            "phone_e164": phone,
            "street_address": street,
            "city": city,
            "state": state,
            "zip": zipcode,
            "dob": dob["dob"],
            "dob_year": dob["dob_year"],
            "dob_month": dob["dob_month"],
            "dob_day": dob["dob_day"],
            "company": fake.company(),
            "job": fake.job(),
        }

        if include_sensitive:
            # clearly fake SSN-like placeholder (do NOT use real SSNs)
            profile["ssn_like"] = f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"

        profiles.append(profile)

    return profiles[0] if n == 1 else profiles

def log_credentials(email, password, action, status, log_file="driver_credentials_log.csv"):
    # Ensure directory exists if a path is provided
    dir_name = os.path.dirname(log_file)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, email, password, action, status]

    # Write header if file doesn't exist
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Email", "Password", "Action", "Status"])
        writer.writerow(row)

def generate_us_name():
    # Create a Faker instance with the US locale
    fake = Faker('en_US')
    
    # Generate a random name
    random_name = fake.name()
    
    # Separate the first and last name
    first_name, last_name = random_name.split(" ", 1)
    
    return first_name, last_name
def random_year():
    """Return a random year between 1999 and 2006 (inclusive)."""
    return random.randint(1999, 2006)
def random_day():
    """Return a random integer from 1 to 28 (inclusive)."""
    return random.randint(1, 28)
def random_month_name():
    """Return a random month name, excluding May."""
    months = ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return random.choice(months)
def generate_random_number_by_country(country_code='en_US'):
    fake = Faker(country_code)
    # Generate a phone number in E.164 format
    random_number = fake.numerify(text='1##########')
    return random_number

def generate_random_date():
    # Generate a random day (1-30), month (1-12), and year (1990-2003)
    day = random.randint(1, 30)
    month = random.randint(1, 12)
    year = random.randint(1990, 2003)
    
    return day, month, year

def calculate_date_difference(start_date, end_date):
    # Calculate the difference between two dates using relativedelta
    difference = relativedelta(end_date, start_date)
    return difference

def generate_random_1_to_50():
    # Generate a random integer between 1 and 50
    return random.randint(20, 50)

def save_cookies(driver, folder_path, file_name):
    # Define the cookie file path
    cookie_file_path = os.path.join(folder_path, file_name)

    # Get all cookies from the current session without filtering
    cookies = driver.get_cookies()

    # Save all cookies to a file
    with open(cookie_file_path, 'wb') as file:
        pickle.dump(cookies, file)


def load_device_credentials(txt_file_device, randomize=False, header_name=None):
    """
    Load device credentials from a .txt file, treating each line as a full device string.

    Args:
        txt_file_device (str): Path to the .txt file.
        randomize (bool): Whether to return one random device.

    Returns:
        list or str: A list of device credentials or one random device if randomize is True.
    """
    credentials_device = []
    try:
        with open(txt_file_device, mode='r', encoding='utf-8-sig') as file:
            # Skip header if present
            lines = file.readlines()
            if lines[0].strip().lower() == f"{header_name}":
                lines = lines[1:]
            
            credentials_device = [line.strip() for line in lines if line.strip()]
        
        if not credentials_device:
            raise ValueError("No 'device' data found in the TXT file.")

        if randomize:
            return random.choice(credentials_device)
        
        return credentials_device
    
    except FileNotFoundError:
        print(f"Error: The file '{txt_file_device}' was not found.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def save_cookies_json(driver, cookies_file):
    """
    Save cookies from the current Selenium WebDriver session to a JSON file.
    """
    os.makedirs(os.path.dirname(cookies_file), exist_ok=True)  # Ensure directory exists
    with open(cookies_file, "w") as file:
        json.dump(driver.get_cookies(), file)
    print(f"✅ Cookies saved successfully to {cookies_file}!")

def load_and_apply_cookies(driver, cookies_file, url):
    """
    Load cookies from a JSON file and apply them to the given Selenium WebDriver session.
    """
    try:
        with open(cookies_file, "r") as file:
            cookies = json.load(file)
        
        driver.get(url)
        
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.refresh()
        print(f"✅ Cookies applied successfully from {cookies_file}!")
        
        if "Sign In" not in driver.page_source:
            print("✅ Successfully logged in!")
        else:
            print("❌ Login might have expired, re-authentication needed.")
    except FileNotFoundError:
        print(f"❌ Cookies file {cookies_file} not found. Please log in and save cookies first.")