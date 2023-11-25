import streamlit as st
import deserialize as ds
import pandas as pd
from streamlit import session_state as ss
from Home_def import display_fraction
from fractions import Fraction

st.set_page_config(
    page_title="Group 3",
    layout='wide'
)

#Heading and description
st.markdown("<h1 style='text-align: center;'>Recipe and Meal Planner App</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center;'>The Recipe and Meal Planner App is the perfect companion for dedicated chefs and cooking enthusiasts. 
            With a user-friendly <br>interface and diverse features, this app helps you organize and enjoy your cooking experience efficiently and creatively.</p>""", unsafe_allow_html=True)

#Search bar
display_col = st.columns([10, 1, 1])
with display_col[0]:
    my_ingre = st.multiselect(
        label='Choose your ingredients',
        placeholder='',
        options=ds.user_search_list
    )
with display_col[1]:
    servings = st.number_input('Servings', value=None, step=1, min_value=1)
with display_col[2]:
    for i in range(2):
        st.write('')
    find = st.button(':mag_right:')

#Category checkbox
empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)
if 'mycookbook' not in ss:
    favourite = empty_cookbook
    mydata = {'Description': [None], 'Recipe list': [favourite]}
    ss.mycookbook = pd.DataFrame(mydata, index=['My Favourite'])
if 'num' not in ss:
        ss.num = [0]
if 'result' not in ss:
    ss.result = pd.DataFrame({'Dataset': [ds.final_recipes_data]}, index=['default'])
if 'add_button' not in ss:
    ss.add_button = [[1 for i in range(len(ss.result.iloc[j]['Dataset']))] for j in range(len(ss.result))]

category_list = ['Cuisine', 'Appetizers and Snacks', 'Main Dishes', 'Side Dishes', 'Desserts', 'Drinks']
dataset = [ds.cuisine_region_list, ds.appetizer_snack_list, ds.maindish_list, ds.sidedish_list, ds.dessert_list, ds.drink_list]
category_df = pd.DataFrame({'Dataset': dataset}, index=category_list)
category_df['Choice'] = False
st.write('Category')

checks = st.columns(6)
for i in range(6):
    with checks[i]:
        category_df['Choice'].iloc[i] = st.checkbox(category_list[i])

region_list = ['African', 'Asian', 'Brands', 'European', 'Latin American', 'Middle Eastern']
region_choice = [False for i in range(6)]
if category_df['Choice'].iloc[0]: #If cuisine is chosen
    for i in range(6):
        region_choice[i] = st.checkbox(region_list[i])

if find:
    if len(category_df[category_df['Choice'] == True]) != 0:
        ss.result = category_df[category_df['Choice'] == True].drop('Choice', axis=1)
        if any(i == True for i in region_choice) :
            ss.result = ss.result.drop(labels='Cuisine')
            for i in range(len(region_choice)):
                if region_choice[i] == True:
                    region_set = ds.cuisine_region_list[ds.cuisine_region_list['Cuisine Category'] == region_list[i]]
                    new_row = pd.Series({'Dataset': region_set}, name=region_list[i])
                    ss.result = pd.concat([ss.result, new_row.to_frame().T])
    else:
        ss.result = pd.DataFrame({'Dataset': [ds.final_recipes_data]}, index=['default'])

    if len(my_ingre) != 0:
        for i in ss.result.index:
            category_ingre = ss.result.loc[i, 'Dataset'].copy()
            mask = category_ingre['Ingredients'].apply(lambda x: all(any(ingre in key for key in x.keys()) for ingre in my_ingre))
            category_ingre = category_ingre[mask]
            ss.result.at[i, 'Dataset'] = category_ingre
    ss.num = [0 for i in range(len(ss.result))]
    ss.add_button = [[1 for i in range(len(ss.result.iloc[j]['Dataset']))] for j in range(len(ss.result))]

#Display left right search
for k in range(len(ss.result)):
    col1 = st.columns([24, 1, 1])
    with col1[0]:
        if ss.result.index[k] != 'default':
            if ss.result.index[k] not in region_list:
                st.write('/' + ss.result.index[k])
            else:
                st.write('/Cuisine/' + ss.result.index[k])
    if  ss.result.iloc[k]['Dataset'].empty:
        st.write('No results')
    else:
        category_set = ss.result.iloc[k]['Dataset']
        with col1[1]:
            if st.button('<', key=ss.result.index[k]) and ss.num[k] >= 5:
                ss.num[k] -= 5
        with col1[2]:
            if st.button('\>', key=ss.result.index[k]+' ') and ss.num[k] < len(category_set) - 5:
                ss.num[k] += 5

        #Display recipes
        col2 = st.columns(5)
        if 'clicked_num' not in ss:
            ss.clicked_num = -1
        
        var = 5
        if ss.num[k] >= len(category_set) - 5:
            var = len(category_set) - ss.num[k]
        for i in range(var):
            item = category_set.iloc[ss.num[k] + i]
            item_name = category_set.index[ss.num[k] + i]
            with col2[i]:
                st.image(category_set.iloc[ss.num[k] + i]['Image link'])
                addcol = st.columns([9, 2])
                with addcol[0]:
                    if st.button(category_set.index[ss.num[k] + i]):
                        ss.clicked_num = ss.num[k] + i
                with addcol[1]:
                    if st.button('\+', key='+' + category_set.index[ss.num[k] + i]):
                        ss.add_button[k][i] += 1
                if ss.add_button[k][i] % 2 == 0:
                    existed_cookbook = [i for i in ss.mycookbook.index if item_name not in ss.mycookbook.loc[i, 'Recipe list'].index]
                    cookbookchoice = existed_cookbook[::-1] + ['New']
                    cookbook = st.selectbox('Choose a cookbook', cookbookchoice, key=item_name+'select')
                    recipe_add = category_set.iloc[[ss.num[k]+i], :]
                    if cookbook == 'New':
                        title = st.text_input('Title *')
                        description = st.text_input('Description')
                        if st.button('Add', key=item_name+'addnew'):
                            if title == '':
                                st.error('You haven\'t entered title')
                            elif title in ss.mycookbook.index:
                                st.error('Title existed!')
                            else:
                                new_cookbook = {'Description': description, 'Recipe list': recipe_add}
                                ss.mycookbook.loc[title] = new_cookbook
                                newcol1 = st.columns([5, 2])
                                with newcol1[0]:
                                    st.success('Recipe added successfully')
                                with newcol1[1]:
                                    st.button('OK')
                                ss.add_button[k][i] += 1
                                
                    else:
                        if st.button('Add', key=item_name+'add'):
                            recipe_list = ss.mycookbook.loc[cookbook, 'Recipe list']
                            recipe_list = pd.concat([recipe_list, recipe_add], ignore_index=False)
                            ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list
                            newcol1 = st.columns([5, 2])
                            with newcol1[0]:
                                st.success('Recipe added successfully')
                            with newcol1[1]:
                                st.button('OK')
                            ss.add_button[k][i] += 1

            if ss.clicked_num != -1:
                item = category_set.iloc[ss.clicked_num]
                instruction = item['Instructions'].replace('\n', '<br>')
                ingredients = ''
                if servings != None:
                    item_servings = servings
                else:
                    item_servings = item['Servings']
                item_ingre = item['Ingredients']
                item_original_servings = item['Servings']
                for j in item_ingre:
                    if item_ingre[j] != 0:
                        ingredients += f'{display_fraction(item_ingre[j]/item_original_servings*item_servings)} {j}<br>'
                    else:
                        ingredients += f'{j}<br>'
                for i in my_ingre:
                    ingredients = ingredients.replace(i, f'<mark style="background-color: grey;">{i}</mark>')
                col3 = st.columns(2)
                with col3[0]:
                    item_rating = item['Rating']
                    st.write(f'**Rating:** {item_rating}⭐')
                    col4 = st.columns(2)
                    with col4[0]:
                        item_total_time = item['Total time']
                        st.write(f'**Total time:** {item_total_time}')
                    with col4[1]:
                        st.write(f'**Servings:** {item_servings}')
                    st.write(f'**Nutrition:**')
                    col5 = st.columns([1, 1, 1])
                    with col5[0]:
                        item_total_fat = item['Total Fat']
                        st.write(f'{item_total_fat}g Fat')
                    with col5[1]:
                        item_total_carbs = item['Total Carbohydrate']
                        st.write(f'{item_total_carbs}g Carbs')
                    with col5[2]:
                        item_pro = item['Protein']
                        st.write(f'{item_pro}g Protein')
                    st.write(f'**Ingredients:**')
                    st.write(f'<p>{ingredients}</p>', unsafe_allow_html=True)
                with col3[1]:
                    st.write('**Instruction:**')
                    st.write(f"<p style='text-align: justify;'>{instruction}</p>", unsafe_allow_html=True)
                ss.clicked_num = -1