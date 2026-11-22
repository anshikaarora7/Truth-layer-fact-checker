"""
make_ppt.py
Generates a professional executive PowerPoint-style PDF presentation
for Truth Layer Enterprise using ReportLab.
Run: python make_ppt.py
Output: truth_layer_presentation.pdf
"""

import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics

W, H = landscape(A4)   # 841.9 x 595.3 points

# ── Color Palette ────────────────────────────────────────────────
BG_DARK    = colors.HexColor("#0A0E1A")
BG_CARD    = colors.HexColor("#131B2E")
INDIGO     = colors.HexColor("#6366F1")
INDIGO_LT  = colors.HexColor("#A5B4FC")
SLATE      = colors.HexColor("#94A3B8")
WHITE      = colors.white
GREEN      = colors.HexColor("#10B981")
AMBER      = colors.HexColor("#F59E0B")
RED        = colors.HexColor("#EF4444")
TEAL       = colors.HexColor("#06B6D4")
PURPLE     = colors.HexColor("#A855F7")
SLATE_DARK = colors.HexColor("#1E293B")

# ── Styles ───────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

HERO  = S("Hero",  fontName="Helvetica-Bold",   fontSize=34, textColor=WHITE,     leading=40, spaceAfter=6)
TITLE = S("Title", fontName="Helvetica-Bold",   fontSize=22, textColor=WHITE,     leading=28, spaceAfter=4)
BODY  = S("Body",  fontName="Helvetica",        fontSize=11, textColor=colors.HexColor("#CBD5E1"), leading=18, spaceAfter=4)
PILL  = S("Pill",  fontName="Helvetica-Bold",   fontSize=9,  textColor=INDIGO_LT, leading=14)
KPI_N = S("KPIN",  fontName="Helvetica-Bold",   fontSize=28, textColor=WHITE,     leading=32, alignment=1)
KPI_L = S("KPIL",  fontName="Helvetica",        fontSize=8,  textColor=SLATE,     leading=12, alignment=1, spaceAfter=2)
KPI_S = S("KPIS",  fontName="Helvetica",        fontSize=7,  textColor=SLATE,     leading=10, alignment=1)
H2    = S("H2",    fontName="Helvetica-Bold",   fontSize=14, textColor=INDIGO_LT, leading=20, spaceAfter=4)
SMALL = S("Small", fontName="Helvetica",        fontSize=8,  textColor=SLATE,     leading=12)
TAG   = S("Tag",   fontName="Helvetica-Bold",   fontSize=8,  textColor=WHITE,     leading=12, alignment=1)
QUOTE = S("Quote", fontName="Helvetica-Oblique",fontSize=12, textColor=INDIGO_LT, leading=18, spaceAfter=6, leftIndent=16, rightIndent=16)
FOOTER_S = S("Footer", fontName="Helvetica", fontSize=7, textColor=SLATE, alignment=1)


# ── Helper: dark full-page background ────────────────────────────
def dark_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Subtle accent bar on left
    canvas.setFillColor(INDIGO)
    canvas.rect(0, 0, 4, H, fill=1, stroke=0)
    # Footer line
    canvas.setStrokeColor(SLATE_DARK)
    canvas.setLineWidth(0.5)
    canvas.line(30, 22, W - 30, 22)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(SLATE)
    canvas.drawCentredString(W / 2, 10, "Truth Layer Enterprise  ·  Engineered by Anshika Arora  ·  Confidential")
    canvas.restoreState()


def card_bg(canvas, x, y, w, h, border_color=None):
    """Draw a dark glass card rectangle."""
    canvas.saveState()
    canvas.setFillColor(BG_CARD)
    canvas.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    if border_color:
        canvas.setStrokeColor(border_color)
        canvas.setLineWidth(1.5)
    else:
        canvas.setStrokeColor(colors.HexColor("#1E293B"))
        canvas.setLineWidth(0.8)
    canvas.roundRect(x, y, w, h, 10, fill=0, stroke=1)
    canvas.restoreState()


# ── Slide builder ─────────────────────────────────────────────────
slides = []          # list of (draw_fn, story_items)

# ================================================================
# SLIDE 1 — Cover
# ================================================================
def slide1(canvas, doc):
    dark_bg(canvas, doc)
    # Giant shield gradient effect
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#1E1B4B"))
    canvas.circle(W * 0.72, H * 0.5, 200, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#312E81"))
    canvas.circle(W * 0.72, H * 0.5, 140, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.circle(W * 0.72, H * 0.5, 90, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 60)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(W * 0.72, H * 0.5 - 22, "🛡")

    # Tag pill
    pill_w, pill_h = 220, 24
    canvas.setFillColor(colors.HexColor("#1E1B4B"))
    canvas.roundRect(30, H - 60, pill_w, pill_h, 12, fill=1, stroke=0)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1)
    canvas.roundRect(30, H - 60, pill_w, pill_h, 12, fill=0, stroke=1)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(42, H - 50, "AI-POWERED · ENTERPRISE · PRE-PUBLICATION GATEKEEPER")

    # Main title
    canvas.setFont("Helvetica-Bold", 42)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H * 0.62, "Truth Layer")
    canvas.setFont("Helvetica-Bold", 42)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H * 0.62 - 48, "Enterprise")

    canvas.setFont("Helvetica", 14)
    canvas.setFillColor(SLATE)
    canvas.drawString(30, H * 0.62 - 80, "Automated Fact-Checking & Document Risk Gatekeeper")

    # Divider
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(2)
    canvas.line(30, H * 0.62 - 92, 280, H * 0.62 - 92)

    # Author info
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H * 0.62 - 114, "Anshika Arora")
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(SLATE)
    canvas.drawString(30, H * 0.62 - 130, "CogCulture Assessment · Part 2 · 2024")

    # Capability pills
    pills = [
        ("⚡", "Sub-5s Audit"),
        ("🌐", "Live Web Grounding"),
        ("📝", "Track-Changes Redline"),
        ("🔒", "SHA-256 Certificate"),
    ]
    px = 30
    py = 44
    for icon, text in pills:
        pw = 150
        canvas.setFillColor(colors.HexColor("#1E293B"))
        canvas.roundRect(px, py, pw, 22, 11, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#334155"))
        canvas.setLineWidth(0.8)
        canvas.roundRect(px, py, pw, 22, 11, fill=0, stroke=1)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(INDIGO_LT)
        canvas.drawString(px + 8, py + 7, f"{icon}  {text}")
        px += 158

    canvas.restoreState()

slides.append(slide1)

# ================================================================
# SLIDE 2 — The Problem & Business Cost
# ================================================================
def slide2(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    # Section label
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "01  ·  THE PROBLEM")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    # Headline
    canvas.setFont("Helvetica-Bold", 28)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 92, "Corporate Documents Routinely Contain")
    canvas.setFont("Helvetica-Bold", 28)
    canvas.setFillColor(RED)
    canvas.drawString(30, H - 122, "Outdated Stats, Hallucinations & Inflated Metrics")

    canvas.setFont("Helvetica", 12)
    canvas.setFillColor(SLATE)
    canvas.drawString(30, H - 150, "Relying on unverified PDFs exposes organizations to legal risk, deal failures, and reputational damage.")

    # 3 Pain Point Cards
    cards = [
        ("⚖️", "Regulatory Fines", RED, "Unsubstantiated market claims trigger FTC/SEC investigations and enforcement actions."),
        ("💸", "Deal Failure", AMBER, "Inflated TAM or fabricated traction metrics destroy investor trust during due diligence."),
        ("📰", "Brand Damage", PURPLE, "Public retractions and corrections erode media credibility permanently."),
    ]
    cx = 30
    for icon, title, col, desc in cards:
        cw = (W - 70) / 3 - 6
        ch = 160
        cy = 36

        canvas.setFillColor(BG_CARD)
        canvas.roundRect(cx, cy, cw, ch, 10, fill=1, stroke=0)
        canvas.setStrokeColor(col)
        canvas.setLineWidth(1.5)
        canvas.line(cx, cy + ch, cx + cw, cy + ch)
        canvas.roundRect(cx, cy, cw, ch, 10, fill=0, stroke=0)

        # Top colored line accent
        canvas.setFillColor(col)
        canvas.roundRect(cx, cy + ch - 4, cw, 4, 2, fill=1, stroke=0)

        canvas.setFont("Helvetica-Bold", 20)
        canvas.setFillColor(WHITE)
        canvas.drawString(cx + 14, cy + ch - 36, icon)
        canvas.setFont("Helvetica-Bold", 13)
        canvas.setFillColor(col)
        canvas.drawString(cx + 14, cy + ch - 56, title)
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#94A3B8"))

        # Word-wrap manually
        words = desc.split()
        line, lines = [], []
        for w_txt in words:
            line.append(w_txt)
            if len(" ".join(line)) > 36:
                lines.append(" ".join(line[:-1]))
                line = [w_txt]
        lines.append(" ".join(line))
        for i, l in enumerate(lines[:5]):
            canvas.drawString(cx + 14, cy + ch - 80 - i * 14, l)

        cx += cw + 10

    canvas.restoreState()

slides.append(slide2)

# ================================================================
# SLIDE 3 — Solution Overview & Pipeline
# ================================================================
def slide3(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "02  ·  THE SOLUTION")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    canvas.setFont("Helvetica-Bold", 26)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 90, "A 3-Stage AI Verification Pipeline")

    stages = [
        ("01", "EXTRACT", GREEN,
         "PDF Text Stream\npypdf parses\npage-by-page\nfilters buzzwords\nisolates metrics",),
        ("02", "VERIFY", INDIGO,
         "Live Web Grounding\nGoogle Gemini 2.0\n+ Wikipedia\n+ DuckDuckGo\nkeyless fallback",),
        ("03", "CLASSIFY", AMBER,
         "3-Tier Verdict\n✅ Verified\n⚠️ Inaccurate\n❌ False\n+ Real Fact Fix",),
        ("04", "REPORT", RED,
         "Executive Output\nPDF Certificate\nTrack-Changes\nAltair Charts\nJSON / CSV / MD",),
    ]

    sx = 30
    for num, title, col, desc_raw in stages:
        sw = (W - 60) / 4 - 6
        sh = 300
        sy = 42

        # Card
        canvas.setFillColor(BG_CARD)
        canvas.roundRect(sx, sy, sw, sh, 10, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor("#1E293B"))
        canvas.setLineWidth(0.5)
        canvas.roundRect(sx, sy, sw, sh, 10, fill=0, stroke=1)

        # Number badge
        canvas.setFillColor(col)
        canvas.circle(sx + sw / 2, sy + sh - 32, 20, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(WHITE)
        canvas.drawCentredString(sx + sw / 2, sy + sh - 37, num)

        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(col)
        canvas.drawCentredString(sx + sw / 2, sy + sh - 68, title)

        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#CBD5E1"))
        for i, line in enumerate(desc_raw.split("\n")):
            canvas.drawCentredString(sx + sw / 2, sy + sh - 94 - i * 16, line)

        # Arrow between cards
        if sx + sw + 10 < W - 30:
            ax = sx + sw + 5
            ay = sy + sh / 2
            canvas.setStrokeColor(INDIGO)
            canvas.setLineWidth(1.5)
            canvas.line(ax - 2, ay, ax + 4, ay)
            # Arrow head (manual polygon)
            canvas.setFillColor(INDIGO)
            from reportlab.graphics.shapes import Polygon
            p = canvas.beginPath()
            p.moveTo(ax + 4, ay + 5)
            p.lineTo(ax + 4, ay - 5)
            p.lineTo(ax + 12, ay)
            p.close()
            canvas.drawPath(p, fill=1, stroke=0)

        sx += sw + 10

    canvas.restoreState()

slides.append(slide3)

# ================================================================
# SLIDE 4 — Key Features
# ================================================================
def slide4(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "03  ·  KEY FEATURES THAT IMPRESS")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    canvas.setFont("Helvetica-Bold", 24)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 86, "5 Differentiating Features")

    features = [
        (INDIGO, "📝  Document Redline (Track Changes)",
         "Renders live Word-style strikethrough on false claims with verified corrections injected beside them. Exactly what Legal & Compliance teams need."),
        (GREEN,  "📄  Executive PDF Compliance Certificate",
         "One-click downloadable PDF with formal Clearance Decision (PASSED / CONDITIONAL / REJECTED), SHA-256 integrity checksum, and legal sign-off block."),
        (AMBER,  "📊  Altair Analytics Charts",
         "Visual Donut chart of Verified/Inaccurate/False ratio and Category bar chart — no spreadsheet needed."),
        (TEAL,   "🧪  3 One-Click Industry Presets",
         "Reviewers can test without uploading a file: Trap Document, Series B Pitch Deck, and Corporate ESG Audit — all pre-loaded."),
        (PURPLE, "💡  Zero-Cost Keyless Fallback Mode",
         "If Gemini API credits run out, the app auto-switches to Wikipedia + DuckDuckGo. Demo never breaks."),
    ]

    fy = H - 110
    for col, title, desc in features:
        canvas.setFillColor(BG_CARD)
        canvas.roundRect(30, fy - 52, W - 60, 56, 8, fill=1, stroke=0)
        canvas.setFillColor(col)
        canvas.roundRect(30, fy - 52, 4, 56, 2, fill=1, stroke=0)

        canvas.setFont("Helvetica-Bold", 11)
        canvas.setFillColor(WHITE)
        canvas.drawString(44, fy - 18, title)
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(SLATE)
        canvas.drawString(44, fy - 34, desc[:100] + ("..." if len(desc) > 100 else ""))

        fy -= 64

    canvas.restoreState()

slides.append(slide4)

# ================================================================
# SLIDE 5 — Business Value / ROI
# ================================================================
def slide5(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "04  ·  BUSINESS VALUE & ROI")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    canvas.setFont("Helvetica-Bold", 26)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 86, "Quantifiable Impact vs. Manual Compliance Review")

    # Comparison Table
    headers = ["Metric", "Manual Review", "Truth Layer Enterprise"]
    rows = [
        ["Audit Turnaround", "3.5 – 5.0 hours / document", "< 5 seconds / document"],
        ["Verification Cost", "$250 – $375 per document", "< $0.005 per document"],
        ["Consistency", "Reviewer fatigue / bias", "Deterministic AI consensus"],
        ["Auditability", "Sticky-note annotations", "SHA-256 PDF Certificate"],
        ["Scalability", "1 analyst → 1 document", "1 agent → unlimited documents"],
    ]

    col_widths = [170, 230, 240]
    tx = 30
    ty = H - 108

    for ci, (header, cw) in enumerate(zip(headers, col_widths)):
        canvas.setFillColor(INDIGO if ci == 2 else SLATE_DARK)
        canvas.rect(tx, ty - 22, cw - 4, 24, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(WHITE)
        canvas.drawString(tx + 8, ty - 12, header)
        tx += cw

    for ri, row in enumerate(rows):
        ty -= 28
        tx = 30
        alt_bg = colors.HexColor("#131B2E") if ri % 2 == 0 else colors.HexColor("#0E1420")
        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            canvas.setFillColor(alt_bg)
            canvas.rect(tx, ty - 20, cw - 4, 24, fill=1, stroke=0)
            if ci == 2:
                canvas.setFont("Helvetica-Bold", 9)
                canvas.setFillColor(GREEN)
            else:
                canvas.setFont("Helvetica", 9)
                canvas.setFillColor(colors.HexColor("#CBD5E1") if ci > 0 else SLATE)
            canvas.drawString(tx + 8, ty - 10, cell)
            tx += cw

    # ROI Callout
    ty -= 48
    canvas.setFillColor(colors.HexColor("#1E1B4B"))
    canvas.roundRect(30, ty - 28, W - 60, 32, 8, fill=1, stroke=0)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1)
    canvas.roundRect(30, ty - 28, W - 60, 32, 8, fill=0, stroke=1)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawCentredString(W / 2, ty - 10,
        "⚡  For a 10-claim document → saves 2.5 hours (~$188) of compliance labor per review cycle")

    canvas.restoreState()

slides.append(slide5)

# ================================================================
# SLIDE 6 — Architecture / Tech Stack
# ================================================================
def slide6(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "05  ·  ARCHITECTURE & TECH STACK")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    canvas.setFont("Helvetica-Bold", 26)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 86, "Production-Grade Modular Design")

    # Left: Architecture flow
    layers = [
        (WHITE,      "📄  Presentation Layer",    "Streamlit · Altair Charts · ReportLab PDF"),
        (INDIGO_LT,  "🧠  Intelligence Layer",    "Google Gemini 2.0 Flash · Search Grounding API"),
        (GREEN,      "🔍  Search Engine Layer",   "DuckDuckGo · Wikipedia Open Knowledge · Tavily"),
        (AMBER,      "📦  Data Model Layer",      "Pydantic v2 Schemas · Type-Safe Validation"),
        (TEAL,       "📂  Extraction Layer",       "pypdf · NLP Claim Classifier · Fluff Filter"),
    ]

    ly = H - 112
    for col, title, tech in layers:
        canvas.setFillColor(BG_CARD)
        canvas.roundRect(30, ly - 36, 390, 40, 6, fill=1, stroke=0)
        canvas.setFillColor(col)
        canvas.roundRect(30, ly - 36, 4, 40, 2, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.setFillColor(col)
        canvas.drawString(44, ly - 10, title)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawString(44, ly - 24, tech)
        ly -= 48

    # Right: Tech badges grid
    techs = [
        ("Streamlit", "1.67", INDIGO),
        ("Google GenAI", "1.0", GREEN),
        ("pypdf", "5.x", AMBER),
        ("Pydantic", "2.x", TEAL),
        ("Altair", "6.x", PURPLE),
        ("ReportLab", "5.x", RED),
        ("DuckDuckGo", "7.x", GREEN),
        ("Python", "3.10+", INDIGO_LT),
    ]
    bx, by = 450, H - 100
    for i, (name, ver, col) in enumerate(techs):
        bxi = bx + (i % 4) * 98
        byi = by - (i // 4) * 56
        canvas.setFillColor(BG_CARD)
        canvas.roundRect(bxi, byi - 36, 92, 40, 6, fill=1, stroke=0)
        canvas.setStrokeColor(col)
        canvas.setLineWidth(1)
        canvas.roundRect(bxi, byi - 36, 92, 40, 6, fill=0, stroke=1)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.setFillColor(col)
        canvas.drawCentredString(bxi + 46, byi - 14, name)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(SLATE)
        canvas.drawCentredString(bxi + 46, byi - 28, f"v{ver}")

    canvas.restoreState()

slides.append(slide6)

# ================================================================
# SLIDE 7 — Live Demo Evidence (Trap Document Results)
# ================================================================
def slide7(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 48, "06  ·  LIVE DEMO — BENCHMARK RESULTS")
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 52, W - 30, H - 52)

    canvas.setFont("Helvetica-Bold", 24)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 86, "Official Trap Document: Ground Truth Verdict Table")

    headers = ["Claim in Document", "Category", "Agent Verdict", "Real Fact / Correction"]
    col_widths = [230, 90, 120, 240]
    results = [
        ("ChatGPT reached 100M users in March 2021", "Date/Stat", ("⚠️ INACCURATE", AMBER), "Launched Nov 2022; 100M in Jan 2023"),
        ("India GDP ≈ $1.8 Trillion", "Financial", ("⚠️ INACCURATE", AMBER), "India GDP surpassed $3.9T in 2024"),
        ("Tesla founded in 2008 by Elon Musk", "History", ("⚠️ INACCURATE", AMBER), "Founded July 2003 by Eberhard & Tarpenning"),
        ("Google founded in 1975 by Bill Gates", "Fabrication", ("❌ FALSE", RED), "Founded 1998 by Larry Page & Sergey Brin"),
        ("iPhone 16: 4GB RAM, Sept 2020", "Tech Spec", ("⚠️ INACCURATE", AMBER), "Sept 2024, 8GB RAM for Apple Intelligence"),
        ("CogCulture has 500,000 employees", "Scale", ("❌ FALSE", RED), "Boutique agency ~50-200 members, Gurugram"),
        ("Apollo 11 landed on Moon, July 20 1969", "History", ("✅ VERIFIED", GREEN), "Historical consensus matches exactly"),
        ("Python first released in 1991 by Van Rossum", "Technical", ("✅ VERIFIED", GREEN), "Historical consensus matches exactly"),
        ("World-class paradigm-shifting synergy...", "Fluff", ("🚫 FILTERED", SLATE), "Subjective — no testable claim"),
    ]

    tx, ty = 30, H - 110

    # Header row
    for ci, (header, cw) in enumerate(zip(headers, col_widths)):
        fc = INDIGO if ci == 0 else BG_CARD
        canvas.setFillColor(fc)
        canvas.rect(tx, ty - 18, cw - 3, 20, fill=1, stroke=0)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(WHITE)
        canvas.drawString(tx + 4, ty - 11, header)
        tx += cw

    for ri, (claim, cat, (verdict, vcol), correction) in enumerate(results):
        ty -= 24
        tx = 30
        alt = colors.HexColor("#0E1420") if ri % 2 else BG_CARD
        for ci, (text, cw) in enumerate(zip([claim, cat, verdict, correction], col_widths)):
            canvas.setFillColor(alt)
            canvas.rect(tx, ty - 18, cw - 3, 22, fill=1, stroke=0)
            if ci == 2:
                canvas.setFont("Helvetica-Bold", 8)
                canvas.setFillColor(vcol)
            elif ci == 0:
                canvas.setFont("Helvetica-Oblique", 7.5)
                canvas.setFillColor(colors.HexColor("#E2E8F0"))
            elif ci == 3:
                canvas.setFont("Helvetica", 7.5)
                canvas.setFillColor(GREEN if vcol == GREEN else colors.HexColor("#CBD5E1"))
            else:
                canvas.setFont("Helvetica", 7.5)
                canvas.setFillColor(SLATE)
            canvas.drawString(tx + 4, ty - 10, str(text)[:42] + ("..." if len(str(text)) > 42 else ""))
            tx += cw

    canvas.restoreState()

slides.append(slide7)

# ================================================================
# SLIDE 8 — Thank You / CTA
# ================================================================
def slide8(canvas, doc):
    dark_bg(canvas, doc)
    canvas.saveState()

    # Center circle glow
    canvas.setFillColor(colors.HexColor("#1E1B4B"))
    canvas.circle(W / 2, H / 2 + 20, 180, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#312E81"))
    canvas.circle(W / 2, H / 2 + 20, 110, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.circle(W / 2, H / 2 + 20, 55, fill=1, stroke=0)

    canvas.setFont("Helvetica-Bold", 36)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(W / 2, H / 2 + 7, "🛡️")

    canvas.setFont("Helvetica-Bold", 30)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(W / 2, H / 2 - 60, "Truth Layer Enterprise")
    canvas.setFont("Helvetica", 13)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawCentredString(W / 2, H / 2 - 82, "AI-Powered · Production-Ready · 100% Verifiable")

    canvas.setFont("Helvetica-Bold", 11)
    canvas.setFillColor(SLATE)
    canvas.drawCentredString(W / 2, H / 2 - 110, "Engineered by  Anshika Arora  ·  anshikaarora7")

    # GitHub pill
    canvas.setFillColor(colors.HexColor("#1E293B"))
    canvas.roundRect(W / 2 - 160, H / 2 - 148, 320, 26, 13, fill=1, stroke=0)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1)
    canvas.roundRect(W / 2 - 160, H / 2 - 148, 320, 26, 13, fill=0, stroke=1)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawCentredString(W / 2, H / 2 - 131,
        "github.com/anshikaarora7/Truth-layer-fact-checker")

    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(WHITE)
    canvas.drawCentredString(W / 2, H - 52, "Thank You")

    canvas.restoreState()

slides.append(slide8)


# ── Build PDF ──────────────────────────────────────────────────────
class SlidePDF(BaseDocTemplate):
    def __init__(self, filename, slides_list):
        super().__init__(filename, pagesize=landscape(A4),
                         rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
        self.slides_list = slides_list
        self._slide_index = 0

        frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        template = PageTemplate(id="slide", frames=[frame], onPage=self._on_page)
        self.addPageTemplates(template)

    def _on_page(self, canvas, doc):
        idx = self._slide_index % len(self.slides_list)
        self.slides_list[idx](canvas, doc)
        self._slide_index += 1


out_path = os.path.join(os.path.dirname(__file__), "truth_layer_presentation.pdf")
pdf = SlidePDF(out_path, slides)

# One empty paragraph per slide to trigger page breaks
story = []
from reportlab.platypus import PageBreak
for i in range(len(slides)):
    story.append(Spacer(1, 1))
    if i < len(slides) - 1:
        story.append(PageBreak())

pdf.build(story)
print(f"\n✅  Presentation saved → {out_path}")
print(f"   Slides: {len(slides)}  |  Size: {os.path.getsize(out_path):,} bytes")
