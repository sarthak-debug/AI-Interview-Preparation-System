"""End-to-end UI tests with Playwright.

The React app must be running (cd frontend && npm run dev -> http://localhost:5173).
Backend calls are intercepted with page.route(), so no backend or Gemini key is needed
and results are deterministic.

Run:  pytest -m e2e tests/e2e            (add --headed to watch the browser)
"""
import json
import os

import pytest
from playwright.sync_api import Page, expect

from qa_helpers import make_pdf

pytestmark = pytest.mark.e2e

APP_URL = os.getenv("APP_URL", "http://localhost:5173")
API = "http://127.0.0.1:8000"

UPLOAD_OK = {
    "filename": "resume.pdf",
    "skills": ["python", "sql"],
    "stored_questions": ["What is a decorator in Python?", "What is a JOIN?"],
    "ai_questions": "1. Explain FastAPI dependency injection.\n2. How would you test an LLM?",
    "is_ai_fallback": False,
}
FEEDBACK = "Score: 7/10\n\nStrengths:\n- Correct definition\n\nImprovements:\n- Add an example"


@pytest.fixture
def resume_file(tmp_path):
    p = tmp_path / "resume.pdf"
    p.write_bytes(make_pdf("Python and SQL developer"))
    return p


def mock_api(page: Page, upload=UPLOAD_OK, feedback=FEEDBACK, upload_status=200):
    def handle_upload(route):
        route.fulfill(status=upload_status, content_type="application/json", body=json.dumps(upload))

    def handle_evaluate(route):
        route.fulfill(status=200, content_type="application/json", body=json.dumps({"feedback": feedback}))

    page.route(f"{API}/upload", handle_upload)
    page.route(f"{API}/evaluate", handle_evaluate)


def upload_resume(page: Page, resume_file):
    page.goto(APP_URL)
    page.set_input_files("#resume-input", str(resume_file))
    page.get_by_role("button", name="Process & Generate Questions").click()


def test_full_happy_path(page: Page, resume_file):
    mock_api(page)
    upload_resume(page, resume_file)

    # Skills and question banks appear
    expect(page.get_by_text("PYTHON", exact=True)).to_be_visible()
    expect(page.get_by_role("button", name="Core Questions (2)")).to_be_visible()
    expect(page.get_by_role("button", name="AI Generated (2)")).to_be_visible()

    # Pick a question, answer it, get scored feedback
    page.get_by_text("What is a JOIN?").click()
    page.locator(".answer-textarea").fill("A JOIN combines rows from two tables using a related column.")
    page.get_by_role("button", name="Submit & Evaluate Answer").click()

    expect(page.locator(".score-radial")).to_have_text("7")
    expect(page.get_by_text("Correct definition")).to_be_visible()
    expect(page.get_by_text("Add an example")).to_be_visible()


def test_ai_questions_are_cleaned_of_numbering(page: Page, resume_file):
    mock_api(page)
    upload_resume(page, resume_file)
    page.get_by_role("button", name="AI Generated (2)").click()
    expect(page.get_by_text("Explain FastAPI dependency injection.", exact=True)).to_be_visible()


def test_fallback_warning_is_shown(page: Page, resume_file):
    mock_api(page, upload={**UPLOAD_OK, "is_ai_fallback": True})
    upload_resume(page, resume_file)
    page.get_by_role("button", name="AI Generated (2)").click()
    expect(page.get_by_text("AI API is currently unavailable", exact=False)).to_be_visible()


def test_submit_disabled_until_answer_typed(page: Page, resume_file):
    mock_api(page)
    upload_resume(page, resume_file)
    page.get_by_text("What is a JOIN?").click()
    submit = page.get_by_role("button", name="Submit & Evaluate Answer")
    expect(submit).to_be_disabled()
    page.locator(".answer-textarea").fill("Some answer")
    expect(submit).to_be_enabled()


def test_backend_down_shows_error_alert(page: Page, resume_file):
    mock_api(page, upload={"detail": "server error"}, upload_status=500)
    messages = []
    page.on("dialog", lambda d: (messages.append(d.message), d.dismiss()))
    upload_resume(page, resume_file)
    expect(page.get_by_role("button", name="Process & Generate Questions")).to_be_enabled()
    assert any("Upload Failed" in m for m in messages)


def test_unstructured_feedback_falls_back_to_raw_text(page: Page, resume_file):
    mock_api(page, feedback="The model replied without the expected format.")
    upload_resume(page, resume_file)
    page.get_by_text("What is a JOIN?").click()
    page.locator(".answer-textarea").fill("answer")
    page.get_by_role("button", name="Submit & Evaluate Answer").click()
    expect(page.get_by_text("The model replied without the expected format.")).to_be_visible()
