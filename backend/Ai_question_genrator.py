import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_ai_questions(resume_text):

    prompt = f"""
    Analyze this resume.

    Generate 10 technical interview questions.

    Resume:
    {resume_text}

    Return only questions.
    """

    response = model.generate_content(prompt)

    return response.text