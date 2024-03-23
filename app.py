import streamlit as st
from introduction import introduction_page
from generate_report import generate_report_page
from chatbot import chatbot_page
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import subprocess
import os, time

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="GreenScript AI", layout="wide")

    with open('keyfinal.json', 'r', encoding='utf-8') as f:
        animation_content = json.load(f)

    # Set Streamlit theme based on config
    with st.sidebar:
        st_lottie(animation_content, speed=1, height=250, key="sidebar_animation")
    st.sidebar.title("Trailblaze the Scriptscape")

    # Define navigation pages
    pages = {
        "Know The Initiative": introduction_page,
        "Carbon Footprint Report": generate_report_page,
        "GreenGizmo: Voice and Chat": chatbot_page
    }

    # Display the navigation options
    selection = st.sidebar.radio("Explore GreenScript AI", list(pages.keys()))
    page = pages[selection]
    page()

    # Add "Connect with Us" heading and buttons
    st.write("")
    st.write("")

    st.markdown(
        """
<style>
div.stButton > button:first-child {
    background-color: #FF4B4B;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #FF0000;
    color:#ffffff;
    transform: scale(1.05);
}
</style>""",
        unsafe_allow_html=True,
    )

    # Connect with Us section
    st.sidebar.header("Connect with Us")

    with st.sidebar:
        selected = option_menu(
            menu_title=None,  # Title is already provided above
            options=["Email", "Phone"],
            icons=["envelope", "telephone"],
            menu_icon="cast",  # Menu icon is optional
            default_index=0,
            orientation="vertical",
        )

    # Display the contact information based on selection
    if selected == "Email":
        st.sidebar.code("bpdps95@hotmail.com")

    elif selected == "Phone":
        st.sidebar.code("+91 9831268042")

if __name__ == "__main__":
    main()
