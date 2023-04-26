# %%
import numpy as np
import pandas as pd
import glob

# read all the csv files in the categories_ingredients folder
df = pd.concat([pd.read_csv(f) for f in glob.glob('categories_ingredients/*.csv')], ignore_index = True)

# replace ingredient column with simplified_ingredients column and remove the simplified ingredient column
df = df.drop(columns = ['ingredient'])

# strip the whitespace from the simplified ingredient column
df['simplified_ingredients'] = df['simplified_ingredients'].str.strip()

# remove the rows with recipe_id = 2 and 48
df = df.loc[df['recipe_id'] != 2]
df = df.loc[df['recipe_id'] != 48]

# order the dataframe by recipe_id and section
df = df.sort_values(by=['recipe_id'])
# save the dataframe as a csv file
df.to_csv('ingredients_simplified.csv', index = False)
# %%