import streamlit as st
from streamlit import session_state as ss
from Home_def import split_dict
import deserialize as ds

st.set_page_config(layout='wide')

#Session state
if 'shop_list' not in ss:
    ss.shop_list = {}
if 'ingre_list' not in ss:
    ss.ingre_list = ds.user_search_list
if 'unit_set' not in ss:
    ss.unit_set = ["jar", "container", "ounce", "oz", "pound", "kg", "qt", "gal","mg", "g", "pt", "l", "ml", "inch", "cm", "package", "bag", "sm", "medium", 
         "box", "can", "carton", "stick", "slice", "pad", "roll", "head", "cube", "bar", "block", "clove", "sq", "bottle", "tub", "envelope", "leaf", "loaf", "bunch"]
remove_list = []

#Heading
col0 = st.columns([1, 7])
with col0[0]:
    st.markdown(f'<img src="https://media.giphy.com/media/3BZdOcfkLo3PPqrW6z/giphy.gif" width="130">', unsafe_allow_html=True)
with col0[1]:
    st.write('')
    st.header('Shopping List')

col1 = st.columns([3, 2, 2, 1, 1])
col2 = st.columns([12, 1])
col5 = st.columns([5, 1])

#Add items
with col1[0]:
    ingre = st.selectbox('Enter an ingredient', ['other'] + ss.ingre_list)
    if ingre == 'other':
        ingre = st.text_input('Enter new ingredient', value='')
with col1[1]:
    ingre_num = st.number_input('Enter amount', min_value=0.01, value=None)
with col1[2]:
    ingre_unit = st.selectbox('Enter unit', ['None', 'other'] + ss.unit_set)
    if ingre_unit == 'other':
        ingre_unit = st.text_input('Enter new unit')
with col1[3]:
    st.write('')
    st.write('')
    addbutton = st.button('Add')
if addbutton == True:
    if ingre == '':
        with col5[0]:
            st.error('You haven\'t entered any ingredient')
    elif ingre_num == None:
        with col5[0]:
            st.error('You haven\'t entered amount')
    else:
        if ingre not in ss.ingre_list:
            ss.ingre_list.append(ingre)
        if ingre_unit != 'None':
            ingre = f'{ingre_unit} {ingre}'
            if ingre_unit not in ss.unit_set:
                ss.unit_set.append(ingre_unit)
        if ingre in ss.shop_list:
            ss.shop_list[ingre] += ingre_num
        else:
            ss.shop_list[ingre] = ingre_num

#Display items
dict12 = split_dict(ss.shop_list)
col3 = st.columns(2)
for m in range(2):
    with col3[m]:
        for i in dict12[m]:
            col4 = st.columns([1, 1, 7])
            with col4[0]:
                if st.checkbox('Check to remove', key=i, label_visibility='collapsed'):
                    remove_list.append(i)
            with col4[1]:
                new_num = st.number_input(i, min_value=0.01, value=float(ss.shop_list[i]), label_visibility='collapsed')
                ss.shop_list[i] = new_num
            with col4[2]:
                st.write(i)

#Remove items
if len(remove_list) != 0:
    with col1[4]:
        st.write('')
        st.write('')
        if st.button('Remove'):
            for i in remove_list:
                del ss.shop_list[i]
            with col2[0]:
                st.success('Items removed successfully')
            with col2[1]:
                st.button('OK')