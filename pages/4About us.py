import streamlit as st
import base64

st.set_page_config(layout='wide')

with open('pages/polaroid.css', "r") as css_file:
  st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
  
with open("Introduction/resources/images/hang.jpg", "rb") as hang:
    hang_image_bytes = hang.read()
hang_encoded_image = base64.b64encode(hang_image_bytes).decode()

with open("Introduction/resources/images/danh.JPG", "rb") as danh:
    danh_image_bytes = danh.read()
danh_encoded_image = base64.b64encode(danh_image_bytes).decode()

with open("Introduction/resources/images/dung.JPG", "rb") as dung:
    dung_image_bytes = dung.read()
dung_encoded_image = base64.b64encode(dung_image_bytes).decode()

with open("Introduction/resources/images/hieu.jpg", "rb") as hieu:
    hieu_image_bytes = hieu.read()
hieu_encoded_image = base64.b64encode(hieu_image_bytes).decode()
 
    # HTML content with image and font
html_content = f"""

  <div class = "intro1">
    <h1>MEET OUR TEAM</h1> 

    <div class = "intro">
      We are a small passionate group of developers set out to bring convenience to your everyday life, one application at a time.
  </div>

  <div class="quote">
    "Your meal, our deal!"
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


  <div class="intro2">
    <h2>ABOUT THIS PROJECT</h2> 

    <div class = "paragraph">
      <p>
        This app will help you plan out your everyday meals according to your diet. Our database consists of hundreds of recipe for you to choose from, ranging from savory to sweet. <br>
        <br>
        This app allows you to find recipes based on the ingredients you have and the aamount of servings you need. For users who are struggling to learn new recipes, this app can provide detailed steps and ingredients needed for each recipe, as well as calculate the amount of fat, carbonhydrate and protein within those recipes. <br>
        <br>
        And in case you are on a diet, this app can easily keep track of the nutrition values in each recipe. Additionally, you will have the option to create your very own cook book within the app, allowing you to keep track of your favorite recipes, as well as giving you a grocery list for all the ingredients you would need for all your recipes.
      </p>
    </div>
  </div>
    """

    # Use st.markdown to render HTML
col = st.columns([1, 4, 1])
with col[1]:
  st.markdown(html_content, unsafe_allow_html=True)
