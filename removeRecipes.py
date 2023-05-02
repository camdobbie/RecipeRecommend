import pandas as pd

# list of recipes to remove
remove = [26,31,72,78,92,131]
# read in recipes
recipes = pd.read_csv('recipes_150_recipes.csv')
ingredients = pd.read_csv('ingredients_simplified.csv')
# remove recipes
recipes = recipes[~recipes['recipe_id'].isin(remove)]
# remove ingredients
ingredients = ingredients[~ingredients['recipe_id'].isin(remove)]
# write to csv
recipes.to_csv('recipes_reduced.csv', index=False)
ingredients.to_csv('ingredients_reduced.csv', index=False)