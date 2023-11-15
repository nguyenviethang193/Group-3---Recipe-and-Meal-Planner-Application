import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from datetime import datetime,  timedelta

st.header('Weekly Meal Plan')

row_name = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
column_name = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']

data = [([] for i in range(7)) for j in range(4)]

if 'plan' not in ss:
    ss['plan'] = pd.DataFrame(data, index=row_name, columns=column_name)

today = datetime.now() 
monday_of_current_week = today - timedelta(days=today.weekday()) # 0 represents Monday
st.write(f' Week {monday_of_current_week.strftime('%d/%m/%Y')}')


