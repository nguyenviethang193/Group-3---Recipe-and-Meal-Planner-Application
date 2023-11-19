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
st.markdown("<p style='text-align: center;'>Write your app description here</p>", unsafe_allow_html=True)

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
if 'num' not in ss:
        ss.num = [0]
if 'result' not in ss:
    ss.result = pd.DataFrame({'Dataset': [ds.final_recipes_data]}, index=['default'])

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
            with col2[i]:
                st.image(category_set.iloc[ss.num[k] + i, -1])
                if st.button(category_set.index[ss.num[k] + i]):
                    ss.clicked_num = ss.num[k] + i

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
                ingredients += f'{display_fraction(item_ingre[j]/item_original_servings*item_servings)} {j}<br>'
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