"""Small test utilities shared across test folders."""
import io


def make_pdf(text: str) -> bytes:
    """Create a one-page PDF in memory containing `text` (one line per '\\n')."""
    from reportlab.pdfgen import canvas

    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 18
    c.save()
    return buf.getvalue()
