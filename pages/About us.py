import streamlit as st

def main():
    # Read HTML file content
    with open("https://github.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/blob/main/Introduction/polaroid.html", "r") as f:
        html_content = f.read()

    # Use st.markdown to display HTML content
    st.markdown(html_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
