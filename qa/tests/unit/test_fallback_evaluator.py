"""Unit tests for the offline fallback scorer used when Gemini is unavailable."""
import re

import pytest

from answer_evaluator import fallback_evaluation

SCORE_RE = re.compile(r"Score:\s*(\d+)/10")


@pytest.mark.parametrize(
    "words, expected_score",
    [(5, 4), (19, 4), (20, 6), (49, 6), (50, 8), (200, 8)],   # boundary values
)
def test_score_bands_by_answer_length(words, expected_score):
    out = fallback_evaluation(" ".join(["word"] * words))
    assert int(SCORE_RE.search(out).group(1)) == expected_score


def test_output_has_the_format_the_frontend_parses():
    out = fallback_evaluation("short answer")
    assert "Score:" in out and "Strengths:" in out and "Improvements:" in out
