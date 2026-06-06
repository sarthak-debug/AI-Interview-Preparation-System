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
    allow_origins=["http://localhost:5173"],
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
    try:
        ai_questions = generate_ai_questions(text)
    except Exception as e:
        print("Gemini Error:", e)
        ai_questions = "AI questions unavailable (quota exceeded)"

    return {
        "filename": file.filename,
        "skills": skills,
        "stored_questions": stored_questions,
        "ai_questions": ai_questions
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