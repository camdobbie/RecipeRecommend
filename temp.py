import pandas as pd

cats = ["Baking", "Bread_and_bakery", "Breakfast_foods", "Canned_foods", "Condiments", "Dairy_and_eggs", "Drinks", "Frozen", "Fruits_and_vegetables", "Herbs_and_spices", "Meats_and_seafood", "Other", "Pasta_rice_and_beans", "Snacks"]

def makeDict(category):
    #load Categories_Ingredients/Canned_foods.csv as a pandas dataframe
    df = pd.read_csv(f'Categories_Ingredients/{category}.csv')

    #print(df)
    print(df.shape)

    #create a dictionary with raw_ingredients as the keys and simplified_ingredients as the values
    d = dict(zip(df.raw_ingredients, df.simplified_ingredients))

    # create a df of the keys and values
    df2 = pd.DataFrame(list(d.items()), columns=['raw_ingredients', 'simplified_ingredients'])
    #print the size of the df

    #save the df as a csv file
    df2.to_csv(f'Dictionaries/{category}.csv', index=False)

for cat in cats:
    makeDict(cat)

