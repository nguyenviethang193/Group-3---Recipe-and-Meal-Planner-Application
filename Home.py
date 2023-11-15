import streamlit as st
import deserialize as ds
import pandas as pd
import st_clickable_images as img

st.set_page_config(
    page_title="Group 3",
    layout='wide'
)

#Heading and description
st.markdown("<h1 style='text-align: center;'>Recipe and Meal Planner App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Write your app description here</p>", unsafe_allow_html=True)

#Search bar
col1, col2 = st.columns([6, 1])
with col1:
    my_ingre = st.multiselect(
        label='',
        placeholder='Choose your ingredients',
        options=ds.user_search_list,
        label_visibility='collapsed'
    )
with col2:
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
clicked = img.clickable_images(list(result.iloc[:, -1]),
                                titles=list(result.index),
                                div_style={"overflow-y":"scroll", "height": "460px"},
                                img_style={"margin": "7px", "width": "220px"})

st.markdown(f'Directions:\n {result.iloc[clicked]['Instructions']}')

