from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

from resume_parser import extract_text
from skill import extract_skills
from question_generator import generate_questions
from Ai_question_genrator import generate_ai_questions

from pydantic import BaseModel
from answer_evaluator import evaluate_answer

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5176"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = extract_text(file_path)

    skills = extract_skills(text)

    # Stored Questions
    stored_questions = generate_questions(skills)

    # AI Questions
    is_ai_fallback = False
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "":
        print("Gemini API key is missing. Loading fallback questions.")
        is_ai_fallback = True
        ai_questions = "\n".join([
            "1. What are the key differences between SQL and NoSQL databases?",
            "2. What is the difference between synchronous and asynchronous programming?",
            "3. Describe a time when you had to troubleshoot a difficult bug or production issue.",
            "4. Explain the concepts of RESTful API design.",
            "5. What is git and how do you resolve merge conflicts?"
        ])
    else:
        try:
            ai_questions = generate_ai_questions(text)
            if not ai_questions or ai_questions.strip() == "":
                raise ValueError("Empty response from Gemini")
        except Exception as e:
            print("Gemini Error:", e)
            is_ai_fallback = True
            ai_questions = "\n".join([
                "1. What are the key differences between SQL and NoSQL databases?",
                "2. What is the difference between synchronous and asynchronous programming?",
                "3. Describe a time when you had to troubleshoot a difficult bug or production issue.",
                "4. Explain the concepts of RESTful API design.",
                "5. What is git and how do you resolve merge conflicts?"
            ])

    return {
        "filename": file.filename,
        "skills": skills,
        "stored_questions": stored_questions,
        "ai_questions": ai_questions,
        "is_ai_fallback": is_ai_fallback
    }
class AnswerRequest(BaseModel):
    question: str
    answer: str


@app.post("/evaluate")
async def evaluate(data: AnswerRequest):

    feedback = evaluate_answer(
        data.question,
        data.answer
    )

    return {
        "feedback": feedback
    }