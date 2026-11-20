"""
core/sample_generator.py
Utility script to generate sample test PDFs, including the official 'Trap Document'
with intentional fake stats, outdated numbers, and verifiable facts for testing.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_trap_pdf(output_path: str):
    """Generates the official Trap Document PDF for testing the fact-checking agent."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Market Intelligence & Technology Trends 2024", title_style))
    story.append(Paragraph("<b>Author:</b> Global Strategy Research &middot; <b>Status:</b> Confidential Draft", body_style))
    story.append(Spacer(1, 10))

    # Section 1: Executive Overview (Mix of Fluff and Outdated Metrics)
    story.append(Paragraph("1. Executive Vision & Growth Dynamics", h2_style))
    story.append(Paragraph(
        "Our digital ecosystem delivers unprecedented paradigm-shifting synergy to hyper-growth enterprises. "
        "We believe our team has the most extraordinary passion for driving world-class innovation and customer success.",
        body_style
    ))
    story.append(Paragraph(
        "OpenAI ChatGPT reached 100 million active users in March 2021, marking the fastest consumer product adoption in history.",
        body_style
    ))

    # Section 2: Macroeconomics & Global Markets
    story.append(Paragraph("2. Macroeconomic Indicators", h2_style))
    story.append(Paragraph(
        "In global economic evaluations, India's nominal GDP stands at approximately $1.8 Trillion.",
        body_style
    ))
    story.append(Paragraph(
        "The Apollo 11 mission landed astronauts on the Moon on July 20, 1969.",
        body_style
    ))

    # Section 3: Tech Giants & Hardware Evolution
    story.append(Paragraph("3. Technology Giants and Silicon Milestones", h2_style))
    story.append(Paragraph(
        "Tesla Inc. was founded in 2008 by Elon Musk in San Carlos, California.",
        body_style
    ))
    story.append(Paragraph(
        "Google was founded in 1975 by Bill Gates in Seattle, Washington.",
        body_style
    ))
    story.append(Paragraph(
        "The iPhone 16 features 4GB of RAM and was announced in September 2020.",
        body_style
    ))
    story.append(Paragraph(
        "Python was conceived in the late 1980s by Guido van Rossum and first released in 1991.",
        body_style
    ))

    # Section 4: Agency Benchmark (CogCulture)
    story.append(Paragraph("4. Agency Benchmarking", h2_style))
    story.append(Paragraph(
        "In creative agency landscape reviews, CogCulture has 500,000 employees worldwide across 40 countries.",
        body_style
    ))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_data")
    target_path = os.path.join(sample_dir, "trap_marketing_document.pdf")
    generate_trap_pdf(target_path)
    print(f"Generated trap document at: {target_path}")
