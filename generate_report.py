import streamlit as st
from fpdf import FPDF
import base64
import pandas as pd
import subprocess
import openai
import os
from streamlit_lottie import st_lottie
import json
import requests

openai.api_key = "YOUR_OPENAI_KEY"


# Function to generate a sample report


def generate_report():
    # Read data from CSV file
    df = pd.read_csv(
        "full_system_info_for_carbon_footprint_and_performance_analysis.csv"
    )

    # Now you can work with your dataframe 'df'
    categories_of_interest = [
        "CPU",
        "Memory",
        "Disk",
        "Network",
        "GPU",
        "System",
        "Power",
        "Hardware",
        "Energy",
        "Performance",
    ]

    data_summary = {category: {} for category in categories_of_interest}

    max_details_per_category = 40

    for _, row in df.iterrows():
        category = row["Category"]
        subcategory = row["Subcategory"]
        detail = row["Detail"]
        value = row["Value"]
        if category in categories_of_interest:
            key = (
                f"{subcategory}: {detail}"
                if pd.notna(subcategory) and subcategory.strip()
                else detail
            )
            if len(data_summary[category]) < max_details_per_category:
                data_summary[category][key] = value

    formatted_summary_list = [
        f"{category} - {', '.join([f'{key}: {value}' for key, value in details.items()])}"
        for category, details in data_summary.items()
        if details
    ]
    formatted_summary = "\n".join(formatted_summary_list)

    return formatted_summary


# Function to generate PDF and download
def download_pdf(report_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_data)
    pdf_file_path = "report.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path


# Function to generate environmental report
def generate_environmental_report(csv_data_summary):
    prompt_text = f"""
    Based on the provided summary of an operating system's hardware and usage specifics, generate a detailed report that includes the following:

    1. Introduction: A detailed overview of the operating system's hardware and usage specifics.

    2. Methodology: Explanation of how data was extracted and analyzed. Include any assumptions made about energy consumption, carbon footprint calculations, and environmental scoring due to data gaps. If specific information is unavailable, make reasoned assumptions based on industry standards. For CPU and GPU Power Consumption: Consult sources detailing average power consumption for CPUs and GPUs, including variations by model and workload. (e.g., cpubenchmark.net, buildcomputers.net). For RAM and Storage Devices: Look into the energy usage of RAM (DDR3, DDR4) and storage devices (SSD vs. HDD), focusing on their efficiency and impact on overall system power consumption. (e.g., buildcomputers.net, computerhope.com). For Motherboard and System Power Usage: Gather information on the power requirements of motherboards and overall system configurations, especially considering high-end gaming setups and workstation builds. (e.g., whatsabyte.com).For Power Management and Energy Consumption: Review strategies for power management and direct measurements or estimates of energy consumption, including the role of battery health in portable systems. (e.g., computerhope.com for general power usage guidelines)

    3. Analysis Findings:
        - Energy Consumption Estimation: Detailed breakdown of energy consumption by component (CPU, GPU, RAM, Storage, etc.), based on the provided data and assumptions where necessary.
        - Carbon Footprint Calculation: Conversion of energy consumption estimates into CO2 equivalents, using assumed values as needed. Also show the actual calculations and the results in the report.
        - Environmental Score Assessment: Evaluation of other environmental impacts, such as e-waste and resource depletion, with assumptions clearly stated.

    4. Recommendations: Five actionable advices for reducing environmental impact and improving energy efficiency, tailored to the findings and assumptions.

    5. Conclusion: Summary of key insights and potential benefits of implementing the recommendations.

    Data Summary for Analysis:
    {csv_data_summary}

    Please make reasoned assumptions based on industry standards in cases where specific data points are missing. Avoid making unsubstantiated claims. Ensure the report is comprehensive, clearly articulating calculations, assumptions, findings, and recommendations for environmental improvement.Make sure to show all calculations made in the report.
    Don't merely write calculation were done. Show the actual calculations and the results in the report.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": "The following is a request for a detailed analysis report. Strictly follow the guidelines provided.",
                },
                {"role": "user", "content": prompt_text},
            ],
        )
        model_response = response.choices[0].message.content

        return model_response
    except Exception as e:
        return str(e)


# Main function to run the Streamlit app
def generate_report_page():

    # with open("Apple.json", "r") as f:
    #     animation_content = json.load(f)

    # st_lottie(animation_content, speed=1, height=300, key="animation")
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url = "https://lottie.host/a6801a99-405c-4300-b28f-fde46738ed39/LLzRJzXf8p.json"

    lottie_animation = load_lottieurl(lottie_url)
    if lottie_animation:
        st_lottie(lottie_animation, height=400, key="lottie")
    else:
        st.error("Failed to load Lottie animation.")

    pdf_file_path = ""

    st.title("Carbon Footprint Report")

    st.info(
        """
    🌍 **Empower Your Green Impact!**
    Start your journey to sustainability by making informed decisions with your very own Carbon Footprint Report. Here's how to leap into action:
    
    - **Generate Your System CSV**: Haven't checked your system's details yet? Head over to **System Details CSV** to generate your CSV report. It's your first step towards eco-conscious computing!
    
    - **Smart Carbon Accounting**: With our State-Of-The-Art Language Models, get a precise estimation of your carbon footprint and other environmental impacts directly from your system's data.
    
    - **Actionable Insights**: Our detailed reports go beyond mere numbers. They provide you with actionable advice to enhance your sustainability efforts and make every choice count.
    
    - **Lead with Purpose**: Armed with the power of cutting-edge AI, become a champion of environmental stewardship. Every decision you make with our guidance is a step towards a healthier planet.
    
    Let's join hands to create a sustainable future, one decision at a time. Your eco-journey begins now!
    """
    )

    st.write("")  # Add some space
    st.header("Upload System Details CSV")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Awaiting Upload ", type=["csv"])

    # Check if file is uploaded

    if uploaded_file is not None:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        # Show uploaded data
        st.write("Uploaded CSV:")
        st.write(df)

        script_directory = os.path.dirname(__file__)
        save_path = os.path.join(script_directory, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"CSV file saved successfully as {save_path}")
        if st.button("Generate Report"):
            report_data = generate_report()

            # Generate environmental report
            environmental_report = generate_environmental_report(report_data)
            st.write(environmental_report)
            st.success("Report generated successfully!")

            # Download PDF
            pdf_file_path = download_pdf(environmental_report)
            download_pdf_link(pdf_file_path)


def download_pdf_link(pdf_file_path1):

    with open(pdf_file_path1, "rb") as file:
        pdf_bytes = file.read()
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="report.pdf">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

    return pdf_file_path1


if __name__ == "__main__":
    generate_report_page()
