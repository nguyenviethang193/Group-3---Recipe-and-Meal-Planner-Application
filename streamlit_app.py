import streamlit as st
import deserialize as ds
from streamlit_tags import st_tags

st.markdown("<h1 style='text-align: center;'>Recipe and Meal Planner App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Write your app description here</p>", unsafe_allow_html=True)

my_ingre = st_tags(
    label='Choose your ingredients',
    text='Press enter to add, \'>\' to use suggestions',
    suggestions=ds.user_search_list,
    maxtags=6
)
st.write(ds.dessert_list)