import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from datetime import datetime,  timedelta

row_name = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
column_name = ['Monday', 'Tueday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

data = [([] for i in range(7)) for j in range(4)]

def date_form(a):
    return a.strftime('%d/%m/%Y')

if 'plan' not in ss:
    ss['plan'] = pd.DataFrame(data, index=row_name, columns=column_name)
if 'week_list'not in ss:
    today = datetime.now() 
    ss['monday'] = today - timedelta(days=today.weekday()) # 0 represents Monday
    ss['sunday'] = ss.monday + timedelta(days=6)
    ss['week_list'] = [f'{date_form(ss.monday)} - {date_form(ss.sunday)}']
col_display = st.columns([3, 2])

with col_display[0]:
    st.header('Weekly Meal Plan')
    col_display2 = st.columns([5, 1])

    #Choose week
    with col_display2[0]:
        week = st.selectbox('Choose a week', options=ss.week_list)
    with col_display2[1]:
        st.write('')
        st.write('')
        if st.button('Add'):
            ss.monday += timedelta(days=7)
            ss.sunday += timedelta(days=7)
            ss.week_list.append(f'{date_form(ss.monday)} - {date_form(ss.sunday)}')

    #Weekdays
    for i in range(7):
        with st.expander(column_name[i]):
            st.write('Hi')
with col_display[1]:
    st.header('Shopping list')