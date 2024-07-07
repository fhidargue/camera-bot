import time
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

# Load local environment - .env file
load_dotenv()

# Constant variables
BEST_BUY = "bestbuy"
BH_PHOTO_VIDEO = "bhphotovideo"
HOT_ROD_CAMERAS = "hotrodcameras"
FUJIFILM = "shopusa.fujifilm"
ADD_TO_CART = "Add to Cart"
TIMEOUT = 5

sender_email = os.getenv('SENDER_EMAIL')
sender_pass = os.getenv('SENDER_PASS')
receiver_email = os.getenv('RECEIVER_EMAIL')

# Be sure to map all links from the .env file here
urls = [
    os.getenv('BEST_BUY_BLACK'),
    os.getenv('BEST_BUY_SILVER'),
    os.getenv('HOT_ROD'),
    os.getenv('BH_BLACK'),
    os.getenv('BH_SILVER'),
    os.getenv('FUJIFILM'),
]

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Function definitions 
def wait_for_page_load(driver, timeout=TIMEOUT):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def print_button_status(url, available):
    if available:
        print(f"{ADD_TO_CART} button is available at {url}")
    else:
        print(f"{ADD_TO_CART} button is not available at {url}")

def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())

def handle_url_completion(index):
    urls.pop(index)

# Open valid urls
if urls[0]:
    driver.get(urls[0])
else:
    print("First URL is empty, exiting.")
    driver.quit()
    exit()

try:
    while True:
        for index, url in enumerate(urls[:]):
            if not url:
                continue  

            if index > 0:
                driver.switch_to.window(driver.window_handles[0])
                driver.get(url)
            else:
                driver.get(url)

            wait_for_page_load(driver, timeout=TIMEOUT)
            print('----------------------')
    
            if BEST_BUY in driver.current_url:
                try:
                    us_button = WebDriverWait(driver, TIMEOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'us-link'))
                    )
                    us_button.click()
                    wait_for_page_load(driver, timeout=TIMEOUT)
                except:
                    pass

                try:
                    add_to_cart_button = WebDriverWait(driver, TIMEOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'add-to-cart-button'))
                    )
                    button_text = add_to_cart_button.text.strip()
                    if ADD_TO_CART in button_text:
                        print_button_status(driver.current_url, True)
                        send_email(f"{ADD_TO_CART} Available", f"Camera available NOW in: {driver.current_url}")
                        handle_url_completion(index)
                        break
                    else:
                        print_button_status(driver.current_url, False)
                except:
                    print_button_status(driver.current_url, False)
            elif BH_PHOTO_VIDEO in driver.current_url:
                try:
                    add_to_cart_button = WebDriverWait(driver, TIMEOUT).until(
                        EC.presence_of_element_located((By.XPATH, '//button[@data-selenium="addToCartButton"]'))
                    )
                    print_button_status(driver.current_url, True)
                    send_email(f"{ADD_TO_CART} Available", f"Camera avaibale NOW in: {driver.current_url}")
                    handle_url_completion(index)
                    break
                except:
                    print_button_status(driver.current_url, False)
            elif HOT_ROD_CAMERAS in driver.current_url:
                try:
                    add_to_cart_button = WebDriverWait(driver, TIMEOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'product-form--atc-button'))
                    )
                    button_text = add_to_cart_button.text.strip()

                    if ADD_TO_CART in button_text:
                        print_button_status(driver.current_url, True)
                        send_email(f"{ADD_TO_CART} Available", f"Camera avaibale NOW in: {driver.current_url}")
                        handle_url_completion(index)
                        break
                except:
                    print_button_status(driver.current_url, False)
            elif FUJIFILM in driver.current_url:
                add_to_cart_button = WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.ID, 'product-addtocart-button'))
                )
                button_text = add_to_cart_button.text.strip()

                # This website has an upper cased copy for Add to Cart
                if ADD_TO_CART.upper() in button_text:
                    print_button_status(driver.current_url, True)
                    send_email(f"{ADD_TO_CART} Available", f"Camera avaibale NOW in: {driver.current_url}")
                    handle_url_completion(index)
                    break
                else:
                    print_button_status(driver.current_url, False)
            else:
                print('No valid URLs to check.')

        time.sleep(TIMEOUT)

        if not urls:
            print("No more URLs to check. Exiting.")
            break
except KeyboardInterrupt:
    print('Stopping the bot...')
finally:
    driver.quit()