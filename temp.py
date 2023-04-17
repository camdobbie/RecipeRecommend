import pandas as pd

#load Categories_Ingredients/Canned_foods.csv as a pandas dataframe
df = pd.read_csv('Categories_Ingredients/Meats_and_seafood.csv')

print(df)

#create a dictionary with raw_ingredients as the keys and simplified_ingredients as the values
d = dict(zip(df.raw_ingredients, df.simplified_ingredients))

print(d)
