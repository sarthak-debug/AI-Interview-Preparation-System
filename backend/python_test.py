from resume_parser import extract_text
from Ai_question_genrator import generate_ai_questions

text = extract_text(
    "uploads/Sarthak Gharat-Resume.pdf"
)

questions = generate_ai_questions(text)

print(questions)