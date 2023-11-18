import streamlit as st
from streamlit import session_state as ss
from Home_def import split_dict
import deserialize as ds

st.set_page_config(layout='wide')
st.header('Shopping List')

if 'shop_list' not in ss:
    ss.shop_list = {}
remove_list = []
shopcol = st.columns([3, 2, 2, 1, 1])
shopcol2 = st.columns([12, 1])
shopcol3 = st.columns(2)
with shopcol[0]:
    ingre = st.selectbox('', ds.user_search_list, placeholder='Input your ingredient', label_visibility='collapsed')
with shopcol[1]:
    ingre_num = st.number_input('', min_value=0.01, value=None, placeholder='Number', label_visibility='collapsed')
with shopcol[2]:
    ingre_unit = st.text_input('', placeholder='Unit', value=None, label_visibility='collapsed')

with shopcol[3]:
    if st.button('Add'):
        if ingre_unit != None:
            ingre = f'{ingre_unit} {ingre}'
        if ingre in ss.shop_list:
            ss.shop_list[ingre] += ingre_num
        else:
            ss.shop_list[ingre] = ingre_num
dict12 = split_dict(ss.shop_list)
for m in range(2):
    with shopcol3[m]:
        for i in dict12[m]:
            shopcol1 = st.columns([1, 1, 7])
            with shopcol1[0]:
                if st.checkbox('', key=i, label_visibility='collapsed'):
                    remove_list.append(i)
            with shopcol1[1]:
                new_num = st.number_input(i, min_value=0.01, value=float(ss.shop_list[i]), label_visibility='collapsed')
                ss.shop_list[i] = new_num
            with shopcol1[2]:
                st.write(i)
if len(remove_list) != 0:
    with shopcol[4]:
        if st.button('Remove'):
            for i in remove_list:
                del ss.shop_list[i]
            with shopcol2[0]:
                st.success('Items removed successfully')
            with shopcol2[1]:
                st.button('OK')
