# Setup
import os
import glob
import time
import datetime as dt

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from node_list import node_urls

hanmi_folder = r'C:\Users\user\Downloads\hanmi_automation'
if not os.path.exists(hanmi_folder):  # Create hanmi_automation folder if it doesn't exist
    os.makedirs(hanmi_folder)

prefs = {
    "detach": True,
    "download.default_directory": hanmi_folder,
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open login page
driver.get("redacted") # Removed for privacy
time.sleep(1)
driver.find_element(By.ID, value="details-button").click()  # Advanced button
time.sleep(1)
driver.find_element(By.ID, value="proceed-link").click()  # Proceed link
time.sleep(1)

# Login
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
username_input = driver.find_element(By.NAME, value="ctl00$BodyContent$Username")
username_input.send_keys(username)
password_input = driver.find_element(By.NAME, value="ctl00$BodyContent$Password")
password_input.send_keys(password)
time.sleep(1)
driver.find_element(By.CLASS_NAME, value="sw-btn-t").click()
time.sleep(1)

# Go through each node URL, set start/end date, download CSV (not included on GitHub repo)
for node in node_urls:
    print(f"Current node: {node}\nURL: {node_urls[node]}")
    driver.get(node_urls[node])
    driver.execute_script("window.onbeforeunload = function() {};")
    time.sleep(15)  # Wait for graph to load before clicking timeframe-picker link
    if "CPU" in node:
        time.sleep(20)  # Extra time since CPU graphs take longer to load
    try:
        driver.find_element(By.CLASS_NAME, value="nui-text-link").click()
    except selenium.common.exceptions.ElementNotInteractableException:
        continue
    time.sleep(5)

    # Start and end date adjustments
    today = dt.date.today()
    mn_const_str = 0
    mn_const_end = 0
    yr_const_str = 0
    yr_const_end = 0
    if dt.date.today().month == 1:
        yr_const_str = 1  # Subtract a year from start date if running in January
        mn_const_str = -12
        if dt.date.today().day < 25:
            yr_const_end = 1  # Subtract a year from start date if running in Jan before 25th
            mn_const_str = -11
            mn_const_end = -11
        else:
            month_const = -12
    elif dt.date.today().month == 2:
        if dt.date.today().day < 25:
            yr_const_str = 1  # Subtract a year from start date if running in Feb before 25th
            mn_const_str = -11
            mn_const_end = 1
    else:
        if dt.date.today().day < 25:
            mn_const_str = 1  # Subtract an extra month if running before the 25th
            mn_const_end = 1

    # Set start and end dates
    start_date = driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[2]/div/div/nui-popover-modal/div/div/"
                                                     "div[2]/div/div/nui-quick-picker/div/div[3]/nui-time-frame-picker/"
                                                     "div/div/span[1]/nui-date-time-picker/div/div[1]/nui-date-picker/"
                                                     "div/div[1]/nui-textbox/div/div/input")
    start_date.send_keys(Keys.CONTROL, "A")
    start_date.send_keys(Keys.DELETE)
    start_date.send_keys(str(today.month - 1 - mn_const_str), "/", str(25), "/", str(today.year - yr_const_str))
    driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[2]/div/div/nui-popover-modal/div/div/div[2]/div/div/"
                                        "nui-quick-picker/div/div[3]/nui-time-frame-picker/div/div/span[1]/"
                                        "nui-date-time-picker/div/div[1]/nui-date-picker/div/div[1]/nui-icon/i/div/"
                                        "div").click()
    time.sleep(1)

    end_date = driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[2]/div/div/nui-popover-modal/div/div/"
                                                   "div[2]/div/div/nui-quick-picker/div/div[3]/nui-time-frame-picker/"
                                                   "div/div/span[2]/nui-date-time-picker/div/div[1]/nui-date-picker/"
                                                   "div/div[1]/nui-textbox/div/div/input")
    end_date.send_keys(Keys.CONTROL, "A")
    end_date.send_keys(Keys.DELETE)
    end_date.send_keys(str(today.month - mn_const_end), "/", str(25), "/", str(today.year - yr_const_end))
    driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[2]/div/div/nui-popover-modal/div/div/div[2]/div/div/"
                                        "nui-quick-picker/div/div[3]/nui-time-frame-picker/div/div/span[1]/"
                                        "nui-date-time-picker/div/div[1]/nui-date-picker/div/div[1]/nui-icon/i/div/"
                                        "div").click()
    time.sleep(1)

    driver.find_element(By.XPATH, value="/html/body/div[2]/div/div[2]/div/div/nui-popover-modal/div/div/div[2]/div/"
                                        "nui-dialog-footer/div/button[2]").click()  # Use button
    time.sleep(5)
    if "CPU" in node:
        time.sleep(20)  # Extra time since CPU graphs take longer to load

    driver.find_element(By.XPATH, value="/html/body/sw-os-root/fdk-orion-website-wrapper/fdk-orion-website/div/div/div/"
                                        "sw-os-perfstack-view/nui-sheet/nui-card/div/div/nui-toolbar/div/div[2]/"
                                        "nui-toolbar-group/nui-menu[2]/nui-popup/div/div[1]/button").click()  # Menu
    driver.find_element(By.XPATH, value="/html/body/sw-os-root/fdk-orion-website-wrapper/fdk-orion-website/div/div/div/"
                                        "sw-os-perfstack-view/nui-sheet/nui-card/div/div/nui-toolbar/div/div[2]/"
                                        "nui-toolbar-group/nui-menu[2]/nui-popup/div/div[2]/div/div/div/div/div/div/"
                                        "div/div/nui-menu-group[1]/nui-menu-action[2]/a").click()  # Export button
    time.sleep(5)
    folder_path = hanmi_folder
    file_type = r"\*csv"
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)
    print(max_file)
    os.rename(max_file, fr"{hanmi_folder}\{node}.csv")
    time.sleep(5)
