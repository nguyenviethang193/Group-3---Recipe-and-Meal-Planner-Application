import streamlit as st
import pandas as pd
from class1 import User
# Import other libraries as needed
st.title("Meal Planner App")
selected_meal = st.selectbox("Select a Meal", ["Breakfast", "Lunch", "Dinner"])
selected_date = st.date_input("Select Date")
