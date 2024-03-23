# TechDisrupt - GreenScript AI

Welcome to GreenScript AI, your comprehensive solution for sustainable computing and environmental stewardship. This project aims to empower users with tools and insights to make eco-friendly choices, reduce carbon footprints, and contribute to a greener planet.

## Features

### 1. System Details CSV Generation
Generate detailed CSV reports of your system's specifications with just a few clicks. Get insights into your RAM, CPU, and memory to optimize your system's performance.

   - **Comprehensive Analysis**: Instant Specs Report.
   - **Easy to Use**: Bash-Powered Ease.
   - **Optimization Insights**: Make Informed Decisions.

### 2. Carbon Footprint Report Maker
Estimate your carbon footprint and environmental impact using state-of-the-art language models. Receive actionable reports to make greener choices and drive sustainability forward.

   - **Smart Carbon Accounting**: Employ State-Of-The-Art Language Models to precisely estimate your carbon footprint and environmental impact.
   - **Beyond Numbers**: Receive detailed, actionable reports that empower you to make greener choices and drive sustainability forward.
   - **Champion Environmental Stewardship**: Utilize cutting-edge AI to guide your eco-friendly decisions, making a real difference for our planet.

### 3. GreenGizmo AI Assistant
Leverage an AI-powered chat and voice assistant dedicated to helping you live more sustainably, 24/7. Get tips on reducing your carbon footprint, adopt eco-friendly habits, and engage in an interactive learning experience.

   - **Always-On Eco Companion**: Leverage an AI-powered chat and voice assistant dedicated to helping you live more sustainably, 24/7.
   - **Empower Your Choices**: From tips on reducing your carbon footprint to adopting eco-friendly habits, GreenGizmo is here to guide you.
   - **Engage, Learn, Grow**: Whether you prefer typing or talking, our interactive assistant makes your quest for a greener lifestyle both fun and informative.

## Installation

### For Ubuntu/Debian Users

Follow these steps to run GreenScript AI locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/GreenScript-AI.git

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Install additional system packages:**
   ```bash
   sudo apt-get update && sudo apt-get install -y linux-tools-common linux-tools-generic dmidecode sysstat net-tools iproute2 pciutils intel-gpu-tools coreutils procps upower util-linux && sudo ubuntu-drivers autoinstall


### For Non-Ubuntu/Debian Users
1. **Install Docker on your machine:**
Please refer to [Docker documentation](https://docs.docker.com/?_gl=1*8yx55*_ga*MTg4MDA5NzI0Ni4xNzEwODI3NDAy*_ga_XJWPQMJYHQ*MTcxMDgyNzQwMS4xLjAuMTcxMDgyNzQwMS42MC4wLjA.) for installation instructions.

2. **Build the Docker image:**
   ```bash
   docker build -t techdisrupt_app .

3. **Run the Docker container, exposing the necessary ports:**
   ```bash
   docker run -p 8501:8501 techdisrupt_app

## Usage

**To launch the Streamlit application, run the following command in your terminal:**
   ```bash
streamlit run app.py
```

`Note if you are using docker the command will automatically execute`

Once the application is running, navigate through the different pages to explore the features offered by GreenScript AI.

## Configuration

The theme of the Streamlit application can be customized using the config.toml file. Modify the theme settings according to your preferences.

## Acknowledgements

[Streamlit](https://docs.streamlit.io) - For providing the platform to create interactive web applications with Python.

[OpenAI](https://platform.openai.com/docs/introduction) - For providing the GPT-3.5 model used in the chatbot feature.
