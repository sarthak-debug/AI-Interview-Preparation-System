"""Unit tests for skill.extract_skills (keyword matching on resume text)."""
import pytest

from skill import extract_skills


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Skilled in Python and SQL", {"python", "sql"}),
        ("REACT developer", {"react"}),                       # case-insensitive
        ("Tools: Git, GitHub", {"git", "github"}),
        ("C++ and OpenCV projects", {"c++", "opencv"}),
        ("Machine Learning with FastAPI", {"machine learning", "fastapi"}),
    ],
)
def test_detects_listed_skills(text, expected):
    assert expected.issubset(set(extract_skills(text)))


def test_empty_text_returns_no_skills():
    assert extract_skills("") == []


def test_no_duplicate_skills():
    skills = extract_skills("python python PYTHON")
    assert skills.count("python") == 1


# ---- Bugs found by these tests (kept as strict xfail until fixed) ----

@pytest.mark.xfail(strict=True, reason="BUG-01: substring match - 'ai' is found inside 'email'/'maintain'")
def test_ai_not_detected_inside_other_words():
    assert "ai" not in extract_skills("Email: someone@mail.com. I maintain websites.")


@pytest.mark.xfail(strict=True, reason="BUG-02: 'java' is detected when the resume only says 'JavaScript'")
def test_java_not_detected_from_javascript():
    assert "java" not in extract_skills("Frontend developer using JavaScript")


@pytest.mark.xfail(strict=True, reason="BUG-03: 'express' matches the ordinary word 'expressed'")
def test_express_not_detected_from_plain_english():
    assert "express" not in extract_skills("I expressed interest in data science")
