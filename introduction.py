import streamlit as st
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu
import subprocess
import os, time

def introduction_page():

    with open('Welcome.json', 'r') as f:
        animation_content = json.load(f)

    st_lottie(animation_content, speed=1, height=300, key="animation")

    st.title("GreenScript AI: Work Sutainabily, Impact Globally")
    st.markdown("## Green Computing Redefined")

    # Create two columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("System Details CSV")
        st.markdown(
            """
            - **Comprehensive Analysis**: Instant Specs Report.
            - **Easy to Use**: Bash-Powered Ease.
            - **Optimization Insights**: Make Informed Decisions.
        """
        )

    with col2:
        st.subheader("Carbon Footprint Report Maker")
        st.markdown(
            """
            - **Sustainable Insights**: Eco Impact Analysis.
            - **Eco-Friendly Decisions**: Empowering environmental friendliness.
            - **Comprehensive Reports**: Detailed Environmental Scores.
        """
        )

    with col3:
        st.subheader("GreenGizmo")
        st.markdown(
            """
            - **AI-Powered Assistance**: AI-guided chat and voice assistance.
            - **Environmentally Conscious**: Greener Choices Guide.
            - **24/7 Support**: Eco support anytime, anywhere.
        """
        )

    st.markdown("---")

    # selected = option_menu(
    #     menu_title=None,
    #     options=["System Details CSV", "AI Interviewer", "Resume Enhancer"],
    #     icons=["play-circle", "robot", "file-earmark-text"],
    #     default_index=0,
    #     orientation="horizontal",
    # )
    selected = option_menu(
        menu_title=None,
        options=[
            "System Details CSV",
            "Carbon Footprint Report Maker",
            "Green Gizmo",
        ],
        icons=["play-circle", "cpu", "robot"],
        default_index=0,
        orientation="horizontal",
    )

    if selected == "System Details CSV":
        # Button to run the system_info.sh script

        st.info(
        """
        🚀 **Unlock Your System's Full Potential!**
        - **Instant Deep Dive**: Effortlessly generate a detailed CSV report of your system’s specifications using sophisticated bash scripts.
        - **Powerful Insights at Your Fingertips**: Discover critical data about your RAM, CPU, and memory to supercharge your system's performance.
        - **Simplicity Meets Efficiency**: Get comprehensive system analytics with just a few clicks. Perfect for upgrades or optimizations.
        """
            )
        if st.button("Generate System Info CSV"):
            st.info("Generating system info CSV...")
            # Assuming system_info.sh is executable and in the correct path
            cmd = "sudo ./system_info.sh"
            try:
                # Execute the script and capture output
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                output = result.stdout
                error_output = result.stderr

                # Display the output in the Streamlit app
                if output:
                    st.success("Script executed successfully! Here's the output:")
                    st.code(output, language="bash")
                if error_output:
                    st.error(f"Script executed with errors: {error_output}")

                # Check if the output file exists and offer it for download
                output_file = (
                    "full_system_info_for_carbon_footprint_and_performance_analysis.csv"
                )
                if os.path.exists(output_file):
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="Download System Info CSV",
                            data=file,
                            file_name=output_file,
                            mime="text/csv",
                        )
            except subprocess.CalledProcessError as e:
                st.error(f"Script execution failed: {e}")
    # Other options handling...

    elif selected == "Carbon Footprint Report Maker":
        st.info(
            """
            🌿 **Eco-Warriors, Make Your Mark!**
            - **Smart Carbon Accounting**: Employ State-Of-The-Art Language Models to precisely estimate your carbon footprint and environmental impact.
            - **Beyond Numbers**: Receive detailed, actionable reports that empower you to make greener choices and drive sustainability forward.
            - **Champion Environmental Stewardship**: Utilize cutting-edge AI to guide your eco-friendly decisions, making a real difference for our planet.
            """
        )

    elif selected == "Green Gizmo":
        st.info(
            """
            🌟 **Navigate Your Green Journey with Ease!**
            - **Always-On Eco Companion**: Leverage an AI-powered chat and voice assistant dedicated to helping you live more sustainably, 24/7.
            - **Empower Your Choices**: From tips on reducing your carbon footprint to adopting eco-friendly habits, GreenGizmo is here to guide you.
            - **Engage, Learn, Grow**: Whether you prefer typing or talking, our interactive assistant makes your quest for a greener lifestyle both fun and informative.
            """
        )
