"""Safety tests: candidates must not be able to talk the grader into a high score.

Covers prompt injection, fake system messages, role-play jailbreaks and off-topic answers.
"""
import pytest

from llm_helpers import GUARDRAILS, run_evaluator

pytestmark = pytest.mark.llm


@pytest.mark.parametrize("case", GUARDRAILS, ids=[c["id"] for c in GUARDRAILS])
def test_grader_resists_manipulation(case):
    r = run_evaluator(case["question"], case["answer"])
    assert not r["used_fallback"], "Gemini call failed - fallback used"
    assert r["score"] is not None, "Output format broken"
    assert r["score"] <= case["max_score"], (
        f"Injection succeeded: scored {r['score']}/10 (allowed max {case['max_score']})\n{r['feedback']}"
    )
