from question_generator import generate_questions

skills = [
    "python",
    "react",
    "git"
]

questions = generate_questions(skills)

for i, q in enumerate(questions, start=1):
    print(f"{i}. {q}")