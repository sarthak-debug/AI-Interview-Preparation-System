"""Golden-dataset regression tests: Gemini's score must land in the expected band for each answer.

Run:  pytest -m llm tests/llm_eval
"""
import pytest

from llm_helpers import GOLDEN, run_evaluator

pytestmark = pytest.mark.llm


@pytest.mark.parametrize("case", GOLDEN, ids=[c["id"] for c in GOLDEN])
def test_score_is_in_expected_band(case):
    r = run_evaluator(case["question"], case["answer"])

    if r["used_fallback"]:
        pytest.skip("Gemini still failing after retries (rate limit) - no real grade")
    assert r["score"] is not None, f"Output format broken (no 'Score: x/10'):\n{r['feedback']}"
    assert r["sections_ok"], "Missing Strengths/Improvements sections the frontend needs"
    assert case["min_score"] <= r["score"] <= case["max_score"], (
        f"{case['quality']} answer scored {r['score']}, expected "
        f"{case['min_score']}-{case['max_score']}"
    )
