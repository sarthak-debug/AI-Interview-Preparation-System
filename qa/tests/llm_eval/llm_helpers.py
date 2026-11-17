"""Helpers shared by the LLM evaluation tests and the report script."""
import json
import os
import re
import time
from pathlib import Path

HERE = Path(__file__).parent
GOLDEN = json.loads((HERE / "golden_dataset.json").read_text())
GUARDRAILS = json.loads((HERE / "guardrail_cases.json").read_text())

SCORE_RE = re.compile(r"Score:\s*\**\s*(\d+(?:\.\d+)?)\s*/\s*10", re.IGNORECASE)
DELAY = float(os.getenv("EVAL_DELAY", "4"))   # seconds between calls (free-tier rate limit)


def parse_score(feedback: str):
    """Return the numeric score in 'Score: x/10', or None if the format is broken."""
    m = SCORE_RE.search(feedback or "")
    return float(m.group(1)) if m else None


def has_required_sections(feedback: str) -> bool:
    low = (feedback or "").lower()
    return "strengths" in low and "improvements" in low


def run_evaluator(question: str, answer: str) -> dict:
    """Call the real app evaluator and record whether it silently fell back."""
    from answer_evaluator import evaluate_answer, fallback_evaluation

    start = time.time()
    out = evaluate_answer(question, answer)
    latency = time.time() - start
    time.sleep(DELAY)
    return {
        "feedback": out,
        "score": parse_score(out),
        "sections_ok": has_required_sections(out),
        # evaluate_answer() hides Gemini errors by returning the offline fallback text.
        "used_fallback": out.strip() == fallback_evaluation(answer).strip(),
        "latency_s": round(latency, 2),
    }
