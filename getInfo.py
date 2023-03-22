import pandas as pd
import numpy as np

def getInfo():
    """Function to return the titles, ingredients and servings of the recipes

    Returns:
        list: returns a list of dictionaries (titles, ingredients ,servings)
    """    
    df = pd.read_csv("Tesco_Dinners.csv",usecols=["Title","Ingredients","Servings"])
    titles_dict = {}
    ingredient_dict = {}
    servings_dict = {}
    for i,lst in enumerate(df['Ingredients'].values[0]):
        titles_dict[i] = df.loc[i,'Title']
        ingredient_dict[i] = (df.loc[i,'Ingredients'].strip("[]").split("'"))
        ingredient_dict[i] = [x for x in ingredient_dict[i] if (x != "") & (x != ", ")]
        servings_dict[i] = df.loc[i,'Servings']
    return titles_dict,ingredient_dict,servings_dict

if __name__ == "__main__":
    _,ingredient_dict,_ = getInfo()
    print(ingredient_dict[0])