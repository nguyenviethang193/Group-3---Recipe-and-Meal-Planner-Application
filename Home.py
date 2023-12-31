import streamlit as st
import deserialize as ds
import pandas as pd
from streamlit import session_state as ss
from functions import display_instruction, display_instruction2

st.set_page_config(
    page_title="Group 3",
    layout='wide'
)

#Session state
empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)
if 'clicked_num' not in ss:
    ss.clicked_num = -1
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

#Heading
st.markdown("<h1 style='text-align: center;'>Recipe and Meal Planner App</h1>", unsafe_allow_html=True)

#Search bar
col0 = st.columns([10, 1, 1])
with col0[0]:
    my_ingre = st.multiselect(
        label='Choose your ingredients',
        placeholder='',
        options=ds.user_search_list
    )
with col0[1]:
    servings = st.number_input('Servings', value=None, step=1, min_value=1)
with col0[2]:
    for i in range(2):
        st.write('')
    find = st.button(':mag_right:')

#Category checkboxes
category_list = ['Cuisine', 'Appetizers and Snacks', 'Main Dishes', 'Side Dishes', 'Desserts', 'Drinks']
dataset = [ds.cuisine_region_list, ds.appetizer_snack_list, ds.maindish_list, ds.sidedish_list, ds.dessert_list, ds.drink_list]
category_df = pd.DataFrame({'Dataset': dataset}, index=category_list)
category_df['Choice'] = False
st.write('Category')

checks = st.columns(6)
for i in range(6):
    with checks[i]:
        category_df.at[category_df.index[i], 'Choice'] = st.checkbox(category_list[i])

region_list = ['African', 'Asian', 'European', 'Latin American', 'Middle Eastern', 'Brands']
region_dataset = [ds.african_list, ds.asian_list, ds.european_list, ds.latin_list, ds.middle_eastern_list, ds.brands_list]
region_df = pd.DataFrame({'Dataset': region_dataset}, index=region_list)
region_df['Choice'] = False
if category_df['Choice'].iloc[0]: #If cuisine is chosen
    for i in region_list:
        region_df.at[i, 'Choice'] = st.checkbox(i)

#Find recipes
if find:
    if len(category_df[category_df['Choice'] == True]) != 0:
        ss.result = category_df[category_df['Choice'] == True]
        region_choice = region_df[region_df['Choice'] == True]
        if len(region_choice) != 0:
            ss.result = pd.concat([ss.result.drop(labels='Cuisine'), region_choice])
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
        var = 5
        if ss.num[k] >= len(category_set) - 5:
            var = len(category_set) - ss.num[k]
        for i in range(var):
            item = category_set.iloc[ss.num[k] + i]
            item_name = category_set.index[ss.num[k] + i]
            with col2[i]:
                st.image(category_set.iloc[ss.num[k] + i]['Image link'])

                #Add recipe to a cookbook
                col3 = st.columns([9, 2])
                with col3[0]:
                    if st.button(category_set.index[ss.num[k] + i]):
                        ss.clicked_num = ss.num[k] + i
                with col3[1]:
                    if st.button('\+', key='+' + category_set.index[ss.num[k] + i]):
                        ss.add_button[k][i] += 1
                if ss.add_button[k][i] % 2 == 0:
                    existed_cookbook = [i for i in ss.mycookbook.index if item_name not in ss.mycookbook.loc[i, 'Recipe list'].index]
                    cookbook = st.selectbox('Choose a cookbook', existed_cookbook + ['New'], key=item_name+'select')
                    recipe_add = category_set.iloc[[ss.num[k]+i], :]
                    if servings != None:
                        recipe_add['Input Servings'] = servings
                    if cookbook == 'New':
                        title = st.text_input('Title *', key='title' + item_name)
                        description = st.text_input('Description', key='description' + item_name)
                        if st.button('Add', key=item_name+'addnew'):
                            if title == '':
                                st.error('You haven\'t entered title')
                            elif title in ss.mycookbook.index:
                                st.error('Title existed!')
                            else:
                                new_cookbook = pd.DataFrame([{'Description': description, 'Recipe list': recipe_add}], index=[title])
                                ss.mycookbook = pd.concat([new_cookbook, ss.mycookbook])
                                col4 = st.columns([5, 2])
                                with col4[0]:
                                    st.success('Recipe added successfully')
                                with col4[1]:
                                    st.button('OK')
                                ss.add_button[k][i] += 1           
                    else:
                        if st.button('Add', key=item_name+'add'):
                            recipe_list = ss.mycookbook.loc[cookbook, 'Recipe list']
                            recipe_list = pd.concat([recipe_list, recipe_add])
                            ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list
                            col4 = st.columns([5, 2])
                            with col4[0]:
                                st.success('Recipe added successfully')
                            with col4[1]:
                                st.button('OK')
                            ss.add_button[k][i] += 1

            #Display recipe instruction
            if ss.clicked_num != -1:
                item = category_set.iloc[ss.clicked_num]
                if servings != None:
                    item_servings = servings
                else:
                    item_servings = item['Servings']
                col5 = st.columns(2)
                with col5[0]:
                    display_instruction(item, item_servings, my_ingre)
                with col5[1]:
                    display_instruction2(item)
                ss.clicked_num = -1
