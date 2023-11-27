from fractions import Fraction
import base64
import streamlit as st

def display_fraction(a):
    if a != int(a):
        integer = a.numerator//a.denominator
        if integer == 0:
            integer = ''
        else:
            integer = str(integer) + ' '
        mod = a.numerator % a.denominator
        return f'{integer}{mod}/{a.denominator}'
    return a

def split_dict(input_dict):
    if len(input_dict) % 2 == 1:
        midpoint = len(input_dict) // 2 + 1
    else:
        midpoint  = len(input_dict) // 2
    
    dict1 = dict(list(input_dict.items())[:midpoint])
    dict2 = dict(list(input_dict.items())[midpoint:])
    
    return dict1, dict2

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def date_form(a):
    return a.strftime('%d/%m/%Y')

def display_instruction(item, input_servings, my_ingre = []):
    ingredients = ''
    item_ingre = item['Ingredients']
    item_servings = item['Servings']
    for j in item_ingre:
        if item_ingre[j] != 0:
            ingredients += f'{display_fraction(item_ingre[j]/item_servings*input_servings)} {j}<br>'
        else:
            ingredients += f'{j}<br>'
    for i in my_ingre:
        ingredients = ingredients.replace(i, f'<mark style="background-color: grey;">{i}</mark>')
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

def display_instruction2(item):
    instruction = item['Instructions'].replace('\n', '<br>')
    st.write('**Instruction:**')
    st.write(f"<p style='text-align: justify;'>{instruction}</p>", unsafe_allow_html=True)