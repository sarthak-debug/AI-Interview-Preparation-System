import os

import pytest


def pytest_collection_modifyitems(config, items):
    if not os.getenv("GEMINI_API_KEY", "").strip():
        skip = pytest.mark.skip(reason="GEMINI_API_KEY not set - LLM evals need the real model")
        for item in items:
            if "llm" in item.keywords:
                item.add_marker(skip)
