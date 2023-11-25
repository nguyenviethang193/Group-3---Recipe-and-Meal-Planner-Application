import streamlit as st
import base64

def main():
    with open("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/resources/images/hang.jpg", "rb") as hang:
        hang_image_bytes = hang.read()
    hang_encoded_image = base64.b64encode(hang_image_bytes).decode()

    with open("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/resources/images/danh.JPG", "rb") as danh:
        danh_image_bytes = danh.read()
    danh_encoded_image = base64.b64encode(danh_image_bytes).decode()

    with open("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/resources/images/dung.JPG", "rb") as dung:
        dung_image_bytes = dung.read()
    dung_encoded_image = base64.b64encode(dung_image_bytes).decode()

    with open("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/resources/images/hieu.jpg", "rb") as hieu:
        hieu_image_bytes = hieu.read()
    hieu_encoded_image = base64.b64encode(hieu_image_bytes).decode()
 
    # HTML content with image and font
    html_content = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Polaroid Gallery</title>
  <style type="text/css">
    *{
      box-sizing: border-box;
    }

    @font-face{
      font-family: 'Brittany';
      src: url("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/font/BrittanySignature.ttf");
    }

    @font-face{
      font-family: 'Bebas Neue';
      src: url("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/font/BebasNeue-Regular.ttf");
    }

    @font-face {
      font-family: 'Satisfy';
      src: url("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/font/Satisfy-Regular.ttf");
    }

    body{
      background-image: url("https://raw.githubusercontent.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/resources/images/background.jpg");
    }

    .wrapper {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: row;
      height: 50vh;
    }

    .quote{
      text-align: center;
      margin-top: 2rem; 
      font-family: 'Satisfy', serif;
      font-size: 8rem;
      color: #333; 
      font-weight: 100;
    }

    h1 {
      font-size: 10rem;
      text-align: center;
      margin-bottom: 0;
      color: orange; 
      font-family: 'Brittany', serif;
    }

    h2 {
      font-size: 15rem;
      text-align: center;
      margin-top: 20px;
      color: #595858; 
      font-family: 'Bebas Neue', serif;
      line-height: 60px;
    }

    .polaroid{
      background: white;
      padding: 2rem;
      box-shadow: 0 0.2rem 1.2rem rgba(0,0,0,0.2);
    }

    .polaroid img{
      max-width: 100%;
      height: auto;
    }

    .caption{
      font-family: 'Brittany', serif;
      font-size: 5rem;
      text-align: center;
      line-height: 2em;
    }

    .item{
      width: 20%;
      display: inline-block;
      margin-top: 1rem;
      filter: brightness(100%);
    }

    .item .polaroid:before{
      content: '';
      position: absolute;
      z-index: -1;
      transition: all 0.35s;
    }

    .item:nth-of-type(4n+1){
      transform: scale(0.8,0.8) rotate(-5deg);
      transition: all 0.35s;
    }

    .item:nth-of-type(4n+1) .polaroid:before{
      transform: rotate(-6deg);
      height: 10%;
      width: 20%;
      bottom: 20px;
      right: 10px;
      box-shadow: 0 2.1rem 2rem rgba(0,0,0,0.4);
    }

    .item:nth-of-type(4n+2){
      transform: scale(0.8,0.8) rotate(3deg);
      transition: all 0.35s;
    }

    .item:nth-of-type(4n+2) .polaroid:before{
      transform: rotate(4deg);
      height: 10%;
      width: 20%;
      bottom: 20px;
      right: 10px;
      box-shadow: 0 2.1rem 2rem rgba(0,0,0,0.3);
    }

    .item:nth-of-type(4n+3){
      transform: scale(0.8,0.8) rotate(-3deg);
      transition: all 0.35s;
    }

    .item:nth-of-type(4n+3) .polaroid:before{
      transform: rotate(-4deg);
      height: 10%;
      width: 20%;
      bottom: 20px;
      right: 10px;
      box-shadow: 0 2.1rem 2rem rgba(0,0,0,0.3);
    }

    .item:nth-of-type(4n+4){
      transform: scale(0.8,0.8) rotate(3deg);
      transition: all 0.35s;
    }

    .item:nth-of-type(4n+4) .polaroid:before{
      transform: rotate(4deg);
      height: 10%;
      width: 20%;
      bottom: 20px;
      right: 10px;
      box-shadow: 0 2.1rem 2rem rgba(0,0,0,0.3);
    }

    .item:hover{
      filter: none;
      transform: scale(1,1) rotate(0deg) !important;
      transition: all 0.35s;
    }

    .item:hover .polaroid:before{
      content: '';
      position: absolute;
      z-index: -1;
      transform: rotate(0deg);
      height: 90%;
      width: 90%;
      bottom: 0%;
      right: 5%;
      box-shadow: 0 1rem 3rem rgba(0,0,0,0.2);
      transition: all 0.35s;
    }

  </style>  
</head>

<body>
  <h1>INTRODUCE</h1> 
  <h2>OUR TEAM</h2>

  <div class="quote">
    "Your meal, our deal!"
  </div>

  <div class="wrapper">
    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpeg;base64,{hang_encoded_image}" alt="">
        <div class="caption">Nguyen Viet Hang</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpeg;base64,{danh_encoded_image" alt="">
        <div class="caption">Tran Duy Anh</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpeg;base64,{dung_encoded_image" alt="">
        <div class="caption">Nguyen Manh Dung</div>
      </div>
    </div>

    <div class="item">
      <div class="polaroid">
        <img src="data:image/jpeg;base64,{hieu_encoded_image" alt="">
        <div class="caption">Nguyen Minh Hieu</div>
      </div>
    </div>
</body>
</html>
    """

    # Use st.markdown to render HTML
    st.markdown(html_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
