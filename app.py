import streamlit as st
import os
import json
import pandas as pd
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Define the response JSON structure
RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

def generate_mcqs(text, number, tone):
    prompt = f"""
    Text: {text}
    
    You are an expert MCQ maker. Given the above text, create a quiz of {number} multiple choice questions in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to conform to the text.
    Format your response like the RESPONSE_JSON below and use it as a guide. 
    Ensure to make {number} MCQs.
    
    RESPONSE_JSON:
    {json.dumps(RESPONSE_JSON)}
    """
    
    response = model.generate_content(prompt)
    return response.text

def process_mcqs(quiz):
    # Remove any markdown code block syntax if present
    quiz = quiz.replace("```json", "").replace("```", "").strip()
    quiz = json.loads(quiz)
    quiz_table_data = []
    for key, value in quiz.items():
        mcq = value["mcq"]
        options = " | ".join(
            [f"{option}: {option_value}" for option, option_value in value["options"].items()]
        )
        correct = value["correct"]
        quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
    
    return pd.DataFrame(quiz_table_data)

def get_webpage_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

# Streamlit UI
st.set_page_config(layout="wide")
st.title("MCQ Generator (Powered by Gemini)")

# Sidebar
st.sidebar.header("Controls")
number_of_questions = st.sidebar.number_input("Number of questions", min_value=1, max_value=20, value=5)
tone = st.sidebar.selectbox("Tone", options=["simple", "neutral", "professional"])

# Main area
tab1, tab2 = st.tabs(["Upload File", "Enter URL"])

with tab1:
    uploaded_file = st.file_uploader("Choose a text file", type="txt")

with tab2:
    webpage_url = st.text_input("Enter a webpage URL")

if st.sidebar.button("Generate MCQs"):
    if uploaded_file is not None:
        text = uploaded_file.getvalue().decode("utf-8")
    elif webpage_url:
        text = get_webpage_content(webpage_url)
    else:
        st.error("Please upload a file or enter a webpage URL")
        st.stop()
    
    with st.spinner("Generating MCQs..."):
        quiz = generate_mcqs(text, number_of_questions, tone)
        quiz_df = process_mcqs(quiz)
        
        st.subheader("Generated MCQs")
        st.dataframe(quiz_df, use_container_width=True)
        
        csv = quiz_df.to_csv(index=False)
        st.download_button(
            label="Download MCQs as CSV",
            data=csv,
            file_name="mcqs.csv",
            mime="text/csv",
        )

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info("This app generates multiple-choice questions (MCQs) based on the provided text or webpage content using Google's Gemini AI. Upload a text file or enter a webpage URL, specify the number of questions and tone, then click 'Generate MCQs' to create your quiz.")