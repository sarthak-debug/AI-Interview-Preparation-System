from resume_parser import extract_text
from skill import extract_skills

text = extract_text(
    "uploads/Sarthak Gharat-Resume.pdf"
)

skills = extract_skills(text)

print("\nDetected Skills:\n")

for skill in skills:
    print("-", skill)