from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def fallback_evaluation(answer):

    words = len(answer.split())

    if words < 20:
        return """
Score: 4/10

Strengths:
- Attempted the question

Improvements:
- Answer is too short
- Add technical explanation
- Provide examples
"""

    elif words < 50:
        return """
Score: 6/10

Strengths:
- Basic understanding shown

Improvements:
- Add more details
- Include real-world examples
"""

    else:
        return """
Score: 8/10

Strengths:
- Detailed answer
- Good explanation

Improvements:
- Add advanced concepts
- Mention practical applications
"""


def evaluate_answer(question, answer):

    try:

        prompt = f"""
Evaluate the following interview answer.

Question:
{question}

Answer:
{answer}

Provide:

Score: x/10

Strengths:
- ...

Improvements:
- ...
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print("Gemini Error:", e)

        return fallback_evaluation(answer)