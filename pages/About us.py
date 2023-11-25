import streamlit as st
import base64
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

  <h1>INTRODUCE</h1> 
  <h2>OUR TEAM</h2>

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
    """

    # Use st.markdown to render HTML
st.markdown(html_content, unsafe_allow_html=True)
