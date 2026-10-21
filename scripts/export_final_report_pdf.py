from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "relatorio-final.md"
OUTPUT = ROOT / "output" / "pdf" / "relatorio-final-servidorbr.pdf"
FONT_DIR = Path("C:/Windows/Fonts")

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#168C86")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#607482")
PALE = colors.HexColor("#E8F3F2")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "ariali.ttf")))
    pdfmetrics.registerFontFamily(
        "Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold"
    )


def normalize_typography(value: str) -> str:
    return (
        value.replace("\u2011", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2022", "-")
    )


def inline_markup(value: str) -> str:
    value = normalize_typography(value)
    tokens: list[str] = []

    def hold(markup: str) -> str:
        tokens.append(markup)
        return f"\x00{len(tokens) - 1}\x00"

    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: hold(
            f'<link href="{html.escape(match.group(2), quote=True)}" color="#168C86" '
            f'underline="1">{html.escape(match.group(1))}</link>'
        ),
        value,
    )
    value = re.sub(
        r"`([^`]+)`",
        lambda match: hold(
            f'<font name="Courier" color="#34515F">{html.escape(match.group(1))}</font>'
        ),
        value,
    )
    value = re.sub(
        r"\*\*(.+?)\*\*",
        lambda match: hold(f"<b>{html.escape(match.group(1))}</b>"),
        value,
    )
    value = html.escape(value)
    for index, markup in enumerate(tokens):
        value = value.replace(f"\x00{index}\x00", markup)
    return value


def page_chrome(canvas, document) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#D7E2E8"))
    canvas.setLineWidth(0.55)
    canvas.line(document.leftMargin, height - 17 * mm, width - document.rightMargin, height - 17 * mm)
    canvas.setFont("Arial-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(document.leftMargin, height - 13 * mm, "SERVIDORBR")
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - document.rightMargin, height - 13 * mm, "RELATÓRIO FINAL")
    canvas.line(document.leftMargin, 15 * mm, width - document.rightMargin, 15 * mm)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(document.leftMargin, 10 * mm, "Projeto de consulta a dados públicos de servidores")
    canvas.drawRightString(width - document.rightMargin, 10 * mm, f"Página {document.page}")
    canvas.restoreState()


def build_pdf() -> None:
    register_fonts()
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "ReportTitle", fontName="Arial-Bold", fontSize=23, leading=28,
            textColor=NAVY, spaceAfter=7 * mm, alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            "Section", fontName="Arial-Bold", fontSize=14, leading=18,
            textColor=NAVY, spaceBefore=5 * mm, spaceAfter=2.2 * mm,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "Subsection", fontName="Arial-Bold", fontSize=10.5, leading=14,
            textColor=TEAL, spaceBefore=3 * mm, spaceAfter=1.5 * mm,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "BodyReport", fontName="Arial", fontSize=9.2, leading=13.2,
            textColor=INK, alignment=TA_LEFT, spaceAfter=2.2 * mm,
            splitLongWords=1,
        )
    )
    styles.add(
        ParagraphStyle(
            "BulletReport", parent=styles["BodyReport"], leftIndent=5 * mm,
            firstLineIndent=-3.2 * mm, bulletIndent=0, spaceAfter=1.8 * mm,
        )
    )
    styles.add(
        ParagraphStyle(
            "Metadata", fontName="Arial", fontSize=9.2, leading=13,
            textColor=MUTED, spaceAfter=1.5 * mm,
        )
    )

    output_dir = OUTPUT.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        rightMargin=19 * mm, leftMargin=19 * mm,
        topMargin=24 * mm, bottomMargin=22 * mm,
        title="Relatorio final - ServidorBR",
        author="Projeto ServidorBR",
        subject="Entrega tecnica, evidencias, validacao e limitacoes",
    )

    story = []
    paragraph_lines: list[str] = []
    title_written = False

    def flush_paragraph() -> None:
        if paragraph_lines:
            content = " ".join(line.strip() for line in paragraph_lines)
            story.append(Paragraph(inline_markup(content), styles["BodyReport"]))
            paragraph_lines.clear()

    for source_line in SOURCE.read_text(encoding="utf-8").splitlines():
        line = source_line.strip()
        if not line:
            flush_paragraph()
            continue
        if line.startswith("# "):
            flush_paragraph()
            if not title_written:
                story.append(Spacer(1, 3 * mm))
                story.append(Paragraph(inline_markup(line[2:]), styles["ReportTitle"]))
                story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=5 * mm))
                title_written = True
            else:
                story.append(Paragraph(inline_markup(line[2:]), styles["Section"]))
            continue
        if line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[3:]), styles["Section"]))
            continue
        if line.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[4:]), styles["Subsection"]))
            continue
        if line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph("&#8226; " + inline_markup(line[2:]), styles["BulletReport"]))
            continue
        if re.match(r"^\d+\.\s", line):
            flush_paragraph()
            number, content = line.split(". ", 1)
            story.append(Paragraph(f"<b>{number}.</b> {inline_markup(content)}", styles["BulletReport"]))
            continue
        paragraph_lines.append(line)

    flush_paragraph()
    document.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    print(f"PDF criado: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
