"""API tests for POST /evaluate. The LLM call is mocked."""
import main


def test_evaluate_returns_feedback(client, monkeypatch):
    calls = {}

    def fake_eval(question, answer):
        calls["args"] = (question, answer)
        return "Score: 7/10\n\nStrengths:\n- Clear\n\nImprovements:\n- Add example"

    monkeypatch.setattr(main, "evaluate_answer", fake_eval)
    r = client.post("/evaluate", json={"question": "What is a JOIN?", "answer": "Combines rows."})

    assert r.status_code == 200
    assert r.json()["feedback"].startswith("Score: 7/10")
    assert calls["args"] == ("What is a JOIN?", "Combines rows.")


def test_missing_answer_field_is_rejected(client):
    r = client.post("/evaluate", json={"question": "What is a JOIN?"})
    assert r.status_code == 422


def test_wrong_type_is_rejected(client):
    r = client.post("/evaluate", json={"question": 123, "answer": ["not", "text"]})
    assert r.status_code == 422


def test_llm_failure_still_returns_fallback_score(client, monkeypatch):
    """If Gemini raises, the evaluator falls back to the offline scorer instead of failing."""
    import answer_evaluator

    class BrokenModel:
        def generate_content(self, prompt):
            raise RuntimeError("Gemini down")

    monkeypatch.setattr(answer_evaluator, "model", BrokenModel())
    monkeypatch.setattr(main, "evaluate_answer", answer_evaluator.evaluate_answer)
    r = client.post("/evaluate", json={"question": "Q?", "answer": "short"})
    assert r.status_code == 200
    assert "Score: 4/10" in r.json()["feedback"]
