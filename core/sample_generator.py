"""
core/sample_generator.py
Utility script to generate sample test PDFs across multiple enterprise domains,
including the official 'Trap Document' for testing the fact-checking agent.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def _get_base_styles():
    styles = getSampleStyleSheet()
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
    return title_style, h2_style, body_style


def generate_trap_pdf(output_path: str) -> str:
    """Generates the official Trap Document PDF for testing the fact-checking agent."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    title_style, h2_style, body_style = _get_base_styles()
    story = []

    # Title & Metadata
    story.append(Paragraph("Market Intelligence & Technology Trends 2024", title_style))
    story.append(Paragraph("<b>Author:</b> Global Strategy Research &middot; <b>Status:</b> Confidential Draft", body_style))
    story.append(Spacer(1, 10))

    # Section 1: Executive Overview
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


def generate_pitch_deck_pdf(output_path: str) -> str:
    """Generates an Investor Pitch Deck sample with inflated TAM, metrics, and dates."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    title_style, h2_style, body_style = _get_base_styles()
    story = []

    story.append(Paragraph("NovaSphere AI: Series B Investment Memorandum", title_style))
    story.append(Paragraph("<b>Confidential:</b> Prepared for Tier-1 Venture Capital Partners &middot; Q4 2024", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Market Opportunity & Total Addressable Market", h2_style))
    story.append(Paragraph(
        "We are building the definitive foundational intelligence layer for global commerce. "
        "According to leading analysts, the global artificial intelligence market reached $15 Trillion in annual revenue in 2023.",
        body_style
    ))

    story.append(Paragraph("2. Operational Traction & Growth Velocity", h2_style))
    story.append(Paragraph(
        "Our flagship generative workflow engine surpassed 50 million daily active users within 90 days of launch.",
        body_style
    ))
    story.append(Paragraph(
        "Microsoft acquired LinkedIn in December 2016 for $26.2 Billion, validating enterprise network valuations.",
        body_style
    ))

    story.append(Paragraph("3. Leadership & Historical Precedents", h2_style))
    story.append(Paragraph(
        "Amazon Web Services was launched in 2006, pioneering modern public cloud compute infrastructure.",
        body_style
    ))
    story.append(Paragraph(
        "Our advisory board includes industry veterans who previously led Apple Inc. when it was founded in 1995 by Mark Zuckerberg.",
        body_style
    ))

    doc.build(story)
    return output_path


def generate_esg_pdf(output_path: str) -> str:
    """Generates a Corporate Sustainability / ESG sample with environmental metrics."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    title_style, h2_style, body_style = _get_base_styles()
    story = []

    story.append(Paragraph("AeroTerra Global: Corporate Sustainability & Climate Audit 2024", title_style))
    story.append(Paragraph("<b>Scope:</b> ESG Compliance & Corporate Social Responsibility &middot; Annual Disclosure", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Carbon Footprint & Decarbonization Targets", h2_style))
    story.append(Paragraph(
        "We are passionately committed to sustainable planetary stewardship and holistic ecological harmony across all business units.",
        body_style
    ))
    story.append(Paragraph(
        "Our European manufacturing facilities achieved certified 100% net-zero greenhouse gas emissions in 2015.",
        body_style
    ))

    story.append(Paragraph("2. Global Climate Benchmarks", h2_style))
    story.append(Paragraph(
        "The Paris Agreement climate accord was legally adopted by 196 parties at COP21 on December 12, 2015.",
        body_style
    ))
    story.append(Paragraph(
        "Global average atmospheric carbon dioxide concentrations reached approximately 420 parts per million (ppm) in 2024.",
        body_style
    ))

    story.append(Paragraph("3. Renewable Transition & Scope 3 Verification", h2_style))
    story.append(Paragraph(
        "Over 95% of all global commercial airline flights operate entirely on zero-emission hydrogen fuel as of 2023.",
        body_style
    ))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "sample_data")
    generate_trap_pdf(os.path.join(sample_dir, "trap_marketing_document.pdf"))
    generate_pitch_deck_pdf(os.path.join(sample_dir, "series_b_pitch_deck.pdf"))
    generate_esg_pdf(os.path.join(sample_dir, "corporate_esg_audit.pdf"))
    print("Generated all 3 sample preset documents successfully.")
