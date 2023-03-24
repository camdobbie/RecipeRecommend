from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = 'https://tesco.list-integration.whisk.com/stateless-checkout?recipes=%5B%7B"recipeUrl"%3A"https%3A%2F%2Frealfood.tesco.com%2Frecipes%2Follys-thank-you-finest-burgers.html"%7D%5D'

# Set the path to the ChromeDriver executable
chromedriver_path = "path/to/chromedriver"

# Initialize the Chrome browser driver
driver = webdriver.Chrome()

# Navigate to the URL
driver.get(url)

# Find and click the button
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '103c201c125624b4bd4b0fba657b8fa1a84')))
button.click()

""" # Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
 """

# Wait until there is a button with data-testid "list-checkout-add-to-retailer-cart-button"
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="list-checkout-add-to-retailer-cart-button"]')))

# Get the page source (HTML code) and print it
html = driver.page_source

# Close the browser
driver.quit()

soup = BeautifulSoup(html, 'html.parser')

ings = soup.find_all('div', attrs={'class': 'sc-1c5wdcd lfbNqY'})
for ing in ings:
    print(ing.text)

    