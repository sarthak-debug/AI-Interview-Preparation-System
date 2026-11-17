"""API tests for POST /upload. Gemini is mocked so these run offline and free."""
import main

FALLBACK_FIRST_Q = "What are the key differences between SQL and NoSQL databases?"


def upload(client, pdf_bytes, filename="resume.pdf"):
    return client.post("/upload", files={"file": (filename, pdf_bytes, "application/pdf")})


def test_upload_returns_skills_and_questions(client, sample_resume_pdf, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(main, "generate_ai_questions", lambda text: "1. Q one?\n2. Q two?")

    r = upload(client, sample_resume_pdf)

    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"filename", "skills", "stored_questions", "ai_questions", "is_ai_fallback"}
    assert {"python", "react", "sql", "git"}.issubset(body["skills"])
    assert len(body["stored_questions"]) > 0
    assert body["ai_questions"] == "1. Q one?\n2. Q two?"
    assert body["is_ai_fallback"] is False


def test_missing_api_key_uses_fallback_questions(client, sample_resume_pdf, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = upload(client, sample_resume_pdf)
    assert r.status_code == 200
    assert r.json()["is_ai_fallback"] is True
    assert FALLBACK_FIRST_Q in r.json()["ai_questions"]


def test_gemini_error_uses_fallback_questions(client, sample_resume_pdf, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    def boom(text):
        raise RuntimeError("429 rate limited")

    monkeypatch.setattr(main, "generate_ai_questions", boom)
    r = upload(client, sample_resume_pdf)
    assert r.status_code == 200
    assert r.json()["is_ai_fallback"] is True


def test_empty_gemini_response_uses_fallback(client, sample_resume_pdf, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(main, "generate_ai_questions", lambda text: "   ")
    r = upload(client, sample_resume_pdf)
    assert r.json()["is_ai_fallback"] is True


def test_upload_without_file_is_rejected(client):
    r = client.post("/upload")
    assert r.status_code == 422


# ---- Bugs found by these tests ----

import pytest  # noqa: E402


@pytest.mark.xfail(strict=True, reason="BUG-04: non-PDF upload crashes with 500 instead of a clear 4xx error")
def test_non_pdf_upload_returns_client_error(client, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = upload(client, b"this is not a pdf", filename="notes.txt")
    assert 400 <= r.status_code < 500


@pytest.mark.xfail(strict=True, reason="BUG-05 (security): filename with '../' is written outside uploads/")
def test_filename_path_traversal_is_blocked(client, sample_resume_pdf, monkeypatch, tmp_path):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    upload(client, sample_resume_pdf, filename="../escaped.pdf")
    assert not (tmp_path / "escaped.pdf").exists()
