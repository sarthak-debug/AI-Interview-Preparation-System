from resume_parser import extract_text

text = extract_text(
    "uploads/Sarthak Gharat-Resume.pdf"
)


print(text[:2000])