import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds
from  Home_def import display_instruction, display_instruction2

st.set_page_config(layout='wide')
empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)

#Session state
if 'add' not in ss:
    ss.add = 1
if 'title_button' not in ss:
    ss.title_button = 1
if 'des_button' not in ss:
    ss.des_button = 1
if 'mycookbook' not in ss:
    favourite = empty_cookbook
    mydata = {'Description': [None], 'Recipe list': [favourite]}
    ss.mycookbook = pd.DataFrame(mydata, index=['My Favourite'])

#Heading
col0 = st.columns([1, 7])
with col0[0]:
    st.markdown(f'<img src="https://media.giphy.com/media/igVCthAMg37D7FMFrm/giphy.gif" width="130">', unsafe_allow_html=True)
with col0[1]:
    st.write('')
    st.header('My Cookbooks')

#Search bar
col1 = st.columns(2)
with col1[0]:
    col2 = st.columns([10, 1])
    with col2[0]:
        cookbook = st.selectbox('Find cookbook', ss.mycookbook.index, 
                                placeholder = 'Choose your cookbooks', label_visibility='collapsed')
    
    #Create a new cookbook
    with col2[1]:
        if st.button('\+'):
            ss.add += 1
        if ss.add % 2 == 0:
            with col1[1]:
                st.subheader('Create a new cookbook')
                title = st.text_input('Title *')
                description = st.text_input('Description')
                recipe = st.multiselect('Choose your recipes', ds.final_recipes_data.index)
                if st.button('Create'):
                    if title == '':
                        st.error('You haven\'t entered title')
                    elif title in ss.mycookbook.index:
                        st.error('Title existed!')
                    else: 
                        new_cookbook_recipe = ds.final_recipes_data.loc[recipe, :].copy()
                        new_cookbook = pd.DataFrame([{'Description': description, 'Recipe list': new_cookbook_recipe}], index=[title])
                        ss.mycookbook = pd.concat([new_cookbook, ss.mycookbook])
                        ss.add += 1
                        col3 = st.columns([6, 1])
                        with col3[0]:
                            st.success('New Cookbook created')
                        with col3[1]:
                            st.button('Close')

current = ss.mycookbook.loc[cookbook]
recipe_list = current['Recipe list']

with col1[0]:
    col4 = st.columns([8, 1])
    col5 = st.columns([8, 1])
    
    #Display cookbook
    with col4[0]:
        st.write('**Title:**')
    with col4[1]:
        if cookbook != 'My Favourite':
            if st.button('✏️'):
                ss.title_button += 1
    if ss.title_button % 2 != 0:
        st.write(cookbook)

    col6 = st.columns([8, 1])
    col7 = st.columns([8, 1])
    with col6[0]:
        st.write('**Description:**')
    with col6[1]:
        if st.button('✏️', key='desbutton'):
            ss.des_button += 1
    if ss.des_button % 2 != 0:
        if current['Description'] != None:
            st.write(current['Description'])
    col8 = st.columns([3, 5, 1])
    col9 = st.columns([5, 1])
    col10 = st.columns([9, 1])

    #Add recipes
    with col8[1]:
        recipe_add = st.multiselect('Add recipes',[i for i in ds.final_recipes_data.index if i not in recipe_list.index], 
                                    placeholder='Add recipes', label_visibility='collapsed')
    with col8[2]:
        if st.button('OK', key='addbutton'):
            if len(recipe_add) != 0:
                add_list = ds.final_recipes_data.loc[recipe_add, :]
                recipe_list = pd.concat([recipe_list, add_list])
            with col10[0]:
                st.success('Recipes added successfully')
            with col10[1]:
                st.button('OK')

    #Display recipes
    with col8[0]:
        st.write('**Recipe list:**')
    remove_list = []
    for m in range(len(recipe_list)):
        col11 = st.columns([2, 3, 12, 4])
        item = recipe_list.iloc[m]
        with col11[0]:
            recipe_name = recipe_list.index[m]
            if st.checkbox(f'{recipe_name}', label_visibility='collapsed'):
                remove_list.append(recipe_list.index[m])
        with col11[1]:
            item_image = item['Image link']
            st.markdown(f'<img src="{item_image}" height="38.4">', unsafe_allow_html=True)
            st.write('')
        with col11[3]:
            input_servings = st.number_input(recipe_list.index[m]+'servings', value=int(item['Input Servings']), 
                                             step=1, min_value=1, placeholder='Servings', label_visibility='collapsed')
            recipe_list.at[recipe_list.index[m], 'Input Servings'] = input_servings
        with col11[2]:
            if st.button(recipe_list.index[m]):
                with col1[1]:
                    display_instruction(item, input_servings)
                    display_instruction2(item)
    ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list

    #Remove recipes
    if len(remove_list) != 0: 
        if col9[1].button('Remove'):
            ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list.drop(remove_list)
            with col10[0]:
                st.success('Recipes removed successfully')
            with col10[1]:
                st.button('OK', key='removerecipes')

    #Modify title and description
    if ss.title_button % 2 == 0:
        with col5[0]:
            new_title = st.text_input('New title:', cookbook, label_visibility='collapsed')
        with col5[1]:
            if st.button('OK'):
                if new_title != cookbook and new_title in ss.mycookbook.index:
                    with col5[0]:
                        st.error('Title existed!')
                else:
                    ss.mycookbook = ss.mycookbook.rename(index={cookbook: new_title})
                    ss.mycookbook = pd.concat([ss.mycookbook.loc[[new_title], :], ss.mycookbook.drop(new_title)])
                    with col5[0]:
                        st.success('Title changed successfully')
                    with col5[1]:
                        st.button('OK', key='titlechange')
                    ss.title_button += 1
     
    if ss.des_button % 2 == 0:
        with col7[0]:
            new_description = st.text_input('New description:', current['Description'], key='desinput', label_visibility='collapsed')
        with col7[1]:
            if st.button('OK', key='changedes'):
                ss.mycookbook.at[cookbook, 'Description'] = new_description
                ss.mycookbook = pd.concat([ss.mycookbook.loc[[cookbook], :], ss.mycookbook.drop(cookbook)])
                with col7[0]:
                    st.success('Description changed successfully')
                with col7[1]:
                    st.button('OK', key='deschange')
                ss.des_button += 1

    #Remove cookbook
    if cookbook != 'My Favourite':
        if st.button(':red[Remove cookbook]'):
            ss.mycookbook = ss.mycookbook.drop(cookbook, axis=0)
            col12 = st.columns([8, 1])
            with col12[0]:
                st.success('Cookbook removed successfully')
            with col12[1]:
                st.button('OK', key='removecookbook')