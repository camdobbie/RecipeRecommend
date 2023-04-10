from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# load dinner_list.txt as a column in a dataframe with the column title being url
df = pd.read_csv('dinner_list.txt', sep = '/', header = None, usecols = [4])
df.columns = ['url']

# add https://tesco.list-integration.whisk.com/stateless-checkout?recipes=%5B%7B"recipeUrl"%3A"https%3A%2F%2Frealfood.tesco.com%2Frecipes%2F to the beginning and "%7D%5D to the end of each url
df['url'] = 'https://tesco.list-integration.whisk.com/stateless-checkout?recipes=%5B%7B"recipeUrl"%3A"https%3A%2F%2Frealfood.tesco.com%2Frecipes%2F' + df['url'] + '"%7D%5D'

info_df = pd.DataFrame(columns = ['recipe_id' , 'section', 'item', 'ingredient', 'quantity', 'price'])

j = 0
for i in range(150):
    print(i)
    url = df['url'][i]
    
    # Set the path to the ChromeDriver executable
    chromedriver_path = "path/to/chromedriver"

    # Initialize the Chrome browser driver
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(url)

    # Find and click the button
    button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, '103c201c125624b4bd4b0fba657b8fa1a84')))
    button.click()

    # Wait until there is a button with data-testid "list-checkout-add-to-retailer-cart-button"
    button = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="list-checkout-add-to-retailer-cart-button"]')))

    # Get the page source (HTML code) and print it
    html = driver.page_source

    # Close the browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    headings = soup.find_all('div')
    for heading in headings:
        if heading.get('role') == 'heading':
            section = heading.text
            if section == 'Uncategorised':
                break
        elif heading.get('role') == 'listitem':
            try:
                quantity = heading.find('input').get('value')
            except:
                quantity = '0'
            if quantity != '0':
                item = heading.find('span', attrs={'data-testid': 'list-checkout-item'}).text
                ingredient = heading.find('div', attrs={'class': 'sc-gfiwwq gGwesG'}).text
                price = heading.find('div', attrs={'class': 'sc-18zubgw ioKGjp'}).text

                info_df.loc[j,'recipe_id'] = i
                info_df.loc[j,'section'] = section
                info_df.loc[j,'item'] = item
                info_df.loc[j,'ingredient'] = ingredient
                info_df.loc[j,'quantity'] = quantity
                info_df.loc[j,'price'] = price
                j += 1
        else:
            pass

# #save df to csv
info_df.to_csv('ingredients_150_recipes.csv', index = False)