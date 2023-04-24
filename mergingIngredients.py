# %%
import numpy as np
import pandas as pd
import glob

# read all the csv files in the categories_ingredients folder
df = pd.concat([pd.read_csv(f) for f in glob.glob('categories_ingredients/*.csv')], ignore_index = True)

# replace ingredient column with simplified_ingredients column and remove the simplified ingredient column
df['ingredient'] = df['simplified_ingredients']
df = df.drop(columns = ['simplified_ingredients','raw_ingredients'])

# remove the rows with recipe_id = 2 and 48
df = df.loc[df['recipe_id'] != 2]
df = df.loc[df['recipe_id'] != 48]

# order the dataframe by recipe_id and section
df = df.sort_values(by=['recipe_id'])
# save the dataframe as a csv file
df.to_csv('ingredients_simplified.csv', index = False)
# %%
unique_ingredients,counts = np.unique(df['ingredient'], return_counts = True)
# order the ingredients by the number of times they appear
unique_ingredients = unique_ingredients[np.argsort(counts)[::-1]]
counts = counts[np.argsort(counts)[::-1]]
# %%
# create a dataframe with the ingredients, items and price
ingredients_df = pd.DataFrame(columns = ['ingredient', 'item', 'price'])
# loop through the ingredients
for i in range(len(unique_ingredients)):
    # get the ingredient
    ingredient = unique_ingredients[i]
    # get the rows where the ingredient appears
    rows = df.loc[df['ingredient'] == ingredient]
    # get the items and prices
    items = rows['item'].values
    prices = rows['price'].values
    # loop through the items and prices
    for j in range(len(items)):
        # divide the price by the quantity and add pound sign to the front
        try:
            prices[j] = '£' + str(float(prices[j].replace("£",""))/float(rows['quantity'].values[j]))
        except:
            prices[j] = '£' + str(float(prices[j])/float(rows['quantity'].values[j]))
        # add the ingredient, item and price to the dataframe
        ingredients_df.loc[len(ingredients_df)] = [ingredient, items[j], prices[j]]
# %%
