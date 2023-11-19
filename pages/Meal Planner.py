import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds
from datetime import datetime,  timedelta
from Home_def import display_fraction

st.set_page_config(layout='wide')
st.header('Weekly Meal Plan')
row_name = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
column_name = ['Monday', 'Tueday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

data = [(pd.DataFrame(columns=ds.final_recipes_data.columns) for i in range(7)) for j in range(4)]
empty_dataset = pd.DataFrame(data, index=row_name, columns=column_name)

def date_form(a):
    return a.strftime('%d/%m/%Y')

#Session state
if 'week_list'not in ss:
    today = datetime.now() 
    ss.monday = today - timedelta(days=today.weekday()) # 0 represents Monday
    ss.sunday = ss.monday + timedelta(days=6)
    ss.week_list = pd.Series([empty_dataset], index=[f'{date_form(ss.monday)} - {date_form(ss.sunday)}'])

col_display2 = st.columns([15, 1, 11])
col_display = st.columns([3, 2])

#Choose week
with col_display2[1]:
    st.write('')
    st.write('')
    if st.button('\+'):
        ss.monday += timedelta(days=7)
        ss.sunday += timedelta(days=7)
        new_week = pd.Series([empty_dataset], index=[f'{date_form(ss.monday)} - {date_form(ss.sunday)}'])
        ss.week_list = pd.concat([new_week, ss.week_list])
with col_display2[0]:
    week = st.selectbox('Choose a week', options=ss.week_list.index)
#Weekdays
with col_display[0]:
    current_week = ss.week_list[week]
    for i in column_name:
        with st.expander(i):
            for j in row_name:
                recipe_list = current_week.loc[j, i]
                mealcol0 = st.columns([4, 5, 1])
                mealcol2 = st.columns(3)
                mealcol1 = st.columns([6, 1])
                col6 = st.columns([9, 1])
                with mealcol0[0]:
                    st.write(j)
                    st.write('**Nutritions**')
                with mealcol2[0]:
                    total_fat = recipe_list['Total Fat']
                    st.write(f'{sum(total_fat)}g Fat')
                with mealcol2[1]:
                    total_carbs = recipe_list['Total Carbohydrate']
                    st.write(f'{sum(total_carbs)}g Carbs')
                with mealcol2[2]:
                    total_pro = recipe_list['Protein']
                    st.write(f'{sum(total_pro)}g Protein')
                with mealcol0[1]:
                    recipe_add = st.multiselect('', [i for i in ds.final_recipes_data.index if i not in recipe_list.index], 
                                 key=week+i+j+'select', placeholder='Add', label_visibility='collapsed')
                with mealcol0[2]:
                    button = st.button('OK', key=week+i+j+'add')
                if button:
                    add_list = ds.final_recipes_data.loc[recipe_add, :]
                    add_list['Input servings'] = add_list['Servings'].copy()
                    with col6[0]:
                        st.success('Recipes added successfully')
                    with col6[1]:
                        st.button('OK')
                    recipe_list = pd.concat([recipe_list, add_list], ignore_index=False)

                remove_list = []
                servings_change = []
                for m in range(len(recipe_list)):
                    display_col3 = st.columns([2, 3, 12, 4])
                    item = recipe_list.iloc[m]
                    with display_col3[0]:
                        recipe_name = recipe_list.index[m]
                        if st.checkbox('', key=f'{recipe_name}'+i+j+week+'checkbox', label_visibility='collapsed'):
                            remove_list.append(recipe_list.index[m])
                    with display_col3[1]:
                        item_image = item['Image link']
                        st.markdown(f'<img src="{item_image}" height="38.4">', unsafe_allow_html=True)
                        st.write('')
                    with display_col3[3]:
                        input_servings = st.number_input('', value=int(item['Input servings']), step=1, min_value=1, placeholder='Servings', label_visibility='collapsed', key=recipe_list.index[m]+week+i+j+'servings')
                        servings_change.append(input_servings)
                    with display_col3[2]:
                        if st.button(recipe_list.index[m], key=f'{recipe_list.index[m]}'+i+j+week):
                            instruction = item['Instructions'].replace('\n', '<br>')
                            ingredients = ''
                            item_ingre = item['Ingredients']
                            item_servings = item['Servings']
                            for j in item_ingre:
                                ingredients += f'{display_fraction(item_ingre[j]/item_servings*input_servings)} {j}<br>'
                            with col_display[1]:
                                item_rating = item['Rating']
                                st.write(f'**Rating:** {item_rating}⭐')
                                col4 = st.columns(2)
                                with col4[0]:
                                    item_total_time = item['Total time']
                                    st.write(f'**Total time:** {item_total_time}')
                                with col4[1]:
                                    st.write(f'**Servings:** {input_servings}')
                                st.write(f'**Nutrition:**')
                                col5 = st.columns([1, 1, 1])
                                with col5[0]:
                                    item_fat = item['Total Fat']
                                    st.write(f'{item_fat}g Fat')
                                with col5[1]:
                                    item_carbs = item['Total Carbohydrate']
                                    st.write(f'{item_carbs}g Carbs')
                                with col5[2]:
                                    item_pro = item['Protein']
                                    st.write(f'{item_pro}g Protein')
                                st.write(f'**Ingredients:**')
                                st.write(f'<p>{ingredients}</p>', unsafe_allow_html=True)
                                st.write('**Instruction:**')
                                st.write(f"<p style='text-align: justify;'>{instruction}</p>", unsafe_allow_html=True)
                recipe_list['Input servings'] = servings_change
                ss.week_list[week].at[j, i] = recipe_list
                if len(remove_list) != 0: 
                    if mealcol1[1].button('Remove', key=week+i+j):
                        ss.week_list[week].at[j, i] = recipe_list.drop(remove_list)
                        with col6[0]:
                            st.success('Recipes removed successfully')
                        with col6[1]:
                            st.button('OK')