"""Run the full LLM evaluation and write a report with the numbers.

Usage (from the qa/ folder):
    python tests/llm_eval/run_eval_report.py            # each case once
    python tests/llm_eval/run_eval_report.py --repeats 3  # also measures score consistency

Writes reports/llm_eval_report.md and reports/llm_eval_results.json
"""
import argparse
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

QA = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(QA.parent / "backend"))
sys.path.insert(0, str(Path(__file__).parent))

from llm_helpers import GOLDEN, GUARDRAILS, run_evaluator  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=1)
    args = ap.parse_args()

    rows, guard_rows = [], []
    for case in GOLDEN:
        runs = [run_evaluator(case["question"], case["answer"]) for _ in range(args.repeats)]
        scores = [r["score"] for r in runs if r["score"] is not None]
        rows.append({
            "id": case["id"], "quality": case["quality"],
            "band": f"{case['min_score']}-{case['max_score']}",
            "scores": scores,
            "in_band": all(case["min_score"] <= s <= case["max_score"] for s in scores) and len(scores) == len(runs),
            "format_ok": all(r["score"] is not None and r["sections_ok"] for r in runs),
            "fallback": any(r["used_fallback"] for r in runs),
            "spread": (max(scores) - min(scores)) if len(scores) > 1 else 0,
            "latency_s": statistics.mean(r["latency_s"] for r in runs),
        })
        print(f"{case['id']:<32} scores={scores}")

    for case in GUARDRAILS:
        r = run_evaluator(case["question"], case["answer"])
        guard_rows.append({"id": case["id"], "score": r["score"], "max_allowed": case["max_score"],
                           "blocked": r["score"] is not None and r["score"] <= case["max_score"],
                           "fallback": r["used_fallback"]})
        print(f"{case['id']:<32} score={r['score']}")

    n, g = len(rows), len(guard_rows)
    pct = lambda k, rs: round(100 * sum(1 for r in rs if r[k]) / len(rs), 1)
    summary = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "golden_cases": n, "repeats": args.repeats,
        "scoring_accuracy_pct": pct("in_band", rows),
        "format_compliance_pct": pct("format_ok", rows),
        "llm_error_fallback_pct": pct("fallback", rows),
        "injection_resistance_pct": pct("blocked", guard_rows),
        "avg_latency_s": round(statistics.mean(r["latency_s"] for r in rows), 2),
        "max_score_spread": max(r["spread"] for r in rows),
    }

    out = QA / "reports"
    out.mkdir(exist_ok=True)
    (out / "llm_eval_results.json").write_text(json.dumps(
        {"summary": summary, "golden": rows, "guardrails": guard_rows}, indent=2))

    md = [f"# Prepare.AI - LLM Evaluation Report ({summary['date']})", "",
          "| Metric | Value |", "|---|---|",
          f"| Golden cases | {n} (x{args.repeats} runs) |",
          f"| Scoring accuracy (score in expected band) | {summary['scoring_accuracy_pct']}% |",
          f"| Output format compliance | {summary['format_compliance_pct']}% |",
          f"| Prompt-injection resistance | {summary['injection_resistance_pct']}% ({g} attacks) |",
          f"| Silent LLM failures (fallback used) | {summary['llm_error_fallback_pct']}% |",
          f"| Average latency | {summary['avg_latency_s']} s |",
          f"| Max score spread across repeats | {summary['max_score_spread']} |", "",
          "## Golden dataset", "", "| Case | Quality | Expected | Scores | Pass |", "|---|---|---|---|---|"]
    md += [f"| {r['id']} | {r['quality']} | {r['band']} | {r['scores']} | {'✅' if r['in_band'] else '❌'} |" for r in rows]
    md += ["", "## Guardrails", "", "| Attack | Score | Max allowed | Blocked |", "|---|---|---|---|"]
    md += [f"| {r['id']} | {r['score']} | {r['max_allowed']} | {'✅' if r['blocked'] else '❌'} |" for r in guard_rows]
    (out / "llm_eval_report.md").write_text("\n".join(md) + "\n")
    print("\n" + json.dumps(summary, indent=2))
    print(f"\nReport written to {out / 'llm_eval_report.md'}")


if __name__ == "__main__":
    main()
