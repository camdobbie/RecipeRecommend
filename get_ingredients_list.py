# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:08:00 2023

@author: sita_
"""

import pandas as pd

data=pd.read_csv('ingredients_next_50.csv')
data.head()

ingredients = data['ingredient']

#starts from 0!!!
#want 1 column with amount, 1 with ingredient and 1 with basic ingredient 


for i in range(0,len(ingredients)):
    ingredients[i] = ingredients[i].lower()
    
#separates each word in each ingredient 
sep_ing = []
for i in range(0,len(ingredients)):
    array = ingredients[i]
    array = array.split()
    sep_ing.append(array)

#merges tbsp etc with number to get quantity as 1 string - if we add more recipes we will need to see if there are any other measurement words   
units = ['tsp', 'tbsp', 'head', 'cm', 'leaves', 'bunch', 'sticks', 'tin', 'tins','bulb','clove','cloves','stick','stalk','teaspoon','tablespoon','heaped teaspoon','heaped tablespoon','ltr','lt','can','sprig','sprigs']
for j in range(len(sep_ing)):
    arr = sep_ing[j]
    i = 1
    while i < len(arr):
        if any(unit in arr[i] for unit in units):
            arr[i-1] = arr[i-1] + ' ' + arr[i]
            arr.pop(i)
        else:
            i += 1
    sep_ing[j] = arr
    
#separating all the quantities 
quantities = []
for i in range(0,len(sep_ing)):
    strings = sep_ing[i]
    quantity = []
    for string in strings:
        for character in string:
            if character.isdigit():
                quantity.append(string)
                sep_ing[i].remove(string)
                break
    if len(quantity) == 0:
        quantities.append([])
    else:
        quantities.append(quantity)
   
    
data['quantities'] = quantities

merged = [' '.join(item) for item in sep_ing]
data['raw_ingredients'] = merged

data.to_csv('ingredients_next_50.csv', index=False)





