
SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "express",
    "flask",
    "fastapi",
    "sql",
    "mysql",
    "mongodb",
    "git",
    "github",
    "html",
    "css",
    "tailwind",
    "opencv",
    "machine learning",
    "ai",
]

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))