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
DELAY = float(os.getenv("EVAL_DELAY", "12"))   # seconds between calls (free-tier rate limit)
RETRIES = int(os.getenv("EVAL_RETRIES", "3"))  # retries when Gemini fails (e.g. 429 rate limit)


def parse_score(feedback: str):
    """Return the numeric score in 'Score: x/10', or None if the format is broken."""
    m = SCORE_RE.search(feedback or "")
    return float(m.group(1)) if m else None


def has_required_sections(feedback: str) -> bool:
    low = (feedback or "").lower()
    return "strengths" in low and "improvements" in low


def run_evaluator(question: str, answer: str) -> dict:
    """Call the real app evaluator. If Gemini fails (usually a 429 rate limit), the app
    silently returns its offline fallback text - we detect that, wait and retry, so a
    rate limit is never mistaken for a real grade."""
    from answer_evaluator import evaluate_answer, fallback_evaluation

    fallback_text = fallback_evaluation(answer).strip()
    for attempt in range(RETRIES + 1):
        start = time.time()
        out = evaluate_answer(question, answer)
        latency = time.time() - start
        used_fallback = out.strip() == fallback_text
        time.sleep(DELAY)
        if not used_fallback:
            break
        if attempt < RETRIES:
            wait = 30 * (attempt + 1)
            print(f"  Gemini failed (probably rate limit) - retrying in {wait}s")
            time.sleep(wait)
    return {
        "feedback": out,
        "score": parse_score(out),
        "sections_ok": has_required_sections(out),
        "used_fallback": used_fallback,
        "latency_s": round(latency, 2),
    }
