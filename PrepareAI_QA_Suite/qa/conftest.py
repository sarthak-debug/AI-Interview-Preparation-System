"""Shared pytest setup: make the backend importable and provide common fixtures."""
import os
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))


from qa_helpers import make_pdf  # noqa: E402


@pytest.fixture
def sample_resume_pdf() -> bytes:
    return make_pdf(
        "Sarthak Gharat\n"
        "Skills: Python, React, SQL, Git\n"
        "Projects: built REST APIs with FastAPI"
    )


@pytest.fixture
def client(tmp_path, monkeypatch):
    """FastAPI TestClient running in a temp folder so uploads don't touch the real repo."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "uploads").mkdir()
    from fastapi.testclient import TestClient
    import main

    return TestClient(main.app, raise_server_exceptions=False)


@pytest.fixture
def gemini_key_present():
    return bool(os.getenv("GEMINI_API_KEY", "").strip())
