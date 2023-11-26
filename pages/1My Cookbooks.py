import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds
from  Home_def import display_instruction, display_instruction2

st.set_page_config(layout='wide')
empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)

#Heading
headercol = st.columns([1, 7])
with headercol[0]:
    st.markdown(f'<img src="https://media.giphy.com/media/igVCthAMg37D7FMFrm/giphy.gif" width="130">', unsafe_allow_html=True)
with headercol[1]:
    st.write('')
    st.header('My Cookbooks')

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

#Search bar
display_col0 = st.columns(2)
with display_col0[0]:
    col10 = st.columns([10, 1])
    with col10[0]:
        cookbook = st.selectbox('Find cookbook', ss.mycookbook.index.tolist()[::-1], 
                                placeholder = 'Choose your cookbooks', label_visibility='collapsed')
    
    #Create a new cookbook
    with col10[1]:
        if st.button('\+'):
            ss.add += 1
        if ss.add % 2 == 0:
            with display_col0[1]:
                st.subheader('Create a new cookbook')
                title = st.text_input('Title *')
                description = st.text_input('Description')
                recipe = st.multiselect('Choose your recipes', ds.final_recipes_data.index)
                if st.button('Create'):
                    if title == '':
                        st.error('You haven\'t entered title')
                    else: 
                        new_cookbook_recipe = ds.final_recipes_data.loc[recipe, :].copy()
                        new_cookbook = {'Description': description, 'Recipe list': new_cookbook_recipe}
                        ss.mycookbook.loc[title] = new_cookbook
                        ss.add += 1
                        display_col1 = st.columns([6, 1])
                        with display_col1[0]:
                            st.success('New Cookbook created')
                        with display_col1[1]:
                            st.button('Close')

current = ss.mycookbook.loc[cookbook]
recipe_list = current['Recipe list']

with display_col0[0]:
    titlecol = st.columns([8, 1])
    titlechange = st.columns([8, 1])
    
    #Display cookbook
    with titlecol[0]:
        st.write('**Title:**')
    with titlecol[1]:
        if cookbook != 'My Favourite':
            if st.button('✏️'):
                ss.title_button += 1
    if ss.title_button % 2 != 0:
        st.write(cookbook)

    descol = st.columns([8, 1])
    deschange = st.columns([8, 1])
    with descol[0]:
        st.write('**Description:**')
    with descol[1]:
        if st.button('✏️', key='desbutton'):
            ss.des_button += 1
    if ss.des_button % 2 != 0:
        if current['Description'] != None:
            st.write(current['Description'])
    col7 = st.columns([3, 5, 1])
    col8 = st.columns([5, 1])
    col6 = st.columns([9, 1])

    #Add recipes
    with col7[1]:
        recipe_add = st.multiselect('Add recipes',[i for i in ds.final_recipes_data.index if i not in recipe_list.index], 
                                    placeholder='Add recipes', label_visibility='collapsed')
    with col7[2]:
        if st.button('OK', key='addbutton'):
            if len(recipe_add) != 0:
                add_list = ds.final_recipes_data.loc[recipe_add, :]
                recipe_list = pd.concat([recipe_list, add_list], ignore_index=False)
            with col6[0]:
                st.success('Recipes added successfully')
            with col6[1]:
                st.button('OK')

    #Display recipes
    with col7[0]:
        st.write('**Recipe list:**')
    remove_list = []
    servings_change = []
    for m in range(len(recipe_list)):
        display_col3 = st.columns([2, 3, 12, 4])
        item = recipe_list.iloc[m]
        with display_col3[0]:
            recipe_name = recipe_list.index[m]
            if st.checkbox(f'{recipe_name}', label_visibility='collapsed'):
                remove_list.append(recipe_list.index[m])
        with display_col3[1]:
            item_image = item['Image link']
            st.markdown(f'<img src="{item_image}" height="38.4">', unsafe_allow_html=True)
            st.write('')
        with display_col3[3]:
            input_servings = st.number_input(recipe_list.index[m]+'servings', value=int(item['Input Servings']), step=1, min_value=1, placeholder='Servings', label_visibility='collapsed')
            servings_change.append(input_servings)
        with display_col3[2]:
            if st.button(recipe_list.index[m]):
                with display_col0[1]:
                    display_instruction(item, input_servings)
                    display_instruction2(item)
    recipe_list['Input Servings'] = servings_change
    ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list

    #Remove recipes
    if len(remove_list) != 0: 
        if col8[1].button('Remove'):
            ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list.drop(remove_list)
            with col6[0]:
                st.success('Recipes removed successfully')
            with col6[1]:
                st.button('OK', key='removerecipes')

    #Modify title and description
    if ss.title_button % 2 == 0:
        with titlechange[0]:
            new_title = st.text_input('New title:', cookbook, label_visibility='collapsed')
        with titlechange[1]:
            if st.button('OK'):
                ss.mycookbook = ss.mycookbook.rename(index={cookbook: new_title})
                ss.mycookbook = pd.concat([ss.mycookbook.drop(new_title), ss.mycookbook.loc[[new_title], :]])
                with titlechange[0]:
                    st.success('Title changed successfully')
                with titlechange[1]:
                    st.button('OK', key='titlechange')
                ss.title_button += 1
     
    if ss.des_button % 2 == 0:
        with deschange[0]:
            new_description = st.text_input('New description:', current['Description'], key='desinput', label_visibility='collapsed')
        with deschange[1]:
            if st.button('OK', key='changedes'):
                ss.mycookbook.at[cookbook, 'Description'] = new_description
                ss.mycookbook = pd.concat([ss.mycookbook.drop(cookbook), ss.mycookbook.loc[[cookbook], :]])
                with deschange[0]:
                    st.success('Description changed successfully')
                with deschange[1]:
                    st.button('OK', key='deschange')
                ss.des_button += 1

    #Remove cookbook
    if cookbook != 'My Favourite':
        if st.button(':red[Remove cookbook]'):
            ss.mycookbook = ss.mycookbook.drop(cookbook, axis=0)
            col9 = st.columns([8, 1])
            with col9[0]:
                st.success('Cookbook removed successfully')
            with col9[1]:
                st.button('OK', key='removecookbook')