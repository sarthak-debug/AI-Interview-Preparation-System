"""Unit tests for resume_parser.extract_text (PDF -> text)."""
from qa_helpers import make_pdf
from resume_parser import extract_text


def test_extracts_text_from_pdf(tmp_path):
    pdf = tmp_path / "cv.pdf"
    pdf.write_bytes(make_pdf("Python Developer\nSkills: SQL, Git"))
    text = extract_text(str(pdf))
    assert "Python Developer" in text
    assert "SQL" in text
