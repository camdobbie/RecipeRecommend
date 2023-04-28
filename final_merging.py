# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:48:30 2023

@author: sita_
"""

import pandas as pd

data=pd.read_csv('unique_ingredients.csv')
data.head()

ingredients = data['ingredient']
ingredientids = data['recipe_id']
sections = data['section']

recipes=pd.read_csv('recipes_150_recipes.csv')
recipes.head()

names = recipes['name']
dietlabels = recipes['dietary']
urls = recipes['url']

# printing all the unique ingredients by section 
sectionlist = sections.tolist() 
ingredientlist = ingredients.tolist() 
section_dict = {}
for sec in set(sectionlist):
    section_dict[sec] = []
for i, ing in enumerate(ingredientlist):
    sec = sectionlist[i]
    section_dict[sec].append(ing)
 
"""
for i in range(len(ingredients)):
    if i != 27 and i != 75 and i != 250:
        print(ingredients[i])
""" 
       

# user = input('Please list any ingredients from the list above that you already have at home. We are assuming that you already have salt, black pepper and cooking oil.')
# make sure user input turns into a list like the one below 
user = ['apple','rice','pasta','cheese','pepper','mushroom','leek','coriander']       
# then add 'salt', 'black pepper' and 'cooking oil' to this list 

dietlist = ['Vegetarian', 'Vegan', 'Dairy Free', 'Gluten Free']
print('Please say if you have any of the following dietary requirements: \n')
for i in range(4):
    print(dietlist[i])
# would they just click enter if none? 
# write line that has a user input that turns it into a list like the one below called preference
preference = 'Vegetarian'
 
# finds which row of the datasets each ingredient is in
indexes = []
for i in range(len(user)):
    row_index = data.index[data['ingredient'] == user[i]][0]
    indexes.append(row_index)
    
# finds which recipes each of their ingredients are in and combines it into a list of numbers 
recipesfound = []
for i in indexes:
    recipesfound.append(ingredientids[i])
recipesfound = [''.join(recipesfound)]
recipesfound = recipesfound[0].replace('[','').replace(']','').split()
recipesfound = [int(num) for num in recipesfound]

# gets rid of the recipes that don't fit the preference 
for i in recipesfound:
    if preference not in dietlabels[i]:
        recipesfound.remove(i)

# finds the recipes that contain the highest number of these ingredients
from collections import Counter
counts = Counter(recipesfound)
most_common = counts.most_common(2) # change to 10 when more ingredients
# also shows how many times they appear 

recommend = [t[0] for t in most_common] # recipe IDs for the recipes it's recommending
# printing the final recommended recipes
for i in recommend:
    print(names[i])
    print('URL: ' + urls[i] + '\n')

# need to change this to a GUI and do them by section  
# don't include herbs and spices in taking off what they have from 2nd recipe 
