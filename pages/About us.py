import streamlit as st

def main():
    st.title("Team Introduction Page")

    github_raw_url = "https://github.com/nguyenviethang193/Group-3---Recipe-and-Meal-Planner-Application/tree/main/Introduction"
    html_content = st.markdown(github_raw_url, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
