# %%
import pandas as pd
import numpy as np

df = pd.read_csv('ingredients_simplified.csv')
unique_ingredients,counts = np.unique(df['simplified_ingredients'], return_counts = True)
# order the ingredients by the number of times they appear
unique_ingredients = unique_ingredients[np.argsort(counts)[::-1]]
ingredients_counts = counts[np.argsort(counts)[::-1]]
# %%
# create a dataframe with the ingredients, items and price
ingredients_df = pd.DataFrame(columns = ['recipe_id', 'section', 'ingredient', 'item', 'price', 'quantity'])
each_exceptions = ['Jar', 'Cucumber', 'Baguettes', 'Greens', 'Lettuce', 'wine']
# loop through the ingredients
for i in range(len(unique_ingredients)):
    # get the ingredient
    ingredient = unique_ingredients[i]
    # get the rows where the ingredient appears
    rows = df.loc[df['simplified_ingredients'] == ingredient]
    # get the items and prices
    ids = rows['recipe_id'].values
    section = np.unique(rows['section'].values)
    # strip square brackets from the section
    section = section[0].replace('[','').replace(']','')
    items = rows['item'].values   
    # find prices
    prices = rows['price'].values
    # loop through the items and prices
    for j in range(len(items)):
        # divide the price by the quantity and add pound sign to the front
        try:
            prices[j] = '£' + str(float(prices[j].replace("£",""))/float(rows['quantity'].values[j]))
        except:
            prices[j] = '£' + str(float(prices[j])/float(rows['quantity'].values[j]))
        # get the quantity
        item = items[j]
        # split at the comma
        item = item.split(',')
        # retrieve the first element
        item = item[0]
        # get last word
        if item.split(' ')[-2] == 'Class':
            quantity = item.split(' ')[-3]
        else:
            quantity = item.split(' ')[-1]
        if quantity in each_exceptions:
            quantity = 'Each'
        if quantity == "++" or '-' in quantity.split() or quantity == 'Stems' or quantity == "Pack":
            quantity = item.split(' ')[-2]
        if quantity == "Wraps" or quantity == "Bread":
            quantity = item.split(' ')[1]
        # add the ingredient, item and price to the dataframe
        ingredients_df.loc[len(ingredients_df)] = [str(ids), section , ingredient, items[j], prices[j], quantity]
# sort by ingredient name then price (ascending)
ingredients_df = ingredients_df.sort_values(by=['ingredient', 'price'])
# only keep the first instance of each ingredient
ingredients_df = ingredients_df.drop_duplicates(subset=['ingredient'], keep='first')
# save the dataframe as a csv file
ingredients_df.to_csv('unique_ingredients.csv', index = False)
# %%
# plot the frequency of each ingredient
import matplotlib.pyplot as plt
plt.bar(unique_ingredients[:20], ingredients_counts[:20])
plt.xticks(rotation=90)
plt.xlabel('Ingredient')
plt.ylabel('Frequency')
plt.title('Frequency of top 20 ingredients')
plt.show()

# find ingredients that are in fruits and vegetables
fruits_vegetables = ingredients_df.loc[ingredients_df['section'] == 'Fruits and vegetables']
fruits_freq_df = pd.DataFrame(columns = ['ingredient', 'frequency'])
for i in range(len(fruits_vegetables)):
    fruits_freq_df.loc[i,'ingredient'] = fruits_vegetables['ingredient'].values[i]
    fruits_freq_df.loc[i,'frequency'] = len(fruits_vegetables['recipe_id'].values[i].strip('[]').strip().split(' '))
# sort by frequency (descending)
fruits_freq_df = fruits_freq_df.sort_values(by=['frequency'], ascending = False)
# plot the frequency of each ingredient
plt.bar(fruits_freq_df['ingredient'].values[:20], fruits_freq_df['frequency'].values[:20])
plt.xticks(rotation=90)
plt.xlabel('Ingredient')
plt.ylabel('Frequency')
plt.title('Frequency of top 20 ingredients in fruits and vegetables')
plt.show()

# Do the same for meat and seafood
meat_fish = ingredients_df.loc[ingredients_df['section'] == 'Meats and seafood']
meat_freq_df = pd.DataFrame(columns = ['ingredient', 'frequency'])
for i in range(len(meat_fish)):
    meat_freq_df.loc[i,'ingredient'] = meat_fish['ingredient'].values[i]
    meat_freq_df.loc[i,'frequency'] = len(meat_fish['recipe_id'].values[i].strip('[]').strip().split(' '))
# sort by frequency (descending)
meat_freq_df = meat_freq_df.sort_values(by=['frequency'], ascending = False)
# plot the frequency of each ingredient
plt.bar(meat_freq_df['ingredient'].values[:20], meat_freq_df['frequency'].values[:20])
plt.xticks(rotation=90)
plt.xlabel('Ingredient')
plt.ylabel('Frequency')
plt.title('Frequency of top 20 ingredients in meat and seafood')
plt.show()

# %%
# plot the frequency of each section
unique_sections,sections_counts = np.unique(ingredients_df['section'].values, return_counts = True)
unique_sections = unique_sections[np.argsort(sections_counts)[::-1]]
sections_counts = sections_counts[np.argsort(sections_counts)[::-1]]
plt.figure(figsize=(10,5))
plt.bar(unique_sections, sections_counts)
plt.xticks(rotation=90)
plt.xlabel('Section')
plt.ylabel('Frequency')
plt.title('Frequency of sections')
plt.show()
# plot price distribution
prices = ingredients_df['price'].values
prices = [float(price.replace('£','')) for price in prices]
plt.figure(figsize=(10,5))
plt.hist(prices, bins = 100)
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.title('Price distribution')
plt.show()
# %%