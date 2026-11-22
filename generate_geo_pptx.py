"""
generate_geo_pptx.py
Builds the official Part 1 PowerPoint (.pptx) & PDF presentation for CogCulture:
Feature: Cross-LLM AI Competitor Benchmarking & Share of Voice Dashboard for GEO.
Author: Anshika Arora
"""

import sys
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ── Color Palette ────────────────────────────────────────────────────────
BG_DARK = RGBColor(10, 14, 26)       # #0A0E1A
CARD_DARK = RGBColor(19, 27, 46)     # #131B2E
INDIGO = RGBColor(99, 102, 241)      # #6366F1
INDIGO_LT = RGBColor(165, 180, 252)  # #A5B4FC
SLATE = RGBColor(148, 163, 184)      # #94A3B8
WHITE = RGBColor(255, 255, 255)
GREEN = RGBColor(16, 185, 129)       # #10B981
AMBER = RGBColor(245, 158, 11)       # #F59E0B
RED = RGBColor(239, 68, 68)          # #EF4444
CYAN = RGBColor(6, 182, 212)         # #06B6D4

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, tag_text, title_text):
    box = slide.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(1.3))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = tag_text
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INDIGO_LT
    
    p2 = tf.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(25)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

# =========================================================================
# SLIDE 1: Cover Slide
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_bg(s1)

box = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(0.5))
p = box.text_frame.paragraphs[0]
p.text = "COGCULTURE ASSESSMENT · PART 1: PRODUCT STRATEGY & ROADMAP"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INDIGO_LT

box = s1.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(2.2))
tf = box.text_frame
p = tf.paragraphs[0]
p.text = "Generative Engine Optimization (GEO)"
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "AI Competitor Benchmarking & Cross-LLM Share of Voice Dashboard"
p2.font.size = Pt(22)
p2.font.color.rgb = CYAN

p3 = tf.add_paragraph()
p3.text = "\nHelping brands track, quantify, and dominate brand mentions & citations across ChatGPT, Perplexity, Gemini, and Claude."
p3.font.size = Pt(13)
p3.font.color.rgb = SLATE

box = s1.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(11.3), Inches(1.5))
tf = box.text_frame
p = tf.paragraphs[0]
p.text = "Candidate: Anshika Arora"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = WHITE

p2 = tf.add_paragraph()
p2.text = "Role: Product Management Trainee | Focus: GEO Product Architecture & Monetization"
p2.font.size = Pt(12)
p2.font.color.rgb = SLATE

# =========================================================================
# SLIDE 2: The Paradigm Shift: Why SEO Is Dying and GEO Is Winning
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
set_bg(s2)
add_header(s2, "01 · STRATEGIC CONTEXT & MARKET NEED", "The Paradigm Shift: From Search Engines to Answer Engines")

cards = [
    ("📉 The Collapse of Traditional SEO", "Search traffic is plummeting as 60%+ of queries are answered directly by LLMs (Zero-Click Searches). Traditional backlinks & keywords no longer guarantee brand visibility.", RED),
    ("🤖 How AI Recommends Brands", "LLMs (ChatGPT, Perplexity, Claude, Gemini) don't rank URLs; they synthesize answers using authoritative citations, digital consensus, and factual knowledge graphs.", CYAN),
    ("🎯 The Blind Spot for CMOs", "Marketing leaders have zero visibility into whether LLMs recommend their product or their competitors when users ask: 'What is the best CRM / shoes / cloud platform?'", AMBER)
]

for i, (title, desc, color) in enumerate(cards):
    left = Inches(1.0 + i * 3.85)
    card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.3), Inches(3.6), Inches(4.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(12)
    p2.font.color.rgb = SLATE

# =========================================================================
# SLIDE 3: Competitive Landscape: Existing Tools vs CogCulture GEO
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
set_bg(s3)
add_header(s3, "02 · COMPETITIVE LANDSCAPE & GAP ANALYSIS", "Benchmarking Current Market Tools & The CogCulture Moat")

table_data = [
    ("Capability / Feature", "Traditional SEO (Semrush/Ahrefs)", "First-Gen GEO (Profound/Athena)", "CogCulture GEO Platform"),
    ("LLM Tracking Scope", "Google/Bing SERPs only", "ChatGPT only (static prompts)", "Multi-LLM (ChatGPT, Perplexity, Claude, Gemini)"),
    ("Citation Attribution Graph", "Backlink URLs only", "Surface-level mentions", "Deep Source Citations (Reddit, Wikipedia, Media, G2)"),
    ("Sentiment & Bias Scoring", "Basic sentiment", "None", "Multidimensional (Favorability, Win/Loss, Hallucination)"),
    ("Competitor Win/Loss Gap", "Keyword overlap", "Basic rank table", "Prompt-level Competitor Displacement Intelligence"),
    ("Actionable Remediation", "Meta tags & backlinks", "Manual suggestions", "Automated Knowledge Injection Playbook (Schema/PR)")
]

t_shape = s3.shapes.add_table(len(table_data), 4, Inches(1.0), Inches(2.1), Inches(11.33), Inches(4.5))
table = t_shape.table

for r_idx, row in enumerate(table_data):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx, c_idx)
        cell.text = val
        cell.fill.solid()
        if r_idx == 0:
            cell.fill.fore_color.rgb = INDIGO
            p = cell.text_frame.paragraphs[0]
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = WHITE
        else:
            cell.fill.fore_color.rgb = CARD_DARK
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10.5)
            if c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = GREEN
            elif c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE
            else:
                p.font.color.rgb = SLATE

# =========================================================================
# SLIDE 4: Proposed Feature Architecture & Walkthrough
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
set_bg(s4)
add_header(s4, "03 · FEATURE BLUEPRINT", "Feature: Multi-LLM Competitor Share of Voice & Citation Engine")

steps = [
    ("1. Synthetic Prompt Matrix", "Generates hundreds of high-intent buying prompts based on persona, industry & intent (e.g., 'Best enterprise CRM for fintech').", INDIGO),
    ("2. Cross-Model Simulation", "Queries ChatGPT (GPT-4o), Perplexity Pro, Google Gemini 2.0, and Claude 3.5 Sonnet in real-time across varied geo-locations.", CYAN),
    ("3. Citation & Mention Parser", "Extracts brand name, co-mentioned competitors, sentiment polarity, and the exact publisher links cited as grounding sources.", GREEN),
    ("4. Share of Voice (SoV) Scoring", "Calculates proprietary Brand SoV Index (0-100%), Competitor Win/Loss Ratio, and Citation Authority Rank.", AMBER)
]

for i, (title, desc, color) in enumerate(steps):
    left = Inches(1.0 + i * 2.85)
    card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.3), Inches(2.7), Inches(4.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = WHITE

# =========================================================================
# SLIDE 5: Core User Experience & Dashboard Walkthrough
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
set_bg(s5)
add_header(s5, "04 · DASHBOARD WALKTHROUGH", "Inside the Executive Benchmarking Dashboard")

dash_items = [
    ("📊 Cross-LLM Visibility Matrix", "Shows side-by-side visibility percentages across GPT-4o, Perplexity, Gemini, and Claude. Identifies which model favors your brand vs competitor.", INDIGO),
    ("🔗 Citation Source Attribution Graph", "Pinpoints exactly WHERE the LLM got its data: Reddit threads, Wikipedia articles, G2 reviews, YouTube transcripts, or press releases.", CYAN),
    ("🥊 Competitor Displacement Index", "Reveals the top 5 prompts where competitors are recommended over your brand, and the exact rationale the LLM provided for choosing them.", AMBER),
    ("🚨 Hallucination & Sentiment Alerting", "Flags negative sentiment or factual inaccuracies in LLM responses (e.g., LLM falsely claiming your product lacks a key feature).", RED)
]

for i, (title, desc, color) in enumerate(dash_items):
    y_pos = Inches(2.2 + i * 1.1)
    box = s5.shapes.add_textbox(Inches(1.0), y_pos, Inches(11.3), Inches(0.95))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(12)
    p2.font.color.rgb = SLATE

# =========================================================================
# SLIDE 6: Actionable Output: The GEO Optimization Playbook
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
set_bg(s6)
add_header(s6, "05 · ACTIONABLE VALUE", "Closing the Loop: Automated GEO Remediation Playbook")

p_cards = [
    ("1. Knowledge Graph Seeding", "Auto-generates structured schema markup (JSON-LD), entity descriptions, and authoritative Wikidata/Wikidata references to anchor your brand.", INDIGO),
    ("2. Targeted PR & Citation Placement", "Identifies the exact top 10 domains being cited by LLMs in your niche (e.g. specific TechCrunch articles, Substack newsletters) for targeted outreach.", CYAN),
    ("3. Community Consensus Engineering", "Highlights influential Reddit and forum discussions that LLMs crawl for real-world user reviews, enabling proactive brand advocacy.", GREEN)
]

for i, (title, desc, color) in enumerate(p_cards):
    left = Inches(1.0 + i * 3.85)
    card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.4), Inches(3.6), Inches(4.0))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(12)
    p2.font.color.rgb = SLATE

# =========================================================================
# SLIDE 7: Short-Term Roadmap (Months 1–3)
# =========================================================================
s7 = prs.slides.add_slide(blank_layout)
set_bg(s7)
add_header(s7, "06 · PRODUCT STRATEGY", "Short-Term Product Roadmap (Months 1 – 3: MVP & Validation)")

m_items = [
    ("Month 1: Foundation & Core Ingestion", "• Build prompt synthesis engine for 5 target industry verticals.\n• Implement automated API connectors to ChatGPT (OpenAI) & Perplexity Pro.\n• Establish baseline Share of Voice (SoV) scoring algorithm.", INDIGO),
    ("Month 2: Multi-LLM Expansion & Attribution", "• Integrate Google Gemini 2.0 and Anthropic Claude 3.5 Sonnet endpoints.\n• Launch Citation Attribution Crawler to extract and classify source URLs.\n• Deliver alpha dashboard to 10 pilot enterprise design partners.", CYAN),
    ("Month 3: Competitor Benchmark & Closed Beta", "• Roll out Competitor Win/Loss Gap Analysis table.\n• Add automated weekly email alerts highlighting major SoV shifts.\n• Launch Closed Beta with self-serve signup & billing integration.", GREEN)
]

for i, (title, desc, color) in enumerate(m_items):
    left = Inches(1.0 + i * 3.85)
    card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.3), Inches(3.6), Inches(4.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = WHITE

# =========================================================================
# SLIDE 8: Long-Term Roadmap (Months 4–12)
# =========================================================================
s8 = prs.slides.add_slide(blank_layout)
set_bg(s8)
add_header(s8, "07 · PRODUCT STRATEGY", "Long-Term Product Roadmap (Months 4 – 12: Scale & Dominance)")

lt_items = [
    ("Q2 (Months 4–6): Remediation & Optimization Engine", "• Automated Knowledge Graph Generator (one-click JSON-LD code).\n• Content Optimizer: Generates LLM-optimized comparison pages and PR briefs.\n• Public API access for agency partners & enterprise integrations.", INDIGO),
    ("Q3 (Months 7–9): Real-Time Voice Search & Social LLMs", "• Support Voice AI search engines (Apple Siri Intelligence, Meta AI, Google Voice).\n• Sentiment Defense Layer: Detects & alerts on hallucinated brand disparagement.\n• Multi-language & regional localization support (US, UK, EMEA, APAC).", CYAN),
    ("Q4 (Months 10–12): Predictive Visibility & Automation", "• Predictive LLM Algorithm: Forecasts SoV impact prior to publishing content.\n• Autonomous Agent: Auto-submits corrections to citation databases.\n• Enterprise White-Label platform for global marketing agencies.", GREEN)
]

for i, (title, desc, color) in enumerate(lt_items):
    left = Inches(1.0 + i * 3.85)
    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.3), Inches(3.6), Inches(4.2))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = WHITE

# =========================================================================
# SLIDE 9: Monetization Strategy & Tiered Pricing Model
# =========================================================================
s9 = prs.slides.add_slide(blank_layout)
set_bg(s9)
add_header(s9, "08 · BUSINESS MODEL & MONETIZATION", "Tiered SaaS Pricing & Agency Revenue Streams")

pricing_tiers = [
    ("Starter / Growth", "$299 / month", "Mid-market & High-Growth Startups",
     "• Track 50 prompts / month\n• 2 LLMs (ChatGPT & Perplexity)\n• Weekly SoV audits\n• 3 Competitors benchmarked\n• Email alert digests", CYAN),
    ("Professional", "$899 / month", "Enterprise Brands & Scaleups",
     "• Track 250 prompts / month\n• 4 LLMs (GPT, Perplexity, Gemini, Claude)\n• Daily citation crawl & attribution\n• 10 Competitors benchmarked\n• Automated Remediation Playbooks", INDIGO),
    ("Enterprise & Agency", "$2,499+ / month", "Global Enterprises & Agency Partners",
     "• Unlimited custom prompt tracking\n• Real-Time LLM tracking & Webhooks\n• Multi-brand agency dashboard\n• Full REST API & White-Label reports\n• Dedicated CogCulture GEO Strategist", GREEN)
]

for i, (name, price, target, feats, color) in enumerate(pricing_tiers):
    left = Inches(1.0 + i * 3.85)
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(2.2), Inches(3.6), Inches(4.4))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_DARK
    card.line.color.rgb = color
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = name
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = price
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    
    p3 = tf.add_paragraph()
    p3.text = target + "\n"
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = SLATE
    
    p4 = tf.add_paragraph()
    p4.text = feats
    p4.font.size = Pt(11)
    p4.font.color.rgb = WHITE

# =========================================================================
# SLIDE 10: Conclusion & Measurable Business Impact
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
set_bg(s10)
add_header(s10, "09 · CONCLUSION & BUSINESS OUTCOMES", "Strategic Value Proposition for CogCulture")

box = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(11.3), Inches(3.8))
tf = box.text_frame
p = tf.paragraphs[0]
p.text = "🎯 Transforming CogCulture into the Premier Authority in Generative Search"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = GREEN

p2 = tf.add_paragraph()
p2.text = "\n1. First-Mover Advantage: Captures enterprise marketing budgets as CMOs reallocate spend from declining SEO to GEO."
p2.font.size = Pt(13)
p2.font.color.rgb = WHITE

p3 = tf.add_paragraph()
p3.text = "\n2. High-Margin Recurring SaaS: $299–$2,499/mo SaaS model creates sticky enterprise recurring revenue with low marginal compute costs."
p3.font.size = Pt(13)
p3.font.color.rgb = WHITE

p4 = tf.add_paragraph()
p4.text = "\n3. Agency Flywheel: Generates high-value retainers for CogCulture's agency arm to execute the recommended PR and content playbooks."
p4.font.size = Pt(13)
p4.font.color.rgb = WHITE

p5 = tf.add_paragraph()
p5.text = "\n\nCandidate: Anshika Arora  |  CogCulture Assessment  |  Part 1 (GEO) & Part 2 (Truth Layer)"
p5.font.size = Pt(12)
p5.font.bold = True
p5.font.color.rgb = INDIGO_LT

out_pptx = os.path.join(os.path.dirname(__file__), "geo_product_presentation.pptx")
prs.save(out_pptx)
print(f"[+] Successfully generated Part 1 GEO PowerPoint: {out_pptx}")
