import streamlit as st
from PyPDF2 import PdfReader
import os
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import openai
import speech_recognition as sr
from gtts import gTTS
import io
from audio_recorder_streamlit import audio_recorder

openai.api_key = "YOUR_OPENAI_KEY"

conversation_history = []


def add_message_to_history(role, content):
    conversation_history.append({"role": role, "content": content})


def initialize_conversation_environment(report_text):
    conversation_history.clear()
    system_prompt = (
        "This is a conversation with an AI trained as an environmentalist. "
        "The AI provides advice based on environmental principles and the detailed report provided."
    )
    add_message_to_history("system", system_prompt)
    if report_text:
        add_message_to_history("system", f"Report Summary: {report_text}")


def query_gpt(text):
    add_message_to_history("user", text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
        )
        model_response = response["choices"][0]["message"]["content"]

        add_message_to_history("assistant", model_response)

        return model_response
    except Exception as e:
        return str(e)


def read_pdf(uploaded_file):
    file_path = "temp.pdf"
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() if page.extract_text() else ""

    os.remove(file_path)
    return text


def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    audio_file = io.BytesIO(audio_bytes)

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        duration = len(audio_data.frame_data) / (
            audio_data.sample_rate * audio_data.sample_width
        )

        if duration < 1.5:
            return "Audio too short. Please record a longer message.", False
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Sorry, I couldn't understand that. Please try again."
    return text, True


def text_to_speech(text):
    """
    Converts text to speech, returning an audio byte stream.
    """
    tts = gTTS(text=text, lang="en")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp


def chatbot_page():

    with open("Heuristics.json", "r") as f:
        animation_content = json.load(f)

    st_lottie(animation_content, speed=1, height=300, key="animation")

    st.title("GreenGizmo: AI Environmentalist")

    st.info(
        """
    🌱 **Your Personal AI Environmentalist Awaits!**
    GreenGizmo transforms your eco-efforts with AI-powered guidance. Make the most out of your journey to sustainability with a friendly and knowledgeable companion. Here's how to maximize your GreenGizmo experience:
    
    - **Carbon Insights to Action**: Generated a Carbon Footprint Report? Turn it into a PDF and bring it to GreenGizmo. Our AI has been specially trained to provide personalized advice based on your report.
    
    - **Don't Forget Your PDF**: Before starting your session with GreenGizmo, make sure to upload your Carbon Footprint Report PDF. It’s crucial for tailoring the advice you'll receive, ensuring it's perfectly aligned with your environmental impact.
    
    - **24/7 Eco-Assistant**: Whether you're a night owl or an early bird, GreenGizmo is here to chat or listen anytime. Get tips on reducing your carbon footprint, learn about eco-friendly habits, and take meaningful steps towards sustainability.
    
    - **Interactive and Enlightening**: With GreenGizmo, learning about environmental stewardship becomes an engaging experience. Choose your preferred interaction style and dive into a wealth of knowledge that grows with you.
    
    Ready to make a difference? Your AI environmentalist is just a PDF upload away. Let’s embark on this green journey together and pave the way to a sustainable future.
    """
    )

    uploaded_file = st.file_uploader("Awaiting Carbon Footprint Report", type="pdf")
    if uploaded_file is not None:
        pdf_text = read_pdf(uploaded_file)
        st.info("Successfully uploaded the PDF file.")
        initialize_conversation_environment(pdf_text)

    st.write("## Welcome to GreenGizmo! How can I assist you today?")

    selected = option_menu(
        None,
        ["GG Chatbot", "GG Voice Assistant"],
        icons=["chat-left-text", "voicemail"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    if selected == "GG Chatbot":
        st.info("You're in the Chatbot section.")
        user_message = st.text_input("Type your message here:")
        send_button = st.button("Send Message")

        if send_button:
            model_response = query_gpt(user_message)
            st.write("Your message:", user_message)
            st.write("GG says:", model_response)
    elif selected == "GG Voice Assistant":
        st.info("You're in the Voice Assistant section.")
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
            process_button = st.button("Process Recording")
            if process_button:
                user_message, proceed = speech_to_text(audio_bytes)
                if proceed:
                    st.write("Your message:", user_message)
                    model_response = query_gpt(user_message)
                    response_audio = text_to_speech(model_response)
                    st.audio(response_audio, format="audio/mp3")
                else:
                    st.write(user_message)


if __name__ == "__main__":
    chatbot_page()
