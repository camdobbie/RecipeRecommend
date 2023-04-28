from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# load dinner_list.txt as a column in a dataframe with the column title being url
df = pd.read_csv('dinner_list.txt', sep = '/', header = None, usecols = [4])
df.columns = ['url']
info_df = pd.DataFrame(columns = ['recipe_id' , 'name', 'servings', 'dietary'])

for i in range(150):
    print(i)
    url = 'https://realfood.tesco.com/recipes/' + df['url'][i]
    
    # Set the path to the ChromeDriver executable
    chromedriver_path = "path/to/chromedriver"

    # Initialize the Chrome browser driver
    driver = webdriver.Chrome()
    
    # Navigate to the URL
    driver.get(url)

    # Get the page source (HTML code) and print it
    html = driver.page_source

    # Close the browser
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.find('h1', attrs={'class': 'recipe-detail__headline'}).text
    servings = soup.find('li', attrs={'class': 'recipe-detail__meta-item_servings'}).text.replace('\n', '').replace('\t', '').replace('Serves', '')
    dietary_reqs = []
    # find if the recipe is vegan
    vegan = soup.find('li', attrs={'class': 'recipe-detail__meta-item_vegan'})
    if vegan is not None:
        dietary_reqs.append('Vegan')
    # find if the recipe is vegatarian
    vegetarian = soup.find('li', attrs={'class': 'recipe-detail__meta-item_vegetarian'})
    if vegetarian is not None:
        dietary_reqs.append('Vegetarian')
    # find if the recipe is gluten free
    gluten_free = soup.find('li', attrs={'class': 'recipe-detail__meta-item_gf'})
    if gluten_free is not None:
        dietary_reqs.append('Gluten Free')
    # find if the recipe is dairy free
    dairy_free = soup.find('li', attrs={'class': 'recipe-detail__meta-item_df'})
    if dairy_free is not None:
        dietary_reqs.append('Dairy Free')

    info_df.loc[i,'recipe_id'] = i
    info_df.loc[i,'name'] = title
    info_df.loc[i,'servings'] = servings
    info_df.loc[i,'dietary'] = dietary_reqs
    info_df.loc[i,'url'] = url

# save the dataframe as a csv file
info_df.to_csv('recipes_150_recipes.csv', index = False)