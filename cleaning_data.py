import pandas as pd
import re
from pickle import dump
from itertools import takewhile, chain
from fractions import Fraction

# Read csv file
recipes = pd.read_csv(r"recipes.csv", index_col=1)
recipes.index.name = 'Recipe Name'
del recipes[recipes.columns[0]]
ingre_list = pd.read_csv(r"RAW_recipes.csv")['ingredients']

# Delete duplicate recipes
recipes = recipes.drop_duplicates()

# Create a dataframe nutritions
nutritions = recipes['nutrition']

# Clean dataframe nutritions
# Choose 3 most common nutrition in recipes: Total Fat, Total Carbohydrate, Protein
a = 'Total Fat'
b = 'Total Carbohydrate'
c = 'Protein'
for i in range(len(nutritions)):
    l = re.split(r',', nutritions[i])
    nutritions[i] = [i for i in l if (a in i) or (b in i) or (c in i)]
    for j in range(len(nutritions[i])):
        nutritions[i][j] = re.sub(r'\b\d+%', "", nutritions[i][j]) # Remove percentage number 
        nutritions[i][j] = re.sub(r'\D', "", nutritions[i][j]) # Remove other words, keep only number for gram in nutritions

# Turn nutritions type from series to dataframe
nutritions = nutritions.apply(pd.Series)

# Rename columns
nutritions.rename(columns = {nutritions.columns[0] : 'Total Fat'}, inplace = True)
nutritions.rename(columns = {nutritions.columns[1] : 'Total Carbohydrate'}, inplace = True)
nutritions.rename(columns = {nutritions.columns[2] : 'Protein'}, inplace = True)

# Replace null values with 0
nutritions.fillna('0', inplace = True)

# Convert data type from str to float
nutritions['Total Fat'] = nutritions['Total Fat'].astype(float)
nutritions['Total Carbohydrate'] = nutritions['Total Carbohydrate'].astype(float)
nutritions['Protein'] = nutritions['Protein'].astype(float)

# Create cuisine seperate series
cuisine = recipes['cuisine_path'].str.split('/', expand = True)

# Drop index and unneeded columns
cuisine = cuisine.drop([cuisine.columns[0], cuisine.columns[3], cuisine.columns[4], cuisine.columns[5]], axis = 1)

# Rename the columns
cuisine.rename(columns = {cuisine.columns[0] : 'Cuisine Category'}, inplace = True)
cuisine.rename(columns = {cuisine.columns[1] : 'Country'}, inplace = True)

# Group the cuisine into the 6 main categories
cuisine["Cuisine Category"] = cuisine["Cuisine Category"].str.replace("Fruits and Vegetables","Desserts")
cuisine["Cuisine Category"] = cuisine["Cuisine Category"].str.replace(r"Soup Recipes|Soups, Stews and Chili Recipes|Sauces and Condiments|Bread|Quick Bread Recipes|Quick Side Dish Recipes","Side Dish", regex=True)
cuisine["Cuisine Category"] = cuisine["Cuisine Category"].str.replace("Salad","Appetizers and Snacks")
cuisine["Cuisine Category"] = cuisine["Cuisine Category"].str.replace(r"Seafood|Meat and Poultry|BBQ & Grilling|Everyday Cooking|Holidays and Events Recipes|Breakfast and Brunch","Main Dishes", regex=True)

# Convert cuisine of particular country/continents/brands into dict
for i in range(len(cuisine)):
    if cuisine['Cuisine Category'][i] == 'Cuisine':
        cuisine['Cuisine Category'][i] = {cuisine['Cuisine Category'][i] : cuisine['Country'][i]}
    elif cuisine['Cuisine Category'][i] == 'Mexican':
        cuisine['Cuisine Category'][i] = {'Cuisine' : 'Latin America'}
    elif cuisine['Cuisine Category'][i] == 'Trusted Brands: Recipes and Tips':
        cuisine['Cuisine Category'][i] = {'Cuisine' : 'Brands'}

# Drop column Country
cuisine.drop('Country', axis = 1, inplace = True)

# Create dataframe directions
directions = recipes['directions']

# Remove newline space, name of the author and numbering the steps
for i in range(len(directions)):
    steps = directions[i].split('\n')
    steps = list(takewhile(lambda x: x != "", steps)) # Takes all the element that is different from ""
    steps = [steps for steps in steps if steps.strip()] 
    directions[i] = '\n'.join(f"{i+1}. {path}" for i, path in enumerate(steps))

# Turn directions type from series to dataframe
directions = directions.apply(pd.Series)

# Create an ingredient list for users to search
ingre_list = ingre_list.str.replace(r'[\[\]\'"]', '', regex = True).str.split(', ')
user_ingre_list = list(set(chain.from_iterable(ingre_list)))

# Replace plural units with singular form
recipes['ingredients'] = recipes['ingredients'].str.replace(r' \(.+?\)', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
es_list = ['pinches', 'pouches', 'dashes', 'peaches', 'tomatoes', 'bunches', 'mangoes']
exception = ['skinless', 'boneless', 'leaves', 'seedless', 'strawberries']
def remove_word_tail(s):
  for i in es_list:
    s = s.replace(i, i[:-2])
  lst = re.findall(r'(?<=[\d½¾¼⅔⅓⅞⅝⅛⅜] )[^\d½¾¼⅔⅓⅞⅝⅛⅜\s]+s\b', s)
  lst = [i for i in lst if i not in exception]
  for i in lst:
    s = s.replace(i, i[:-1])
  return s
recipes['ingredients'] = recipes['ingredients'].apply(remove_word_tail)
user_ingre_list = [i for i in user_ingre_list if any(i in j for j in recipes['ingredients'])]
recipes['ingredients'] = recipes['ingredients'].str.split(r', (?=[\d½¾¼⅔⅓⅞⅝⅛⅜])', regex = True)

# Convert the quantity of ingredients into fraction form
dict1 = {'½': '1/2', '¾': '3/4', '¼': '1/4', '⅔': '2/3', '⅓': '1/3', '⅞': '7/8', '⅝': '5/8', '⅛': '1/8', '⅜': '3/8'}
def change_quantity(s):
  for i in range(len(s)):
    if re.search(r'\d', s[i][0]):
      s[i] = s[i].split(maxsplit = 1)
      if s[i][1][0] in dict1:
        s[i][0] = int(s[i][0]) + Fraction(dict1[s[i][1][0]])
        s[i][1] = s[i][1].replace(f'{s[i][1][0]} ', '')
      else:
        s[i][0] = Fraction(s[i][0])
    elif re.search(r'[½¾¼⅔⅓⅞⅝⅛⅜]', s[i][0]):
      s[i] = s[i].split(maxsplit = 1)
      s[i][0] = Fraction(dict1[s[i][0]])
    else:
      s[i] = [Fraction(0), s[i]]
  return s
recipes['ingredients'] = recipes['ingredients'].apply(change_quantity)

# Convert the ingredient list into dict
recipes['ingredients'] = recipes['ingredients'].apply(lambda x: {i[1]: i[0] for i in x})

# Combine dataframes horizontally
cleaned_recipes_data = pd.concat([recipes, cuisine, nutritions], axis = 1)

# Replace null values in total time column
cleaned_recipes_data["total_time"] = cleaned_recipes_data["total_time"].fillna("Unkown")

# Drop unneeded and rename columns
cleaned_recipes_data = cleaned_recipes_data.drop(columns = [cleaned_recipes_data.columns[0], 'prep_time', 'cook_time', 'yield', 'url', 'cuisine_path', 'nutrition', 'timing'])
cleaned_recipes_data = cleaned_recipes_data.rename(columns = {'total_time' : 'Total time', 'servings' : 'Servings', 'directions' : 'Instructions', 'ingredients' : 'Ingredients', 'rating' : 'Rating', 'img_src' : 'Image link'})

# Rearrange columns
cleaned_recipes_data = cleaned_recipes_data[['Cuisine Category', 'Total Fat', 'Total Carbohydrate', 'Protein', 'Ingredients', 'Instructions', 'Total time', 'Servings', 'Rating', 'Image link']]

<<<<<<< HEAD
# Create dataframe for other categories
list_region = ['European', 'Latin American', 'Asian', 'African', 'Brands']
cuisine_dessert = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'] == 'Desserts']
cuisine_maindish = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'] == 'Main Dishes']
cuisine_sidedish = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'] == 'Side Dishes']
cuisine_drink = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'] == 'Drinks']
cuisine_appetizer_snack = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'] == 'Appetizers and Snacks']
cuisine_region = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].isin(list_region)]
=======
# Use boolean mask to create new dataframe of cuisine categorized by region
datatype = 'dict'
mask = cleaned_recipes_data['Cuisine Category'].apply(lambda x: isinstance(x, eval(datatype)))
cuisine_region = cleaned_recipes_data[mask]

# Create dataframe for other categories, na check for NaN values
cuisine_dessert = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].str.contains('Desserts', case = False, na = False)]
cuisine_maindish = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].str.contains('Main Dishes', case = False, na = False)]
cuisine_sidedish = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].str.contains('Side Dish', case = False, na = False)]
cuisine_drink = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].str.contains('Drinks Recipes', case = False, na = False)]
cuisine_appetizer_snack = cleaned_recipes_data.loc[cleaned_recipes_data['Cuisine Category'].str.contains('Appetizers and Snacks', case = False, na = False)]
>>>>>>> parent of 91cbd9f (change dict)

# Check for null of results
cleaned_recipes_data.isnull().sum()

# Final result
cleaned_recipes_data

# Export to csv file
cleaned_recipes_data.to_csv(r"d:\Hang\Cleaned Recipes Dataset.csv")

#Serialize and deserialize
with open('clean_data.pkl', 'wb') as f:
   dump(user_ingre_list, f)
   dump(cleaned_recipes_data, f)
   dump(cuisine_region, f)
   dump(cuisine_dessert, f)
   dump(cuisine_maindish, f)
   dump(cuisine_sidedish, f)
   dump(cuisine_drink, f)
   dump(cuisine_appetizer_snack, f)
