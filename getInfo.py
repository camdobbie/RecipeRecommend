import pandas as pd
import numpy as np

def getInfo():
    """Function to return the titles, ingredients and servings of the recipes

    Returns:
        list: returns a list of dictionaries
    """    
    df = pd.read_csv("Tesco_Dinners.csv",usecols=["Title","Ingredients","Servings"])
    info = []
    for i,lst in enumerate(df['Ingredients'].values[0]):
        d = {}
        d['Title'] = df.loc[i,'Title']
        d['Ingredients'] = (df.loc[i,'Ingredients'].strip("[]").split("'"))
        d['Ingredients'] = [x for x in d['Ingredients'] if (x != "") & (x != ", ")]
        d['Servings'] = df.loc[i,'Servings']
        info.append(d)
    return info

if __name__ == "__main__":
    info= getInfo()
    print(info[0])