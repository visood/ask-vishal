"""PDF generation for the marketing plan.

Uses fpdf2 (pure Python, no system dependencies) to produce
a professional A4 document from the marketing plan content.
"""
import re
from io import BytesIO
from fpdf import FPDF

from marketing_plan import get_plan


def _sanitize(text: str) -> str:
    """Replace Unicode chars with Latin-1 safe equivalents for PDF."""
    replacements = {
        "\u2014": "--",   # em-dash
        "\u2013": "-",    # en-dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u00ab": '"',    # left guillemet
        "\u00bb": '"',    # right guillemet
        "\u2022": "-",    # bullet
    }
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    # Strip any remaining non-latin-1 chars
    return text.encode("latin-1", errors="replace").decode("latin-1")


class MarketingPlanPDF(FPDF):
    """Custom PDF with header and footer."""

    def __init__(self, plan: dict):
        super().__init__()
        self.plan = plan
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, _sanitize(f"{self.plan['subtitle']}  |  {self.plan['date']}"), align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, _sanitize(f"le comptoir -- Page {self.page_no()}/{{nb}}"), align="C")


def _render_body(pdf: MarketingPlanPDF, body: str):
    """Render markdown-like body text into PDF cells."""
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            pdf.ln(3)
            i += 1
            continue

        # Bold header: **text**
        bold_match = re.match(r'^\*\*(.+?)\*\*\s*$', stripped)
        if bold_match:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 6, _sanitize(bold_match.group(1)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            i += 1
            continue

        # Bullet point: - text (may contain **bold** inline)
        if stripped.startswith("- "):
            bullet_text = stripped[2:]
            # Strip inline bold markers for PDF
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'\1', bullet_text)
            bullet_text = re.sub(r'\*(.+?)\*', r'\1', bullet_text)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.cell(8, 5, "-", new_x="END")
            pdf.multi_cell(0, 5, _sanitize(bullet_text), new_x="LMARGIN", new_y="NEXT")
            i += 1
            continue

        # Regular paragraph — may span multiple lines until blank line
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("- ") and not re.match(r'^\*\*(.+?)\*\*\s*$', lines[i].strip()):
            para_text = lines[i].strip()
            # Strip markdown formatting
            para_text = re.sub(r'\*\*(.+?)\*\*', r'\1', para_text)
            para_text = re.sub(r'\*(.+?)\*', r'\1', para_text)
            para_lines.append(para_text)
            i += 1

        if para_lines:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5, _sanitize(" ".join(para_lines)), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue

        i += 1


def generate_marketing_plan_pdf(lang: str = "en") -> bytes:
    """Generate a PDF of the marketing plan in the given language.

    Returns PDF content as bytes.
    """
    plan = get_plan(lang)

    pdf = MarketingPlanPDF(plan)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(74, 111, 165)  # matches theme primaryColor
    pdf.cell(0, 12, _sanitize(plan["title"]), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Subtitle
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, _sanitize(plan["subtitle"]), new_x="LMARGIN", new_y="NEXT")

    # Date
    pdf.set_font("Helvetica", "I", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, _sanitize(plan["date"]), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    # Sections
    for section in plan["sections"]:
        # Section heading
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(74, 111, 165)
        pdf.cell(0, 10, _sanitize(section["heading"]), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Section body
        _render_body(pdf, section["body"])
        pdf.ln(4)

    # Output
    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()
