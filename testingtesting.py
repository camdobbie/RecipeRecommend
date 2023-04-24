import pandas as pd
df = pd.read_csv('ingredients_150_recipes.csv')
#for all ingredients in the raw_ingredients column, remove any spaces at the beginning or end of the string, but not in the middle
df['raw_ingredients'] = df['raw_ingredients'].str.strip()
#replace original csv with new csv
df.to_csv('ingredients_150_recipes.csv', index=False)