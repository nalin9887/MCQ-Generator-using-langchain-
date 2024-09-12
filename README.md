# MCQ Generator (Powered by Gemini)

This is a Python-based application that generates multiple-choice questions (MCQs) using Google's Gemini AI. The app allows users to upload a text file or input a webpage URL to create MCQs based on the content. The MCQs can then be downloaded in PDF, Word, or as an answer key.

## Features

- **Generate MCQs**: Create a custom quiz with a specified number of questions and tone (simple, neutral, professional).
- **Upload or URL**: Input can be provided via a text file or a webpage URL.
- **Download Options**: Download the generated quiz as PDF, Word document, or download the answer key.
- **Error Handling**: Automatic retries and informative messages for better user experience.
  
## Technologies Used

- **Streamlit**: For the app interface.
- **Google Gemini AI**: For generating MCQs based on input content.
- **BeautifulSoup**: For web scraping and extracting text from webpage URLs.
- **ReportLab**: For generating PDF documents.
- **python-docx**: For generating Word documents.
- **dotenv**: For managing environment variables.
- **requests**: For handling HTTP requests.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/mcq-generator.git
    ```

2. Navigate to the project directory:

    ```bash
    cd mcq-generator
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables in a `.env` file:

    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Upload a text file or enter a webpage URL.
3. Specify the number of MCQs and the tone.
4. Generate the quiz and download it in the desired format.

## Example

```python
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-pro')
text = "Sample text for generating questions."
number = 5
tone = "neutral"

prompt = f"""
Text: {text}

Create a quiz of {number} multiple choice questions in {tone} tone.
"""
response = model.generate_content(prompt)
print(response.text)
