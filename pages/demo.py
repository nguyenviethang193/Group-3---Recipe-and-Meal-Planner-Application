import streamlit as st
import deserialize as ds
import pandas as pd
import st_clickable_images as img
from streamlit import session_state as ss

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
category_list = ['Cuisine', 'Appetizers and Snacks', 'Main Dishes', 'Side Dishes', 'Desserts', 'Drinks']
dataset = [ds.cuisine_region_list, ds.appetizer_snack_list, ds.maindish_list, ds.sidedish_list, ds.dessert_list, ds.drink_list]
category_df = pd.DataFrame({'Dataset': dataset}, index=category_list)
category_df['Choice'] = False
st.write('Category')
checks = st.columns(6)

for i in range(6):
    with checks[i]:
        category_df['Choice'].iloc[i] = st.checkbox(category_list[i])


region_list = ['African', 'Asian', 'Brands', 'European', 'Latin America', 'Middle Eastern']
region_choice = [False for i in range(6)]
if category_df['Choice'].iloc[0]: #If cuisine is chosen
    for i in range(6):
        region_choice[i] = st.checkbox(region_list[i])

result = ds.final_recipes_data
if 'num' not in ss:
    ss.num = 0

col1 = st.columns([24, 1, 1])
with col1[1]:
    if st.button('<') and ss.num >= 5:
        ss.num -= 5
with col1[2]:
    if st.button('\>') and ss.num < len(result.index) - 5:
        ss.num += 5

col2 = st.columns(5)
if 'clicked_num' not in ss:
    ss.clicked_num = -1

for i in range(5):
    with col2[i]:
        st.image(result.iloc[ss.num + i, -1])
        if st.button(result.index[ss.num + i]):
            ss.clicked_num = ss.num + i

if ss.clicked_num != -1:
    item = result.iloc[ss.clicked_num]
    instruction = item['Instructions'].replace('\n', '<br>')
    ingredients = ''
    for j in item['Ingredients']:
        ingredients += f'{item['Ingredients'][j]} {j}<br>'
    col3 = st.columns(2)
    with col3[0]:
        st.write(f'**Rating:** {item['Rating']}⭐')
        col4 = st.columns(2)
        with col4[0]:
            st.write(f'**Total time:** {item['Total time']}')
        with col4[1]:
            st.write(f'**Servings:** {item['Servings']}')
        st.write(f'**Nutrition:**')
        col5 = st.columns([1, 1, 1])
        with col5[0]:
            st.write(f'{item['Total Fat']}g Fat')
        with col5[1]:
             st.write(f'{item['Total Carbohydrate']}g Carbs')
        with col5[2]:
            st.write(f'{item['Protein']}g Protein')
        st.write(f'**Ingredients:**')
        st.write(f'<p>{ingredients}</p>', unsafe_allow_html=True)
    with col3[1]:
        st.write('**Instruction:**')
        st.write(f"<p style='text-align: justify;'>{instruction}</p>", unsafe_allow_html=True)