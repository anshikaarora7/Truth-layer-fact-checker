"""
make_geo_pdf.py
Generates a PDF presentation for CogCulture Part 1: GEO Product Strategy & Roadmap.
Author: Anshika Arora
"""

import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Spacer
from reportlab.lib.styles import ParagraphStyle

W, H = landscape(A4)

BG_DARK = colors.HexColor("#0A0E1A")
BG_CARD = colors.HexColor("#131B2E")
INDIGO = colors.HexColor("#6366F1")
INDIGO_LT = colors.HexColor("#A5B4FC")
SLATE = colors.HexColor("#94A3B8")
WHITE = colors.white
GREEN = colors.HexColor("#10B981")
AMBER = colors.HexColor("#F59E0B")
RED = colors.HexColor("#EF4444")
CYAN = colors.HexColor("#06B6D4")

def dark_bg(canvas, doc, slide_num, total_slides=10):
    canvas.saveState()
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(INDIGO)
    canvas.rect(0, 0, 4, H, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#1E293B"))
    canvas.setLineWidth(0.5)
    canvas.line(30, 22, W - 30, 22)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(SLATE)
    canvas.drawCentredString(W / 2, 10, f"CogCulture Part 1: GEO Product Strategy · Anshika Arora · Slide {slide_num} of {total_slides}")
    canvas.restoreState()

def draw_header(canvas, tag, title):
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.setFillColor(INDIGO_LT)
    canvas.drawString(30, H - 42, tag)
    canvas.setStrokeColor(INDIGO)
    canvas.setLineWidth(1.5)
    canvas.line(30, H - 46, W - 30, H - 46)
    canvas.setFont("Helvetica-Bold", 22)
    canvas.setFillColor(WHITE)
    canvas.drawString(30, H - 76, title)

def draw_card(canvas, x, y, w, h, title, desc, col=INDIGO, title_sz=12, desc_sz=8.5):
    canvas.setFillColor(BG_CARD)
    canvas.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    canvas.setFillColor(col)
    canvas.roundRect(x, y + h - 4, w, 4, 2, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", title_sz)
    canvas.setFillColor(col)
    canvas.drawString(x + 12, y + h - 26, title)
    canvas.setFont("Helvetica", desc_sz)
    canvas.setFillColor(colors.HexColor("#CBD5E1"))
    
    # Word wrap
    lines = []
    max_chars = int(w / 6.2)
    for raw_p in desc.split('\n'):
        if not raw_p.strip():
            lines.append("")
            continue
        tokens = raw_p.split()
        cur = []
        for token in tokens:
            cur.append(token)
            if len(" ".join(cur)) > max_chars:
                lines.append(" ".join(cur[:-1]))
                cur = [token]
        if cur:
            lines.append(" ".join(cur))
    
    for i, line in enumerate(lines[:12]):
        canvas.drawString(x + 12, y + h - 46 - i * (desc_sz + 4), line)

# Slides list
slides = []

# S1: Cover
def s1(c, d):
    dark_bg(c, d, 1)
    c.saveState()
    c.setFillColor(colors.HexColor("#1E1B4B"))
    c.circle(W * 0.75, H * 0.5, 180, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#312E81"))
    c.circle(W * 0.75, H * 0.5, 120, fill=1, stroke=0)
    c.setFillColor(INDIGO)
    c.circle(W * 0.75, H * 0.5, 70, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(WHITE)
    c.drawCentredString(W * 0.75, H * 0.5 - 14, "🌐")

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(CYAN)
    c.drawString(30, H - 70, "COGCULTURE ASSESSMENT · PART 1: PRODUCT STRATEGY & ROADMAP")
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(WHITE)
    c.drawString(30, H * 0.65, "Generative Engine")
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(CYAN)
    c.drawString(30, H * 0.65 - 40, "Optimization (GEO)")
    c.setFont("Helvetica", 13)
    c.setFillColor(INDIGO_LT)
    c.drawString(30, H * 0.65 - 72, "AI Competitor Benchmarking & Cross-LLM Visibility Engine")

    c.setStrokeColor(INDIGO)
    c.setLineWidth(2)
    c.line(30, H * 0.65 - 84, 300, H * 0.65 - 84)

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(WHITE)
    c.drawString(30, H * 0.65 - 110, "Candidate: Anshika Arora")
    c.setFont("Helvetica", 9.5)
    c.setFillColor(SLATE)
    c.drawString(30, H * 0.65 - 128, "Product Management Trainee | CogCulture")
    c.restoreState()
slides.append(s1)

# S2: Market Context
def s2(c, d):
    dark_bg(c, d, 2)
    draw_header(c, "01 · STRATEGIC CONTEXT", "The Paradigm Shift: From Search Engines to Answer Engines")
    cards = [
        ("📉 The Collapse of Traditional SEO", "Search volume is bleeding to AI Answer Engines.\nOver 60% of consumer and B2B queries are now resolved directly within chat interfaces without clicking a link.\nTraditional backlinks & keywords no longer guarantee discovery.", RED),
        ("🤖 How LLMs Recommend Brands", "LLMs (ChatGPT, Perplexity, Claude, Gemini) synthesize answers using authoritative consensus, knowledge graphs, and trusted citations.\nThey choose winners based on entity prominence, not keyword density.", CYAN),
        ("🎯 The Enterprise Blind Spot", "CMOs spend millions on marketing but have zero real-time visibility into whether AI engines recommend their brand or their competitor when users ask buying queries.", AMBER)
    ]
    for i, (title, desc, col) in enumerate(cards):
        draw_card(c, 30 + i * 262, 50, 252, 400, title, desc, col)
slides.append(s2)

# S3: Competitive Landscape
def s3(c, d):
    dark_bg(c, d, 3)
    draw_header(c, "02 · COMPETITIVE LANDSCAPE", "Competitive Benchmarking: Where Market Tools Fall Short")
    # Table headers
    headers = ["Capability", "Traditional SEO", "First-Gen GEO", "CogCulture GEO"]
    cols = [160, 180, 190, 230]
    rows = [
        ["Model Coverage", "Google/Bing SERPs", "ChatGPT only (static)", "GPT-4o, Perplexity, Gemini, Claude"],
        ["Citation Graph", "Backlink URLs only", "Surface mentions", "Deep Source Attribution (Reddit/Wiki/G2)"],
        ["Sentiment / Bias", "Basic sentiment", "None", "Multidimensional Win/Loss & Bias scoring"],
        ["Competitor Gap", "Keyword overlap", "Basic table", "Prompt-level Competitor Displacement"],
        ["Remediation", "Meta tags / backlinks", "Manual suggestions", "Automated Knowledge Injection Playbook"]
    ]
    tx, ty = 30, H - 100
    for ci, (h, w) in enumerate(zip(headers, cols)):
        c.setFillColor(INDIGO if ci == 3 else colors.HexColor("#1E293B"))
        c.rect(tx, ty - 18, w - 4, 22, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(WHITE)
        c.drawString(tx + 6, ty - 10, h)
        tx += w
    for ri, r in enumerate(rows):
        ty -= 30
        tx = 30
        alt = BG_CARD if ri % 2 == 0 else colors.HexColor("#0E1420")
        for ci, (val, w) in enumerate(zip(r, cols)):
            c.setFillColor(alt)
            c.rect(tx, ty - 18, w - 4, 26, fill=1, stroke=0)
            c.setFont("Helvetica-Bold" if ci in [0, 3] else "Helvetica", 8.5)
            c.setFillColor(GREEN if ci == 3 else (WHITE if ci == 0 else SLATE))
            c.drawString(tx + 6, ty - 8, val[:36] + ("..." if len(val) > 36 else ""))
            tx += w
slides.append(s3)

# S4: Feature Architecture
def s4(c, d):
    dark_bg(c, d, 4)
    draw_header(c, "03 · FEATURE BLUEPRINT", "Feature: Multi-LLM Competitor Share of Voice & Citation Engine")
    steps = [
        ("1. Synthetic Prompts", "Generates hundreds of high-intent buying prompts based on persona & industry vertical.", INDIGO),
        ("2. Cross-Model Crawl", "Queries ChatGPT (GPT-4o), Perplexity Pro, Google Gemini 2.0, and Claude 3.5 Sonnet concurrently.", CYAN),
        ("3. Citation Parser", "Extracts brand name, co-mentioned competitors, sentiment, and the exact publisher links cited.", GREEN),
        ("4. SoV Scoring", "Calculates Brand Share of Voice Index (0-100%), Competitor Win/Loss Ratio, and Authority Rank.", AMBER)
    ]
    for i, (title, desc, col) in enumerate(steps):
        draw_card(c, 30 + i * 196, 50, 186, 400, title, desc, col, title_sz=11, desc_sz=8)
slides.append(s4)

# S5: Dashboard Walkthrough
def s5(c, d):
    dark_bg(c, d, 5)
    draw_header(c, "04 · DASHBOARD WALKTHROUGH", "Inside the Executive Benchmarking Dashboard")
    items = [
        ("📊 Cross-LLM Visibility Matrix", "Side-by-side visibility percentages across GPT-4o, Perplexity, Gemini, and Claude. Identifies model bias towards competitors.", INDIGO),
        ("🔗 Citation Source Attribution Graph", "Pinpoints exactly WHERE the AI engines get data: Reddit discussions, Wikipedia, G2 reviews, YouTube, or PR wires.", CYAN),
        ("🥊 Competitor Displacement Index", "Reveals prompts where competitors win over your brand and extracts the explicit rationale provided by the LLM.", AMBER),
        ("🚨 Hallucination & Disparagement Alerting", "Detects when LLMs spread inaccurate specs, outdated pricing, or negative misinformation about your brand.", RED)
    ]
    for i, (title, desc, col) in enumerate(items):
        y = H - 110 - i * 86
        c.setFillColor(BG_CARD)
        c.roundRect(30, y - 56, W - 60, 64, 8, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(30, y - 56, 4, 64, 2, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(WHITE)
        c.drawString(44, y - 18, title)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(SLATE)
        c.drawString(44, y - 38, desc)
slides.append(s5)

# S6: Remediation Playbook
def s6(c, d):
    dark_bg(c, d, 6)
    draw_header(c, "05 · ACTIONABLE VALUE", "Closing the Loop: Automated GEO Remediation Playbook")
    cards = [
        ("1. Knowledge Graph Seeding", "Auto-generates structured schema markup (JSON-LD), entity descriptions, and authoritative Wikidata links to anchor your brand firmly in LLM training corpora.", INDIGO),
        ("2. Targeted PR & Citation Placement", "Identifies the top 10 domains cited by LLMs in your industry (e.g. specific TechCrunch articles, Substack newsletters) for focused PR outreach.", CYAN),
        ("3. Community Consensus Engineering", "Highlights influential Reddit and forum discussions crawled by LLMs for user sentiment, enabling proactive brand advocacy and review management.", GREEN)
    ]
    for i, (title, desc, col) in enumerate(cards):
        draw_card(c, 30 + i * 262, 50, 252, 400, title, desc, col)
slides.append(s6)

# S7: Short-Term Roadmap
def s7(c, d):
    dark_bg(c, d, 7)
    draw_header(c, "06 · PRODUCT STRATEGY", "Short-Term Product Roadmap (Months 1 – 3: MVP & Validation)")
    months = [
        ("Month 1: Foundation", "• Build prompt synthesis engine for 5 target industry verticals.\n• Implement automated connectors for ChatGPT (OpenAI) & Perplexity Pro.\n• Establish baseline Share of Voice (SoV) scoring model.\n• Internal alpha testing.", INDIGO),
        ("Month 2: Expansion", "• Integrate Google Gemini 2.0 and Anthropic Claude 3.5 Sonnet.\n• Launch Citation Attribution Crawler to extract source URLs.\n• Deliver alpha dashboard to 10 pilot enterprise partners.\n• User feedback & heuristic tuning.", CYAN),
        ("Month 3: Closed Beta", "• Roll out Competitor Win/Loss Gap Analysis table.\n• Add automated weekly email alerts for major SoV shifts.\n• Launch Closed Beta with self-serve billing & Stripe integration.\n• Case study generation.", GREEN)
    ]
    for i, (title, desc, col) in enumerate(months):
        draw_card(c, 30 + i * 262, 50, 252, 400, title, desc, col)
slides.append(s7)

# S8: Long-Term Roadmap
def s8(c, d):
    dark_bg(c, d, 8)
    draw_header(c, "07 · PRODUCT STRATEGY", "Long-Term Product Roadmap (Months 4 – 12: Scale & Dominance)")
    quarters = [
        ("Q2 (M 4–6): Remediation Engine", "• Automated Knowledge Graph Generator (one-click JSON-LD).\n• Content Optimizer: Generates LLM-optimized comparison pages and PR briefs.\n• Public API access for agency partners & enterprise integrations.", INDIGO),
        ("Q3 (M 7–9): Real-Time & Voice", "• Support Voice AI search engines (Apple Siri Intelligence, Meta AI, Google Voice).\n• Sentiment Defense Layer: Alerts on hallucinated brand disparagement.\n• Multi-language localization (US, UK, EMEA, APAC).", CYAN),
        ("Q4 (M 10–12): Predictive AI", "• Predictive LLM Algorithm: Forecasts SoV impact prior to publishing content.\n• Autonomous Agent: Auto-submits corrections to citation databases.\n• White-label platform for global enterprise agency partners.", GREEN)
    ]
    for i, (title, desc, col) in enumerate(quarters):
        draw_card(c, 30 + i * 262, 50, 252, 400, title, desc, col)
slides.append(s8)

# S9: Monetization
def s9(c, d):
    dark_bg(c, d, 9)
    draw_header(c, "08 · BUSINESS MODEL", "Monetization Strategy: SaaS Tiers & Agency Services")
    tiers = [
        ("Starter / Growth", "$299 / month\nMid-Market & Scaleups", "• Track 50 prompts / month\n• 2 LLMs (ChatGPT & Perplexity)\n• Weekly SoV audits\n• 3 Competitors benchmarked\n• Email alert digests", CYAN),
        ("Professional", "$899 / month\nEnterprise Brands", "• Track 250 prompts / month\n• 4 LLMs (GPT, Perplexity, Gemini, Claude)\n• Daily citation crawl & attribution\n• 10 Competitors benchmarked\n• Automated Remediation Playbooks", INDIGO),
        ("Enterprise & Agency", "$2,499+ / month\nGlobal Brands & Agencies", "• Unlimited custom prompt tracking\n• Real-Time LLM tracking & Webhooks\n• Multi-brand agency dashboard\n• Full REST API & White-Label reports\n• Dedicated CogCulture Strategist", GREEN)
    ]
    for i, (title, price_target, desc, col) in enumerate(tiers):
        draw_card(c, 30 + i * 262, 50, 252, 400, f"{title}\n{price_target}", desc, col)
slides.append(s9)

# S10: Conclusion
def s10(c, d):
    dark_bg(c, d, 10)
    c.saveState()
    c.setFillColor(colors.HexColor("#1E1B4B"))
    c.circle(W / 2, H / 2 + 10, 160, fill=1, stroke=0)
    c.setFillColor(INDIGO)
    c.circle(W / 2, H / 2 + 10, 50, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, H / 2 - 2, "🚀")

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, H / 2 - 70, "CogCulture GEO: The Next Generation of Search")
    c.setFont("Helvetica", 12)
    c.setFillColor(CYAN)
    c.drawCentredString(W / 2, H / 2 - 92, "Empowering brands to own their reputation in the AI era.")

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(SLATE)
    c.drawCentredString(W / 2, H / 2 - 124, "Part 1 (GEO Feature & Strategy) & Part 2 (Truth Layer Fact-Checking Agent)")
    c.drawCentredString(W / 2, H / 2 - 142, "Submission by Anshika Arora")
    c.restoreState()
slides.append(s10)

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

out_pdf = os.path.join(os.path.dirname(__file__), "geo_product_presentation.pdf")
pdf = SlidePDF(out_pdf, slides)
story = []
for i in range(len(slides)):
    story.append(Spacer(1, 1))
    if i < len(slides) - 1:
        story.append(PageBreak())
pdf.build(story)
print(f"[+] Successfully generated Part 1 GEO PDF: {out_pdf}")
