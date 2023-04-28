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
 
def print_section():
    for sec in set(sectionlist):
        print(f'\n{sec}:')
        for i in range(len(section_dict[sec])):
            # print the ingredients in a list making first letter of each word capital
            print(section_dict[sec][i].title())
        print('\n')

print_section()
user = []
user_input = input('Please list any ingredients from the list above that you already have at home. We are assuming that you already have salt, black pepper and cooking oil.\nHit enter to stop listing ingredients. ')
while user_input != '':
    # show the user the list of ingredients again if they type 'list'
    if user_input == 'list':
        print_section()
    # check if the ingredient is in the list of ingredients
    elif user_input in ingredients.tolist() and user_input not in user:
        user.append(user_input.lower())
    else:
        print('\nSorry, that ingredient is not in the list or you have already listed it. Please try again.')
    user_input = input('\nPlease list any ingredients from the list above that you already have at home. We are assuming that you already have salt, black pepper and cooking oil.\nHit enter to stop listing ingredients. ').lower()

# if the user doesn't have salt, black pepper or cooking oil,      
# then add 'salt', 'black pepper' and 'cooking oil' to this list
if 'salt' not in user:
    user.append('salt')
if 'black pepper' not in user:
    user.append('black pepper')
if 'cooking oil' not in user:
    user.append('cooking oil')

dietlist = ['Vegetarian', 'Vegan', 'Dairy Free', 'Gluten Free']
print('Please say if you have any of the following dietary requirements: \n')
for i in range(4):
    print(dietlist[i])

preference = input('Please enter your dietary preference from the list above. Hit enter if you have no preference. ').title()
while preference not in dietlist and preference != '':
    print('Sorry, that is not a valid dietary preference. Please try again.')
    preference = input('Please enter your dietary preference from the list above. Hit enter if you have no preference. ').title()

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
    if preference not in dietlabels[i] and preference != '':
        recipesfound.remove(i)

# finds the recipes that contain the highest number of these ingredients
from collections import Counter
counts = Counter(recipesfound)
most_common = counts.most_common(2) # change to 10 when more ingredients
# also shows how many times they appear 

recommend = [t[0] for t in most_common] # recipe IDs for the recipes it's recommending
# printing the final recommended recipes
for i in recommend:
    print(f'\n{names[i]}')
    print('URL: ' + urls[i])

# need to change this to a GUI and do them by section  
# don't include herbs and spices in taking off what they have from 2nd recipe 
