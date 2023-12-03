import streamlit as st
from functions import get_img_as_base64

st.set_page_config(layout='wide')

with open('pages/polaroid.css', "r") as css_file:
  st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
  
hang_encoded_image = get_img_as_base64("Introduction/resources/images/hang.jpg")
danh_encoded_image = get_img_as_base64("Introduction/resources/images/danh.JPG")
dung_encoded_image = get_img_as_base64("Introduction/resources/images/dung.JPG")
hieu_encoded_image = get_img_as_base64("Introduction/resources/images/hieu.jpg")

col0 = st.columns([2, 1, 2])
with col0[1]:
  st.markdown(f'<img src="https://media.giphy.com/media/6IfdksCcmX1l5yCqBy/giphy.gif" width="200">', unsafe_allow_html=True)

# HTML content with image and font
html_content = f"""
  <div class="quote">
    Your meal, our deal!
  </div>

  <div class="wrapper">
    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpg;base64,{hang_encoded_image}" alt="">
        <div class="caption">Nguyen Viet Hang</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpg;base64,{danh_encoded_image}" alt="">
        <div class="caption">Tran Duy Anh</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpg;base64,{dung_encoded_image}" alt="">
        <div class="caption">Nguyen Manh Dung</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpg;base64,{hieu_encoded_image}" alt="">
        <div class="caption">Nguyen Minh Hieu</div>
      </div>
    </div>
  </div>

  <div class = "intro1">
  <div class = "intro">
      We are a small passionate group of developers set out to bring convenience to your everyday life, one application at a time.
  </div>

  <div class="intro2">
    <h2>ABOUT THIS PROJECT</h2> 

    <div class = "paragraph">
      <p>
        This app will help you plan out your everyday meals according to your diet. We have hundreds of recipe for you to choose from, ranging from savory to sweet, which allows you to find recipes based on the ingredients and the amount of servings. We provide detailed steps and ingredients needed as well as calculate the amount of nutrition for each recipe. <br>
        <br>
        You can create your very own cookbook within the app, allowing you to keep track of your favorite recipes, as well as plan weekly meals for individuals or your whole family and create your very own shopping list.
      </p>
    </div>
  </div>
    """

# Use st.markdown to render HTML
col1 = st.columns([1, 4, 1])
with col1[1]:
  st.markdown(html_content, unsafe_allow_html=True)