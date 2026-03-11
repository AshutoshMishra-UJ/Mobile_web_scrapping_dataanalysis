# open google.com
# search campusx
# learnwith.campusx.in
# dsmp course page
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configure Chrome options to avoid detection
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

s = Service(r"C:\Users\ashut\OneDrive\Desktop\chromedriver.exe")

driver = webdriver.Chrome(service=s, options=chrome_options)

# Make browser appear more human-like
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

driver.get('http://google.com')
print("If CAPTCHA appears, please solve it manually. Waiting 10 seconds...")
time.sleep(10)

# fetch the search input box using name attribute (more reliable)
user_input = driver.find_element(by=By.NAME, value='q')
user_input.send_keys('Campusx')
time.sleep(1)

user_input.send_keys(Keys.ENTER)
time.sleep(3)

# Find the link containing 'campusx' in the URL using CSS selector
link = driver.find_element(by=By.CSS_SELECTOR, value='a[href*="campusx"]')
link.click()

time.sleep(3)

# Find the courses link - using a more flexible approach
link2 = driver.find_element(by=By.PARTIAL_LINK_TEXT, value='Courses')
link2.click()

time.sleep(2)
