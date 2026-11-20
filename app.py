"""
app.py
Enterprise-Grade Fact-Checking & Pre-Publication Risk Gatekeeper: Truth Layer.
Featuring modern Obsidian-Cyber Executive styling, visual charts (Altair),
interactive document redlines, and downloadable PDF compliance certificates.
"""

import os
import sys
import json
import hashlib
from datetime import datetime
import pandas as pd
import altair as alt
import streamlit as st

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.models import Claim, ClaimStatus, ClaimCategory, FactCheckReport, DocumentExtractionSummary
from core.extractor import DocumentExtractor, ClaimExtractor
from core.verifier import FactCheckVerifier
from core.pdf_exporter import generate_audit_certificate_pdf
from core.sample_generator import generate_trap_pdf, generate_pitch_deck_pdf, generate_esg_pdf

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Truth Layer Enterprise | AI Fact-Checking Gatekeeper",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling: Obsidian-Cyber Executive Dark Theme
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }

    /* Hero Header */
    .hero-header-box {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 2px;
        margin-bottom: 8px;
    }
    .hero-icon {
        font-size: 2.5rem;
        line-height: 1;
        display: inline-block;
        filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.4));
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        line-height: 1.2;
        margin: 0;
        padding: 0;
    }
    .hero-title-accent {
        color: #818CF8;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .hero-pills {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 9999px;
        padding: 4px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #C7D2FE;
        letter-spacing: 0.02em;
    }

    /* Glassmorphism Metric Cards */
    .metric-card-glass {
        background: rgba(19, 27, 46, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card-glass:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    .metric-num {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
    }

    /* Executive Clearance Banners */
    .clearance-glow-banner {
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 10px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(12px);
        border-width: 1.5px;
        border-style: solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .clearance-glow-passed {
        background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.18) 0%, rgba(15, 23, 42, 0.8) 90%);
        border-color: rgba(16, 185, 129, 0.6);
        color: #E2E8F0;
    }
    .clearance-glow-conditional {
        background: radial-gradient(circle at 10% 20%, rgba(245, 158, 11, 0.18) 0%, rgba(15, 23, 42, 0.8) 90%);
        border-color: rgba(245, 158, 11, 0.6);
        color: #E2E8F0;
    }
    .clearance-glow-rejected {
        background: radial-gradient(circle at 10% 20%, rgba(239, 68, 68, 0.18) 0%, rgba(15, 23, 42, 0.8) 90%);
        border-color: rgba(239, 68, 68, 0.6);
        color: #E2E8F0;
    }

    /* Badges */
    .badge-neon-verified {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-neon-inaccurate {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    .badge-neon-false {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }

    /* Claim Inspection Cards */
    .claim-card-dark {
        background: rgba(19, 27, 46, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    .claim-card-dark:hover {
        border-color: rgba(129, 140, 248, 0.4);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }
    .claim-text-title {
        font-size: 1.08rem;
        font-weight: 600;
        color: #F8FAFC;
        line-height: 1.5;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    .correction-box-glow {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        margin-bottom: 12px;
        color: #FDE68A;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .evidence-box-dark {
        background: rgba(15, 23, 42, 0.6);
        border-left: 4px solid #6366F1;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 8px;
        font-size: 0.9rem;
        color: #CBD5E1;
        line-height: 1.5;
    }
    .source-pill-dark {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.8rem;
        color: #A5B4FC;
        text-decoration: none;
        margin-right: 8px;
        margin-top: 8px;
        transition: all 0.15s ease;
    }
    .source-pill-dark:hover {
        background: rgba(99, 102, 241, 0.3);
        color: #FFFFFF;
        text-decoration: none;
    }

    /* Redline Track Changes Document Card */
    .redline-canvas {
        background: rgba(19, 27, 46, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 28px;
        line-height: 1.9;
        font-size: 1.03rem;
        color: #E2E8F0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .redline-del {
        background-color: rgba(239, 68, 68, 0.2);
        color: #FCA5A5;
        text-decoration: line-through;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 500;
        border: 1px dashed rgba(239, 68, 68, 0.4);
    }
    .redline-ins {
        background-color: rgba(16, 185, 129, 0.2);
        color: #6EE7B7;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    .redline-verified {
        background-color: rgba(16, 185, 129, 0.08);
        color: #A7F3D0;
        padding: 2px 6px;
        border-radius: 4px;
        border-bottom: 1.5px solid #10B981;
    }

    /* Preset Selection Cards */
    .preset-card {
        background: rgba(19, 27, 46, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
    }
    .preset-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
        background: rgba(25, 36, 61, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: Setup & Verification Controls
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.markdown("### **TruthLayer Enterprise**")
    st.caption("AI-Powered Due-Diligence & Fact Gatekeeper")
    st.markdown("---")

    st.subheader("⚙️ Verification Engine")
    
    # Environment or Streamlit Secrets API Key handling
    default_gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    if not default_gemini_key and hasattr(st, "secrets"):
        try:
            default_gemini_key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
        except Exception:
            pass

    gemini_key = st.text_input(
        "Gemini API Key (Optional)",
        value=default_gemini_key,
        type="password",
        help="Enables Google Search Grounding with Gemini 2.0/2.5. If empty, runs on the built-in zero-cost Live Web Engine."
    )

    tavily_key = st.text_input(
        "Tavily API Key (Optional)",
        value=os.getenv("TAVILY_API_KEY", ""),
        type="password",
        help="Optional live search provider key."
    )

    if gemini_key:
        st.success("🟢 Google Search Grounding Active")
    else:
        st.info("🌐 Keyless Live Web Engine (Zero-Cost Mode)")

    st.markdown("---")
    st.subheader("🏢 Target Audit Scenarios")
    st.markdown("""
    - 🦄 **Investor Decks & TAM Claims**
    - 🌱 **ESG & Climate Compliance**
    - 📄 **Marketing Collateral & Whitepapers**
    - ⚖️ **Procurement & Vendor Vetting**
    """)

    st.markdown("---")
    st.caption("Engineered by **Anshika Arora**")
    st.caption("Production Architecture & CI/CD Validated")

# ---------------------------------------------------------
# Session State Initialization & Fixtures
# ---------------------------------------------------------
if "doc_summary" not in st.session_state:
    st.session_state.doc_summary = None
if "claims" not in st.session_state:
    st.session_state.claims = []
if "report" not in st.session_state:
    st.session_state.report = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
os.makedirs(sample_dir, exist_ok=True)
trap_pdf_path = os.path.join(sample_dir, "trap_marketing_document.pdf")
pitch_pdf_path = os.path.join(sample_dir, "series_b_pitch_deck.pdf")
esg_pdf_path = os.path.join(sample_dir, "corporate_esg_audit.pdf")

if not os.path.exists(trap_pdf_path):
    generate_trap_pdf(trap_pdf_path)
if not os.path.exists(pitch_pdf_path):
    generate_pitch_deck_pdf(pitch_pdf_path)
if not os.path.exists(esg_pdf_path):
    generate_esg_pdf(esg_pdf_path)

# ---------------------------------------------------------
# Hero Section
# ---------------------------------------------------------
st.markdown("""
<div class="hero-header-box">
    <span class="hero-icon">🛡️</span>
    <span class="hero-title">Truth Layer <span class="hero-title-accent">Enterprise</span></span>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero-subtitle">
Automated Pre-Publication Due-Diligence & Fact Gatekeeper. Reads PDF collateral, separates testable metrics 
from marketing fluff, cross-references against live web consensus, and generates executive redline audits.
</div>
<div class="hero-pills">
    <span class="hero-pill">⚡ Sub-5s Grounded Audit</span>
    <span class="hero-pill">🌐 Dual-Mode Verification</span>
    <span class="hero-pill">📝 Word-Style Track Changes</span>
    <span class="hero-pill">🔒 SHA-256 Checksummed PDF</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Input Methods (Tabs)
# ---------------------------------------------------------
tab_upload, tab_presets, tab_text = st.tabs([
    "📄 Upload PDF Document", 
    "🧪 1-Click Industry Presets", 
    "✍️ Direct Text Paste"
])

def _load_preset_file(file_path: str, display_name: str):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
        claims = ClaimExtractor.extract_claims_from_pages(pages_data)
        summary = ClaimExtractor.summarize_extraction(display_name, full_text, pages_data, claims)
        st.session_state.doc_summary = summary
        st.session_state.claims = claims
        st.session_state.raw_text = full_text
        st.session_state.report = None
        st.rerun()

with tab_upload:
    uploaded_file = st.file_uploader(
        "Upload PDF collateral (Pitch Deck, Whitepaper, ESG Report, or Brief)", 
        type=["pdf"],
        help="Upload any PDF to extract and audit verifiable claims."
    )
    if uploaded_file is not None:
        if st.button("Extract Claims from Uploaded PDF", type="primary"):
            with st.spinner("Parsing PDF stream and extracting verifiable claims..."):
                pdf_bytes = uploaded_file.read()
                full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
                claims = ClaimExtractor.extract_claims_from_pages(pages_data)
                summary = ClaimExtractor.summarize_extraction(uploaded_file.name, full_text, pages_data, claims)
                st.session_state.doc_summary = summary
                st.session_state.claims = claims
                st.session_state.raw_text = full_text
                st.session_state.report = None
                st.rerun()

with tab_presets:
    st.markdown("Test the agent with **1 click** using realistic industry scenarios:")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("""
        <div class="preset-card">
            <div style="font-size: 1.25rem; margin-bottom: 6px;">📊 <b>Assessment Trap Doc</b></div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 12px;">
                Official CogCulture Benchmark. Outdated GDP figures, ChatGPT 2021 date, fake founding history, and agency scale lies.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Load Trap Document", key="btn_trap", use_container_width=True):
            _load_preset_file(trap_pdf_path, "trap_marketing_document.pdf")

    with col_p2:
        st.markdown("""
        <div class="preset-card">
            <div style="font-size: 1.25rem; margin-bottom: 6px;">🦄 <b>Series B Pitch Deck</b></div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 12px;">
                Venture Due-Diligence. Exaggerated $15T AI market TAM, fabricated DAU growth velocity, and founder credentials.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Load Pitch Deck", key="btn_pitch", use_container_width=True):
            _load_preset_file(pitch_pdf_path, "series_b_pitch_deck.pdf")

    with col_p3:
        st.markdown("""
        <div class="preset-card">
            <div style="font-size: 1.25rem; margin-bottom: 6px;">🌱 <b>Corporate ESG Audit</b></div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 12px;">
                Regulatory & Sustainability. Greenwashing claims, retroactive net-zero milestones, and emissions figures.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Load ESG Report", key="btn_esg", use_container_width=True):
            _load_preset_file(esg_pdf_path, "corporate_esg_audit.pdf")

with tab_text:
    pasted_text = st.text_area(
        "Or paste raw copy, press releases, or claim statements directly:",
        height=160,
        placeholder="e.g., Tesla was founded in 2008 by Elon Musk. OpenAI ChatGPT reached 100 million active users in March 2021. Our digital ecosystem delivers unprecedented synergy..."
    )
    if st.button("Extract Claims from Text"):
        if pasted_text.strip():
            pages_data = [{"page_num": 1, "text": pasted_text}]
            claims = ClaimExtractor.extract_claims_from_pages(pages_data)
            summary = ClaimExtractor.summarize_extraction("Direct_Text_Input.txt", pasted_text, pages_data, claims)
            st.session_state.doc_summary = summary
            st.session_state.claims = claims
            st.session_state.raw_text = pasted_text
            st.session_state.report = None
            st.rerun()
        else:
            st.warning("Please paste some text first.")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Document Extraction Overview & Claims Preview
# ---------------------------------------------------------
if st.session_state.doc_summary and st.session_state.claims:
    summary: DocumentExtractionSummary = st.session_state.doc_summary
    claims = st.session_state.claims

    st.markdown(f"#### 📑 Ingested Document: `{summary.filename}`")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #818CF8;">{summary.total_pages}</div>
            <div class="metric-lbl">Pages Extracted</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #38BDF8;">{summary.total_sentences}</div>
            <div class="metric-lbl">Sentences Parsed</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #34D399;">{summary.total_claims_extracted}</div>
            <div class="metric-lbl">Verifiable Claims</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #C084FC;">{summary.total_characters:,}</div>
            <div class="metric-lbl">Characters</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔍 View Raw Extracted Document Text Preview"):
        st.text(st.session_state.raw_text[:2000] + ("..." if len(st.session_state.raw_text) > 2000 else ""))

    # Trigger Verification
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🚀 Execute Live Web Verification")
    st.write(
        "Cross-reference every quantitative metric, timeline, and assertion against live web knowledge sources to classify into "
        "**Verified**, **Inaccurate (with real fact correction)**, or **False**."
    )

    if st.button("🔍 Verify Claims Against Live Web Data", type="primary", use_container_width=True):
        verifier = FactCheckVerifier(gemini_api_key=gemini_key, tavily_api_key=tavily_key)
        
        progress_bar = st.progress(0.0)
        status_text = st.empty()

        def update_progress(current, total):
            pct = current / total
            progress_bar.progress(pct)
            status_text.text(f"Verifying claim {current} of {total} against live web sources...")

        with st.spinner("Querying live web engines, corroborating facts, and calculating Trust Score..."):
            report = verifier.generate_full_report(
                document_summary=summary,
                claims=claims,
                progress_callback=update_progress
            )
            st.session_state.report = report

        progress_bar.empty()
        status_text.empty()
        st.success("✅ Fact-Checking Complete!")
        st.rerun()

elif not st.session_state.doc_summary:
    st.info("👈 Upload a PDF above or choose one of the **1-Click Industry Presets** to run an audit.")

# ---------------------------------------------------------
# Verification Results Dashboard
# ---------------------------------------------------------
if st.session_state.report:
    report: FactCheckReport = st.session_state.report
    summary: DocumentExtractionSummary = st.session_state.doc_summary
    doc_hash = hashlib.sha256(st.session_state.raw_text.encode('utf-8')).hexdigest()[:16]

    st.markdown("---")
    st.markdown("## 📊 Executive Fact-Check Dashboard")
    st.caption(f"Verification Timestamp: {report.timestamp} | Engine: {report.engine_used} | Checksum: `SHA256:{doc_hash}`")

    # Executive Clearance Decision Banner
    if report.truth_score >= 80:
        badge_style = "clearance-glow-passed"
        decision_label = "🟢 PASSED: CLEAR FOR PUBLICATION"
        decision_desc = "Document shows high factual integrity. Minor or no discrepancies identified."
        score_color = "#34D399"
    elif report.truth_score >= 50:
        badge_style = "clearance-glow-conditional"
        decision_label = "🟡 CONDITIONAL: MANDATORY REVISION REQUIRED"
        decision_desc = f"Identified {report.inaccurate_count} outdated or shifted metrics. Review corrections before release."
        score_color = "#FBBF24"
    else:
        badge_style = "clearance-glow-rejected"
        decision_label = "🔴 REJECTED: CRITICAL COMPLIANCE / LEGAL RISK"
        decision_desc = f"Identified {report.false_count} contradicted and {report.inaccurate_count} inaccurate claims. Do not publish."
        score_color = "#F87171"

    st.markdown(f"""
    <div class="clearance-glow-banner {badge_style}">
        <div>
            <div style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.01em;">{decision_label}</div>
            <div style="font-size: 0.94rem; color: #CBD5E1; margin-top: 4px;">{decision_desc}</div>
        </div>
        <div style="text-align: right; min-width: 130px;">
            <div style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #94A3B8;">Trust Index</div>
            <div style="font-size: 2.6rem; font-weight: 900; color: {score_color}; line-height: 1;">{report.truth_score}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #E2E8F0;">{report.total_claims}</div>
            <div class="metric-lbl">Total Claims</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #34D399;">{report.verified_count}</div>
            <div class="metric-lbl">Verified (Accurate)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #FBBF24;">{report.inaccurate_count}</div>
            <div class="metric-lbl">Inaccurate (Shifted)</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card-glass">
            <div class="metric-num" style="color: #F87171;">{report.false_count}</div>
            <div class="metric-lbl">False (Contradicted)</div>
        </div>
        """, unsafe_allow_html=True)
    with m5:
        st.markdown(f"""
        <div class="metric-card-glass" style="border: 1.5px solid {score_color};">
            <div class="metric-num" style="color: {score_color};">{report.truth_score}%</div>
            <div class="metric-lbl">Overall Trust</div>
        </div>
        """, unsafe_allow_html=True)

    # Multi-Color Proportional Progress Bar
    if report.total_claims > 0:
        pct_v = int((report.verified_count / report.total_claims) * 100)
        pct_i = int((report.inaccurate_count / report.total_claims) * 100)
        pct_f = 100 - pct_v - pct_i
        st.markdown(f"""
        <div style="background-color: rgba(255,255,255,0.07); border-radius: 9999px; height: 12px; width: 100%; display: flex; overflow: hidden; margin-top: 14px; margin-bottom: 24px;">
            <div style="background-color: #10B981; width: {pct_v}%; height: 100%;" title="Verified: {pct_v}%"></div>
            <div style="background-color: #F59E0B; width: {pct_i}%; height: 100%;" title="Inaccurate: {pct_i}%"></div>
            <div style="background-color: #EF4444; width: {pct_f}%; height: 100%;" title="False: {pct_f}%"></div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Multi-View Exploration Tabs
    # ---------------------------------------------------------
    view_tab_claims, view_tab_redline, view_tab_charts, view_tab_telemetry = st.tabs([
        "📋 Claim-by-Claim Inspection",
        "📝 Document Redline (Track Changes)",
        "📊 Analytics & Visual Breakdown",
        "🏢 Enterprise ROI & Telemetry"
    ])

    # ---------------------------------------------------------
    # TAB 1: Claim-by-Claim Inspection (Cards + Filters)
    # ---------------------------------------------------------
    with view_tab_claims:
        col_filter_status, col_filter_cat, col_search = st.columns([1.5, 1.5, 2])

        with col_filter_status:
            status_options = ["All Statuses", "Verified", "Inaccurate", "False"]
            selected_status = st.selectbox("Filter by Status", status_options)

        with col_filter_cat:
            category_options = ["All Categories"] + [c.value for c in ClaimCategory]
            selected_cat = st.selectbox("Filter by Category", category_options)

        with col_search:
            search_query = st.text_input("Search Claims or Entities", placeholder="e.g., ChatGPT, Tesla, GDP, Google...")

        filtered_results = report.results
        if selected_status != "All Statuses":
            filtered_results = [r for r in filtered_results if r.status.value == selected_status]
        if selected_cat != "All Categories":
            filtered_results = [r for r in filtered_results if r.claim.category.value == selected_cat]
        if search_query.strip():
            q = search_query.lower()
            filtered_results = [
                r for r in filtered_results 
                if q in r.claim.claim_text.lower() 
                or (r.correction and q in r.correction.lower())
                or q in r.explanation.lower()
            ]

        st.caption(f"Showing **{len(filtered_results)}** of **{report.total_claims}** claims")

        for res in filtered_results:
            if res.status == ClaimStatus.VERIFIED:
                badge_html = f'<span class="badge-neon-verified">✅ VERIFIED</span>'
            elif res.status == ClaimStatus.INACCURATE:
                badge_html = f'<span class="badge-neon-inaccurate">⚠️ INACCURATE / SHIFTED</span>'
            else:
                badge_html = f'<span class="badge-neon-false">❌ FALSE / CONTRADICTED</span>'

            page_info = f"&middot; Page {res.claim.page_number}" if res.claim.page_number else ""
            category_info = f"&middot; {res.claim.category.value}"

            sources_html = ""
            if res.sources:
                sources_html = "<div style='margin-top: 10px;'><b>Sources:</b> "
                for s in res.sources:
                    sources_html += f'<a href="{s.url}" target="_blank" class="source-pill-dark">🔗 {s.title}</a>'
                sources_html += "</div>"
            else:
                sources_html = "<div style='margin-top: 8px; font-size: 0.8rem; color: #64748B;'><i>No external links cited.</i></div>"

            correction_html = ""
            if res.correction:
                correction_html = f"""
                <div class="correction-box-glow">
                    <b>💡 Verified Real Fact / Correction:</b><br/>{res.correction}
                </div>
                """

            st.markdown(f"""
            <div class="claim-card-dark">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div>{badge_html} <span style="font-size: 0.82rem; color: #94A3B8; margin-left: 8px;">ID: <code>{res.claim.id}</code> {page_info} {category_info}</span></div>
                </div>
                <div class="claim-text-title">"{res.claim.claim_text}"</div>
                {correction_html}
                <div class="evidence-box-dark">
                    <b>Verification Context:</b> {res.explanation}
                    <br/><span style="font-size: 0.85rem; color: #94A3B8;">{res.evidence_summary}</span>
                </div>
                {sources_html}
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 2: Visual Document Redline (Track Changes)
    # ---------------------------------------------------------
    with view_tab_redline:
        st.markdown("""
        **Executive Track-Changes Redline View:**  
        Visual representation of required edits: unverified or outdated assertions are crossed out, with live verified corrections injected directly beside them.
        """)
        
        redline_content = []
        for res in report.results:
            if res.status == ClaimStatus.INACCURATE and res.correction:
                item_html = (
                    f'<p><span class="redline-del">{res.claim.claim_text}</span> '
                    f'<span class="redline-ins">➔ Real Fact: {res.correction}</span> '
                    f'<span style="font-size:0.8rem; color:#94A3B8;">(Pg {res.claim.page_number or 1})</span></p>'
                )
            elif res.status == ClaimStatus.FALSE:
                item_html = (
                    f'<p><span class="redline-del">{res.claim.claim_text}</span> '
                    f'<span style="background-color: rgba(239, 68, 68, 0.25); color: #FCA5A5; font-weight:600; padding: 2px 8px; border-radius:6px; border: 1px solid rgba(239,68,68,0.5);">'
                    f'[CONTRADICTED: {res.explanation}]</span> '
                    f'<span style="font-size:0.8rem; color:#94A3B8;">(Pg {res.claim.page_number or 1})</span></p>'
                )
            else:
                item_html = (
                    f'<p><span class="redline-verified">✓ {res.claim.claim_text}</span> '
                    f'<span style="font-size:0.8rem; color:#34D399;">(Verified Accurate)</span></p>'
                )
            redline_content.append(item_html)

        redline_html = "".join(redline_content)
        st.markdown(f"""
        <div class="redline-canvas">
            <div style="font-weight: 700; font-size: 1.15rem; margin-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; color: #FFFFFF;">
                📄 Document Redline Markup: {summary.filename}
            </div>
            {redline_html}
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 3: Analytics & Visual Breakdown (Altair Charts)
    # ---------------------------------------------------------
    with view_tab_charts:
        st.markdown("### 📊 Visual Distribution & Credibility Analytics")
        
        chart_col1, chart_col2 = st.columns(2)

        # 1. Verification Status Donut Chart
        with chart_col1:
            st.markdown("##### Verification Status Ratio")
            status_df = pd.DataFrame([
                {"Status": "Verified", "Count": report.verified_count},
                {"Status": "Inaccurate", "Count": report.inaccurate_count},
                {"Status": "False", "Count": report.false_count}
            ])
            status_df = status_df[status_df["Count"] > 0]
            
            donut_chart = alt.Chart(status_df).mark_arc(innerRadius=65, stroke="#0A0E1A", strokeWidth=2).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(
                    field="Status",
                    type="nominal",
                    scale=alt.Scale(
                        domain=["Verified", "Inaccurate", "False"],
                        range=["#10B981", "#F59E0B", "#EF4444"]
                    ),
                    legend=alt.Legend(title="Status", orient="bottom")
                ),
                tooltip=["Status", "Count"]
            ).properties(
                height=280
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(donut_chart, use_container_width=True)

        # 2. Claim Category Distribution Bar Chart
        with chart_col2:
            st.markdown("##### Claims by Factual Category")
            cat_counts = {}
            for r in report.results:
                cat = r.claim.category.value
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
            
            cat_df = pd.DataFrame([{"Category": k, "Count": v} for k, v in cat_counts.items()])
            
            cat_chart = alt.Chart(cat_df).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6).encode(
                y=alt.Y("Category:N", sort="-x", title=None),
                x=alt.X("Count:Q", title="Number of Claims"),
                color=alt.value("#6366F1"),
                tooltip=["Category", "Count"]
            ).properties(
                height=280
            ).configure_view(
                strokeWidth=0
            )
            st.altair_chart(cat_chart, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 4: Enterprise ROI & Telemetry
    # ---------------------------------------------------------
    with view_tab_telemetry:
        st.markdown("### 🏢 Operational ROI & Risk Mitigation Telemetry")
        
        analyst_minutes_saved = max(15, report.total_claims * 15)
        hours_saved = round(analyst_minutes_saved / 60, 1)
        est_dollars_saved = int(hours_saved * 75)
        est_token_cost = "$0.004" if report.engine_used.startswith("Google") else "$0.000 (Open Source)"

        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown(f"""
            <div class="metric-card-glass">
                <div class="metric-num" style="color: #818CF8;">{hours_saved} hrs</div>
                <div class="metric-lbl">Human Review Saved</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">~${est_dollars_saved} in labor cost</div>
            </div>
            """, unsafe_allow_html=True)
        with t2:
            st.markdown(f"""
            <div class="metric-card-glass">
                <div class="metric-num" style="color: #34D399;">{est_token_cost}</div>
                <div class="metric-lbl">Est. Compute Cost</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">Sub-cent verification efficiency</div>
            </div>
            """, unsafe_allow_html=True)
        with t3:
            st.markdown(f"""
            <div class="metric-card-glass">
                <div class="metric-num" style="color: #C084FC;">{report.total_claims} / {summary.total_sentences}</div>
                <div class="metric-lbl">Signal Density Ratio</div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">Subjective fluff filtered out</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        #### 🛡️ Compliance & Governance Standards
        - **Regulatory Gatekeeping**: Eliminates unsubstantiated claims before distribution to regulatory authorities or prospective investors.
        - **Cryptographic Auditability**: Each verification embeds an immutable `SHA-256` checksum of the ingested document.
        - **Deterministic Evidence**: All verifications require consensus from live web endpoints or verified encyclopedic references.
        """)

    # ---------------------------------------------------------
    # Export Capabilities (Executive PDF, JSON, CSV, Markdown)
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📥 Export Audit & Compliance Deliverables")
    
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)

    # 1. Executive PDF Compliance Certificate
    with col_exp1:
        pdf_cert_bytes = generate_audit_certificate_pdf(report, summary, st.session_state.raw_text)
        st.download_button(
            label="📄 Executive PDF Certificate",
            data=pdf_cert_bytes,
            file_name=f"truth_layer_certificate_{summary.filename}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )

    # 2. JSON Export
    with col_exp2:
        json_data = report.model_dump_json(indent=2)
        st.download_button(
            label="Download Audit JSON",
            data=json_data,
            file_name=f"truth_layer_report_{summary.filename}.json",
            mime="application/json",
            use_container_width=True
        )

    # 3. CSV Export
    with col_exp3:
        csv_rows = []
        for r in report.results:
            csv_rows.append({
                "Claim ID": r.claim.id,
                "Page": r.claim.page_number,
                "Category": r.claim.category.value,
                "Original Claim": r.claim.claim_text,
                "Status": r.status.value,
                "Correction / Real Fact": r.correction or "N/A",
                "Explanation": r.explanation,
                "Top Source": r.sources[0].url if r.sources else "None"
            })
        df = pd.DataFrame(csv_rows)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Table (CSV)",
            data=csv_data,
            file_name=f"truth_layer_audit_{summary.filename}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 4. Markdown Audit Export
    with col_exp4:
        md_text = f"# Truth Layer Enterprise Audit Report: {summary.filename}\n"
        md_text += f"**Timestamp:** {report.timestamp} | **Trust Score:** {report.truth_score}% | **Integrity SHA256:** `{doc_hash}`\n\n"
        md_text += f"- Total Claims: {report.total_claims}\n"
        md_text += f"- Verified: {report.verified_count}\n"
        md_text += f"- Inaccurate: {report.inaccurate_count}\n"
        md_text += f"- False: {report.false_count}\n\n"
        md_text += "## Claims Detail\n\n"
        for r in report.results:
            md_text += f"### Claim `{r.claim.id}`: {r.status.value}\n"
            md_text += f"> {r.claim.claim_text}\n\n"
            if r.correction:
                md_text += f"**Correction / Real Fact:** {r.correction}\n\n"
            md_text += f"**Context:** {r.explanation}\n\n"
            if r.sources:
                md_text += f"**Source:** [{r.sources[0].title}]({r.sources[0].url})\n\n"
            md_text += "---\n\n"

        st.download_button(
            label="Download Markdown",
            data=md_text,
            file_name=f"truth_layer_summary_{summary.filename}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ About the Truth Layer Enterprise Pipeline"):
    st.markdown("""
    ### Architectural Highlights:
    1. **PDF Text Stream & Normalization**:
       `pypdf` extracts text page-by-page, resolves cross-line word hyphens, and maintains exact page references.
    2. **Verifiable Claim Boundary Extraction**:
       Isolates quantitative metrics (dates, percentages, financial valuations, headcount, and technical milestones) 
       from subjective marketing fluff ("disruptive innovation", "best-in-class synergy").
    3. **Multi-Engine Live Web Grounding**:
       Cross-references each factual assertion against live web consensus via **Google GenAI Search Grounding** (or keyless live encyclopedic endpoints).
    4. **Strict Three-Tier Classification**:
       - **Verified**: Confirmed by current live web data.
       - **Inaccurate**: Contains outdated statistics or shifted dates — **always includes an exact Real Fact correction**.
       - **False**: Contradicted by evidence or fabricated ("no evidence found").
    5. **Automated Trust Score & Executive Clearance**:
       Quantifies document reliability into an executive Trust Score and clear publication recommendation.
    """)
