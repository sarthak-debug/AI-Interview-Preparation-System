"""Feedback-quality evaluation with DeepEval's G-Eval metric, using Gemini as the judge model.

Pass/fail on a score band is not enough for a non-deterministic LLM, so G-Eval scores
(0-1) whether the feedback is accurate, specific and grounded in the candidate's answer.
"""
import os

import pytest

from llm_helpers import GOLDEN, run_evaluator

pytestmark = pytest.mark.llm

# A small, balanced subset keeps cost and rate-limit pressure low.
SUBSET = [c for c in GOLDEN if c["id"] in {
    "py-decorator-strong", "py-decorator-wrong", "react-hooks-partial",
    "sql-join-strong", "js-closure-wrong", "rest-api-strong",
}]


@pytest.fixture(scope="module")
def metric():
    from deepeval.metrics import GEval
    from deepeval.models import GeminiModel

    try:
        from deepeval.test_case import SingleTurnParams as P
    except ImportError:  # older deepeval versions
        from deepeval.test_case import LLMTestCaseParams as P

    judge = GeminiModel(model="gemini-2.5-flash", api_key=os.environ["GEMINI_API_KEY"], temperature=0)
    return GEval(
        name="Feedback Groundedness",
        evaluation_steps=[
            "Read the interview question (input) and the grader's feedback (actual output).",
            "The candidate's answer and its known quality are in the expected output.",
            "Check that the score matches the true quality of the answer.",
            "Check that every strength mentioned is actually present in the candidate's answer (no invented praise).",
            "Check that factual errors in the answer are pointed out under Improvements.",
            "Penalise vague, generic feedback that could apply to any answer.",
        ],
        evaluation_params=[P.INPUT, P.ACTUAL_OUTPUT, P.EXPECTED_OUTPUT],
        model=judge,
        threshold=0.6,
        async_mode=False,
    )


@pytest.mark.parametrize("case", SUBSET, ids=[c["id"] for c in SUBSET])
def test_feedback_is_grounded(case, metric):
    from deepeval import assert_test
    from deepeval.test_case import LLMTestCase

    r = run_evaluator(case["question"], case["answer"])
    test_case = LLMTestCase(
        input=case["question"],
        actual_output=r["feedback"],
        expected_output=(
            f"Candidate answer: {case['answer']}\n"
            f"True quality: {case['quality']} (fair score {case['min_score']}-{case['max_score']}/10)"
        ),
    )
    assert_test(test_case, [metric])
