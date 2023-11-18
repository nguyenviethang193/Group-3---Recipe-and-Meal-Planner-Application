import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import deserialize as ds
from  Home_def import display_fraction

st.set_page_config(layout='wide')
st.header('My Cookbooks')

empty_cookbook = pd.DataFrame(columns=ds.final_recipes_data.columns)
if 'mycookbook' not in ss:
    favourite = empty_cookbook
    mydata = {'Description': [None], 'Recipe list': [favourite]}
    ss.mycookbook = pd.DataFrame(mydata, index=['My Favourite'])
if 'add' not in ss:
    ss.add = 1

display_col0 = st.columns(2)
with display_col0[0]:
    col10 = st.columns([10, 1])
    with col10[0]:
        cookbook = st.selectbox('', ss.mycookbook.index.tolist()[::-1], 
                                placeholder = 'Choose your cookbooks', label_visibility='collapsed')

    with col10[1]:
        if st.button('\+'):
            ss.add += 1
        if ss.add % 2 == 0:
            with display_col0[1]:
                st.subheader('Create a new cookbook')
                title = st.text_input('Title *')
                description = st.text_input('Description')
                recipe = st.multiselect('Choose your recipes (Optional)', ds.final_recipes_data.index)
                if st.button('Create'):
                    if title == '':
                        st.error('You haven\'t input title')
                    else: 
                        new_cookbook_recipe = ds.final_recipes_data.loc[recipe, :].copy()
                        new_cookbook_recipe['Input servings'] = new_cookbook_recipe['Servings'].copy()
                        new_cookbook = {'Description': description, 'Recipe list': new_cookbook_recipe}
                        ss.mycookbook.loc[title] = new_cookbook
                        ss.add += 1
                        display_col1 = st.columns([6, 1])
                        with display_col1[0]:
                            st.success('New Cookbook created')
                        with display_col1[1]:
                            st.button('Close')


current = ss.mycookbook.loc[cookbook]
st.write('**Description:**')
if current['Description'] != None:
    st.write(current['Description'])

recipe_list = current['Recipe list']
display_col2 = st.columns(2)
col3 = st.columns(2)

with display_col2[0]:
    col7 = st.columns([4, 5, 1])
    col8 = st.columns([5, 1])
    col6 = st.columns([9, 1])

    with col7[1]:
            recipe_add = st.multiselect('',[i for i in ds.final_recipes_data.index if i not in recipe_list.index], 
                                        placeholder='Add recipes', label_visibility='collapsed')
    with col7[2]:
        if st.button('OK', key='addbutton'):
            add_list = ds.final_recipes_data.loc[recipe_add, :]
            add_list['Input servings'] = add_list['Servings'].copy()
            recipe_list = pd.concat([recipe_list, add_list], ignore_index=False)
            with col6[0]:
                st.success('Recipes added successfully')
            with col6[1]:
                st.button('OK')

    with col7[0]:
        st.write('**Recipe list:**')
    remove_list = []
    servings_change = []
    for m in range(len(recipe_list)):
        display_col3 = st.columns([2, 3, 12, 4])
        item = recipe_list.iloc[m]
        with display_col3[0]:
            if st.checkbox(f'{recipe_list.index[m]}', label_visibility='collapsed'):
                remove_list.append(recipe_list.index[m])
        with display_col3[1]:
            st.markdown(f'<img src="{item['Image link']}" height="38.4">', unsafe_allow_html=True)
            st.write('')
        with display_col3[3]:
            input_servings = st.number_input('', value=int(item['Input servings']), step=1, min_value=1, placeholder='Servings', label_visibility='collapsed', key=recipe_list.index[m]+'servings')
            servings_change.append(input_servings)
        with display_col3[2]:
            if st.button(recipe_list.index[m]):
                instruction = item['Instructions'].replace('\n', '<br>')
                ingredients = ''
                for j in item['Ingredients']:
                    ingredients += f'{display_fraction(item['Ingredients'][j]/item['Servings']*input_servings)} {j}<br>'
                with display_col2[1]:
                    st.write(f'**Rating:** {item['Rating']}⭐')
                    col4 = st.columns(2)
                    with col4[0]:
                        st.write(f'**Total time:** {item['Total time']}')
                    with col4[1]:
                        st.write(f'**Servings:** {input_servings}')
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
                    st.write('**Instruction:**')
                    st.write(f"<p style='text-align: justify;'>{instruction}</p>", unsafe_allow_html=True)
    recipe_list['Input servings'] = servings_change
    ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list
    if len(remove_list) != 0: 
        if col8[1].button('Remove'):
            ss.mycookbook.at[cookbook, 'Recipe list'] = recipe_list.drop(remove_list)
            with col6[0]:
                st.success('Recipes removed successfully')
            with col6[1]:
                st.button('OK')

with display_col0[0]:
    if cookbook != 'My Favourite':
        if st.button(':red[Remove cookbook]'):
            ss.mycookbook = ss.mycookbook.drop(cookbook, axis=0)
            col9 = st.columns([9, 1])
            with col9[0]:
                st.success('Cookbook removed successfully')
            with col9[1]:
                st.button('OK')
