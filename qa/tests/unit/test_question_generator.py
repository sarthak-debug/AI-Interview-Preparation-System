"""Unit tests for question_generator.generate_questions (static question bank)."""
from question_generator import QUESTION_BANK, generate_questions


def test_returns_questions_for_known_skill():
    assert generate_questions(["python"]) == QUESTION_BANK["python"]


def test_unknown_skill_is_ignored():
    assert generate_questions(["cobol"]) == []


def test_multiple_skills_are_combined_in_order():
    qs = generate_questions(["sql", "git"])
    assert qs == QUESTION_BANK["sql"] + QUESTION_BANK["git"]


def test_every_bank_entry_is_a_non_empty_question():
    for skill, questions in QUESTION_BANK.items():
        assert questions, f"{skill} has no questions"
        for q in questions:
            assert q.strip().endswith("?"), f"Not a question: {q!r}"
