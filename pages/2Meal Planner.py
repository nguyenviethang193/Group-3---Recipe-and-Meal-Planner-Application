import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds
from datetime import datetime,  timedelta
from Home_def import display_instruction, display_instruction2, date_form

st.set_page_config(layout='wide')

row_name = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
column_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
data = [(pd.DataFrame(columns=ds.final_recipes_data.columns) for i in range(7)) for j in range(4)]
empty_dataset = pd.DataFrame(data, index=row_name, columns=column_name)

#Session state
if 'week_list'not in ss:
    today = datetime.now() 
    ss.monday = today - timedelta(days=today.weekday()) # 0 represents Monday
    ss.sunday = ss.monday + timedelta(days=6)
    ss.week_list = pd.Series([empty_dataset], index=[f'{date_form(ss.monday)} - {date_form(ss.sunday)}'])
if 'recipe_button' not in ss:
    ss.recipe_button = -1

col0 = st.columns([1, 7])
with col0[0]:
    st.markdown(f'<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMWg0NnZ1Z3U3OW43c3A0dm42ZHNmZnc4N2swcWFlZmNtZXNpbjB0biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/CkISXfgTSLTmZUOwJE/giphy.gif" width="130">', unsafe_allow_html=True)
with col0[1]:
    st.write('')
    st.header('Weekly Meal Plan')

col1 = st.columns([15, 1, 11])
col2 = st.columns([3, 2])

#Choose week
with col1[1]:
    st.write('')
    st.write('')
    if st.button('\+'):
        ss.monday += timedelta(days=7)
        ss.sunday += timedelta(days=7)
        new_week = pd.Series([empty_dataset], index=[f'{date_form(ss.monday)} - {date_form(ss.sunday)}'])
        ss.week_list = pd.concat([new_week, ss.week_list])
with col1[0]:
    week = st.selectbox('Choose a week', options=ss.week_list.index)

#Weekdays
with col2[0]:
    current_week = ss.week_list[week]
    for i in column_name:
        with st.expander(i):
            for j in row_name:
                recipe_list = current_week.loc[j, i]
                col3 = st.columns([4, 5, 1])
                col4 = st.columns(3)
                col5 = st.columns([6, 1])
                col6 = st.columns([9, 1])

                #Display nutrition for each meal
                with col3[0]:
                    st.write(j)
                    st.write('**Nutritions**')
                with col4[0]:
                    total_fat = recipe_list['Total Fat']
                    st.write(f'{sum(total_fat)}g Fat')
                with col4[1]:
                    total_carbs = recipe_list['Total Carbohydrate']
                    st.write(f'{sum(total_carbs)}g Carbs')
                with col4[2]:
                    total_pro = recipe_list['Protein']
                    st.write(f'{sum(total_pro)}g Protein')

                #Add recipes
                with col3[1]:
                    recipe_add = st.multiselect(week+i+j+'select', [i for i in ds.final_recipes_data.index if i not in recipe_list.index], placeholder='Add', label_visibility='collapsed')
                with col3[2]:
                    button = st.button('OK', key=week+i+j+'add')
                if button:
                    add_list = ds.final_recipes_data.loc[recipe_add, :]
                    with col6[0]:
                        st.success('Recipes added successfully')
                    with col6[1]:
                        st.button('OK')
                    recipe_list = pd.concat([recipe_list, add_list], ignore_index=False)

                remove_list = []
                servings_change = []

                #Display recipes
                for m in range(len(recipe_list)):
                    display_col3 = st.columns([2, 3, 12, 4])
                    item = recipe_list.iloc[m]
                    with display_col3[0]:
                        recipe_name = recipe_list.index[m]
                        if st.checkbox(f'{recipe_name}'+i+j+week+'checkbox', label_visibility='collapsed'):
                            remove_list.append(recipe_list.index[m])
                    with display_col3[1]:
                        item_image = item['Image link']
                        st.markdown(f'<img src="{item_image}" height="38.4">', unsafe_allow_html=True)
                        st.write('')
                    with display_col3[3]:
                        input_servings = st.number_input(recipe_list.index[m]+week+i+j+'servings', value=int(item['Input Servings']), step=1, min_value=1, placeholder='Servings', label_visibility='collapsed')
                        servings_change.append(input_servings)
                    with display_col3[2]:
                        if st.button(recipe_list.index[m], key=f'{recipe_name}'+i+j+week):
                            ss.recipe_button = recipe_list.index[m]
                recipe_list['Input Servings'] = servings_change
                ss.week_list[week].at[j, i] = recipe_list
                if ss.recipe_button != -1:
                    with col2[1]:
                        item = recipe_list.loc[ss.recipe_button]
                        item_input_servings = item['Input Servings']
                        display_instruction(item, item_input_servings)
                        display_instruction2(item)
                        ss.recipe_button =  -1

                #Remove recipes
                if len(remove_list) != 0: 
                    if col5[1].button('Remove', key=week+i+j):
                        ss.week_list[week].at[j, i] = recipe_list.drop(remove_list)
                        with col6[0]:
                            st.success('Recipes removed successfully')
                        with col6[1]:
                            st.button('OK')