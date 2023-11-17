import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds

st.header('My Cookbooks')

empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)
if 'mycookbook' not in ss:
    favourite = empty_cookbook
    mydata = {'Title': ['My Favourite'],
            'Description': [None], 'Recipe list': [favourite]}
    ss.mycookbook = pd.DataFrame(mydata)
if 'add' not in ss:
    ss.add = 1

display_col0 = st.columns([4, 1, 5])
with display_col0[0]:
    cookbook = st.selectbox('', ss.mycookbook['Title'], 
                            placeholder = 'Choose your cookbooks', label_visibility='collapsed')
    with display_col0[1]:
        if st.button('Add'):
            ss.add += 1
        if ss.add % 2 == 0:
            with display_col0[2]:
                st.write('Create a new cookbook')
                title = st.text_input('Title *')
                description = st.text_input('Description')
                recipe = st.multiselect('Choose your recipes (Optional)', ds.final_recipes_data.index)
                if st.button('Create'):
                    if title == '':
                        st.error('You haven\'t input title')
                    else: 
                        new_cookbook_recipe = ds.final_recipes_data.loc[recipe, :]
                        new_cookbook = {'Title': title, 'Description': description, 'Recipe list': new_cookbook_recipe}
                        ss.mycookbook.loc[len(ss.mycookbook)] = new_cookbook
                        ss.add += 1
                        display_col1 = st.columns([5, 1])
                        with display_col1[0]:
                            st.success('New Cookbook created')
                        with display_col1[1]:
                            st.button('Close')
