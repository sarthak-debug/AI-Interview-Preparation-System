# Bugs found by the QA suite

Each bug has a test marked `xfail(strict=True)`. When you fix the bug, that test starts passing,
pytest reports it as **XPASS (strict) → failure**, and you remove the `xfail` marker. This way a fixed
bug can never silently come back.

| ID | Severity | Area | Bug | Test |
|---|---|---|---|---|
| BUG-01 | Medium | Skill extraction | `ai` is matched inside other words (`email`, `maintain`), so almost every resume gets an "AI" skill | `tests/unit/test_skill_extraction.py::test_ai_not_detected_inside_other_words` |
| BUG-02 | Medium | Skill extraction | `java` is detected when the resume only mentions `JavaScript` | `test_java_not_detected_from_javascript` |
| BUG-03 | Low | Skill extraction | `express` matches the English word `expressed` | `test_express_not_detected_from_plain_english` |
| BUG-04 | Medium | `POST /upload` | Uploading a non-PDF file crashes the server with **500** instead of returning a clear 4xx error | `tests/api/test_upload_api.py::test_non_pdf_upload_returns_client_error` |
| BUG-05 | **High (security)** | `POST /upload` | Path traversal: a filename like `../escaped.pdf` is written **outside** the `uploads/` folder | `test_filename_path_traversal_is_blocked` |

## Suggested fixes

**BUG-01/02/03** – match whole words with a regex instead of `in`:

```python
import re
def extract_skills(text):
    text = text.lower()
    return sorted({s for s in SKILLS if re.search(rf"(?<![\w+]){re.escape(s)}(?![\w+])", text)})
```

**BUG-04** – catch PDF parsing errors and return 400:

```python
from fastapi import HTTPException
from pypdf.errors import PdfReadError
try:
    text = extract_text(file_path)
except PdfReadError:
    raise HTTPException(status_code=400, detail="Please upload a valid PDF file")
```

**BUG-05** – never trust the client filename:

```python
import uuid
file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.pdf")
```
