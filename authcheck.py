from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
# Remove headless mode so the user can interact with the browser
chrome_options.add_argument("--start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open Bing
driver.get("https://www.bing.com")

# Wait for the user to log in manually
print("Please log in to Bing manually and press Enter here when done...")
input()

# Get the cookie value
cookies = driver.get_cookies()
u_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == '_U'), None)

# Print the cookie value
print(f"_U cookie value: {u_cookie}")

# Close the browser
driver.quit()