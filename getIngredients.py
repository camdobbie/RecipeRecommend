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

# remove all but the top 10 urls
df = df.head(5)

allIngredients = []



for i in range(len(df)):
    url = df['url'][i]
    
    # Set the path to the ChromeDriver executable
    chromedriver_path = "path/to/chromedriver"

    # Initialize the Chrome browser driver
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(url)

    # Find and click the button
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '103c201c125624b4bd4b0fba657b8fa1a84')))
    button.click()

    # Wait until there is a button with data-testid "list-checkout-add-to-retailer-cart-button"
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="list-checkout-add-to-retailer-cart-button"]')))

    # Get the page source (HTML code) and print it
    html = driver.page_source

    # Close the browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    items_df = pd.DataFrame(columns = ['item', 'ingredient', 'quantity'])
    items = {}
    ingredients = {}
    quantities = {}

    # find first heading
    headings = soup.find_all('div')
    for heading in headings:
        if heading.get('role') == 'heading':
            column = heading.text
            if column == 'Uncategorised':
                break
        elif heading.get('role') == 'listitem':
            quantity = heading.find('input').get('value')
            if quantity != '0':
                item = heading.find('span', attrs={'data-testid': 'list-checkout-item'}).text
                ingredient = heading.find('div', attrs={'class': 'sc-gfiwwq gGwesG'}).text
                try:
                    items[column].append(item)
                except:
                    items[column] = [item]
                try:
                    ingredients[column].append(ingredient)
                except:
                    ingredients[column] = [ingredient]
                try:
                    quantities[column].append(quantity)
                except:
                    quantities[column] = [quantity]
        else:
            pass
    # add items, ingredients and quantities to df
    for key in items:
        df.loc[i,f'{key}-item'] = str(items[key])
        df.loc[i,f'{key}-ingredient'] = str(ingredients[key])
        df.loc[i,f'{key}-quantity'] = str(quantities[key])
    # add price to df
    price = soup.find('div', attrs={'class': 'sc-1errw5p gSHsGZ'}).text
    df.loc[i,'price'] = price

column_to_move = df.pop("price")
df.insert(1, "price", column_to_move)

#save df to csv
df.to_csv('ingredients2.csv', index = False)