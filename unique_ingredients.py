# %%
import pandas as pd
import numpy as np
# %%
df = pd.read_csv('ingredients_simplified.csv')
unique_ingredients,counts = np.unique(df['simplified_ingredients'], return_counts = True)
# order the ingredients by the number of times they appear
unique_ingredients = unique_ingredients[np.argsort(counts)[::-1]]
counts = counts[np.argsort(counts)[::-1]]
# %%
# create a dataframe with the ingredients, items and price
ingredients_df = pd.DataFrame(columns = ['recipe_id', 'ingredient', 'item', 'price'])
# loop through the ingredients
for i in range(len(unique_ingredients)):
    # get the ingredient
    ingredient = unique_ingredients[i]
    # get the rows where the ingredient appears
    rows = df.loc[df['simplified_ingredients'] == ingredient]
    # get the items and prices
    ids = rows['recipe_id'].values
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
        ingredients_df.loc[len(ingredients_df)] = [str(ids), ingredient, items[j], prices[j]]
# sort by ingredient name then price (ascending)
ingredients_df = ingredients_df.sort_values(by=['ingredient', 'price'])
ingredients_df = ingredients_df.drop_duplicates('ingredient')
# save the dataframe as a csv file
ingredients_df.to_csv('unique_ingredients.csv', index = False)
# %%
