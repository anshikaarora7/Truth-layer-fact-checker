"""
app.py
Enterprise-Grade Fact-Checking & Pre-Publication Risk Gatekeeper: Truth Layer.
Verifies factual claims inside uploaded PDF documents against live web data.
Built for deployment on Streamlit Community Cloud and Render.
"""

import os
import sys
import json
import hashlib
from datetime import datetime
import pandas as pd
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
# Custom Styling (Executive C-Suite & Enterprise UI Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Cards */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        text-align: center;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 4px;
        line-height: 1.1;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
    }
    
    /* Clearance Banner */
    .clearance-banner {
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .clearance-passed {
        background: #F0FDF4;
        border: 1.5px solid #22C55E;
        color: #15803D;
    }
    .clearance-conditional {
        background: #FFFBEB;
        border: 1.5px solid #F59E0B;
        color: #B45309;
    }
    .clearance-rejected {
        background: #FEF2F2;
        border: 1.5px solid #EF4444;
        color: #B91C1C;
    }

    /* Status Badges */
    .badge-verified {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #31C48D;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-inaccurate {
        background-color: #FEF08A;
        color: #854D0E;
        border: 1px solid #FACC15;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-false {
        background-color: #FDE8E8;
        color: #9B1C1C;
        border: 1px solid #F98080;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* Claim Result Cards */
    .claim-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.2s ease-in-out;
    }
    .claim-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border-color: #94A3B8;
    }
    .claim-quote {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1E293B;
        line-height: 1.5;
        margin-bottom: 10px;
    }
    .correction-box {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 0.95rem;
        color: #92400E;
    }
    .evidence-box {
        background-color: #F8FAFC;
        border-left: 4px solid #64748B;
        padding: 10px 14px;
        border-radius: 6px;
        margin-top: 8px;
        font-size: 0.9rem;
        color: #475569;
    }
    .source-pill {
        display: inline-block;
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 0.8rem;
        color: #1D4ED8;
        text-decoration: none;
        margin-right: 6px;
        margin-top: 6px;
    }
    .source-pill:hover {
        background: #DBEAFE;
    }

    /* Redline Track-Changes Styling */
    .redline-doc-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        line-height: 1.8;
        font-size: 1.02rem;
        color: #1E293B;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .redline-del {
        background-color: #FEE2E2;
        color: #991B1B;
        text-decoration: line-through;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 500;
    }
    .redline-ins {
        background-color: #DCFCE7;
        color: #166534;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        border-bottom: 2px solid #22C55E;
    }
    .redline-verified {
        background-color: #F0FDF4;
        color: #15803D;
        padding: 2px 4px;
        border-radius: 4px;
        border-bottom: 1px dashed #22C55E;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: Setup & Verification Controls
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("TruthLayer Enterprise")
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
        help="Enables Google Search Grounding with Gemini 2.0/2.5. If empty, the app runs on the built-in Live Web Engine (Wikipedia + DuckDuckGo)."
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
        st.info("🌐 Keyless Live Web Engine Active (Zero-Cost Mode)")

    st.markdown("---")
    st.subheader("🏢 Enterprise Use Cases")
    st.markdown("""
    - **Investor Decks & TAM Audits**
    - **Corporate Whitepapers & ESG**
    - **Pre-Press Marketing Compliance**
    - **Procurement & RFP Vetting**
    """)

    st.markdown("---")
    st.caption("Developed by Anshika Arora")
    st.caption("Production-Ready Architecture & CI/CD Validated")

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "doc_summary" not in st.session_state:
    st.session_state.doc_summary = None
if "claims" not in st.session_state:
    st.session_state.claims = []
if "report" not in st.session_state:
    st.session_state.report = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

# Ensure sample files exist
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
# Header & Hero Section
# ---------------------------------------------------------
st.title("🛡️ Truth Layer Enterprise: Automated Fact-Checking Agent")
st.markdown("""
Executive slide decks, investment memorandums, and corporate whitepapers frequently contain **outdated metrics, hallucinated milestones, and inflated statistics**.
**Truth Layer** automates the compliance lifecycle: extracting testable quantitative claims, cross-referencing against live web consensus, flagging liability risks with real-fact corrections, and producing C-suite audit certificates.
""")

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
        "Upload any PDF collateral (Marketing Deck, Whitepaper, Pitch Deck, Annual Report)", 
        type=["pdf"],
        help="Upload any PDF to extract and audit verifiable factual claims."
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
    st.markdown("Select an industry preset to test the agent with **1 click** (no PDF upload required):")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("""
        **1. 📊 Assessment Trap Document**  
        *Official CogCulture Benchmark*  
        Tests outdated dates, GDP stats, fake founding history, and agency size exaggeration.
        """)
        if st.button("Load Trap Document", use_container_width=True):
            _load_preset_file(trap_pdf_path, "trap_marketing_document.pdf")

    with col_p2:
        st.markdown("""
        **2. 🦄 Series B Pitch Deck**  
        *Venture Capital & Due Diligence*  
        Tests $15T AI market exaggeration, fabricated DAU growth velocity, and founder history.
        """)
        if st.button("Load Pitch Deck", use_container_width=True):
            _load_preset_file(pitch_pdf_path, "series_b_pitch_deck.pdf")

    with col_p3:
        st.markdown("""
        **3. 🌱 Corporate ESG Audit**  
        *Sustainability & Regulatory Claims*  
        Tests greenwashing claims, retroactive net-zero milestones, and emission stats.
        """)
        if st.button("Load ESG Report", use_container_width=True):
            _load_preset_file(esg_pdf_path, "corporate_esg_audit.pdf")

with tab_text:
    pasted_text = st.text_area(
        "Or paste raw copy, press releases, or claim statements directly:",
        height=180,
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

st.markdown("---")

# ---------------------------------------------------------
# Document Extraction Overview & Claims Preview
# ---------------------------------------------------------
if st.session_state.doc_summary and st.session_state.claims:
    summary: DocumentExtractionSummary = st.session_state.doc_summary
    claims = st.session_state.claims

    st.subheader(f"📑 Document Extraction Summary: `{summary.filename}`")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #2563EB;">{summary.total_pages}</div>
            <div class="metric-label">Pages Extracted</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #0284C7;">{summary.total_sentences}</div>
            <div class="metric-label">Sentences Parsed</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #16A34A;">{summary.total_claims_extracted}</div>
            <div class="metric-label">Verifiable Claims</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #9333EA;">{summary.total_characters:,}</div>
            <div class="metric-label">Characters</div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔍 View Raw Extracted Document Text Preview"):
        st.text(st.session_state.raw_text[:2000] + ("..." if len(st.session_state.raw_text) > 2000 else ""))

    # Trigger Verification
    st.markdown("### 🚀 Execute Live Web Verification")
    st.write(
        "Cross-reference every extracted metric, date, and figure against live web knowledge sources to classify into "
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
    st.info("👈 Upload a PDF above or pick one of the **1-Click Industry Presets** to test the agent immediately.")

# ---------------------------------------------------------
# Verification Results Dashboard
# ---------------------------------------------------------
if st.session_state.report:
    report: FactCheckReport = st.session_state.report
    summary: DocumentExtractionSummary = st.session_state.doc_summary
    doc_hash = hashlib.sha256(st.session_state.raw_text.encode('utf-8')).hexdigest()[:16]

    st.markdown("---")
    st.header("📊 Truth Layer Fact-Check Dashboard")
    st.caption(f"Verification Timestamp: {report.timestamp} | Engine: {report.engine_used} | Document Checksum: `SHA256:{doc_hash}`")

    # Executive Clearance Decision Banner
    if report.truth_score >= 80:
        badge_style = "clearance-passed"
        decision_label = "🟢 PASSED: CLEAR FOR PUBLICATION"
        decision_desc = "Document shows high factual integrity. Minor or no discrepancies identified."
    elif report.truth_score >= 50:
        badge_style = "clearance-conditional"
        decision_label = "🟡 CONDITIONAL: MANDATORY REVISION REQUIRED"
        decision_desc = f"Identified {report.inaccurate_count} outdated or shifted metrics. Review corrections before release."
    else:
        badge_style = "clearance-rejected"
        decision_label = "🔴 REJECTED: CRITICAL COMPLIANCE / LEGAL RISK"
        decision_desc = f"Identified {report.false_count} contradicted and {report.inaccurate_count} inaccurate claims. Do not publish."

    st.markdown(f"""
    <div class="clearance-banner {badge_style}">
        <div>
            <div style="font-size: 1.25rem; font-weight: 700;">{decision_label}</div>
            <div style="font-size: 0.92rem; margin-top: 4px;">{decision_desc}</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">Trust Index</div>
            <div style="font-size: 2.2rem; font-weight: 800;">{report.truth_score}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #334155;">{report.total_claims}</div>
            <div class="metric-label">Total Claims</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #16A34A;">{report.verified_count}</div>
            <div class="metric-label">Verified (Matches)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #D97706;">{report.inaccurate_count}</div>
            <div class="metric-label">Inaccurate (Shifted)</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value" style="color: #DC2626;">{report.false_count}</div>
            <div class="metric-label">False (Contradicted)</div>
        </div>
        """, unsafe_allow_html=True)
    with m5:
        score_color = "#16A34A" if report.truth_score >= 80 else ("#D97706" if report.truth_score >= 50 else "#DC2626")
        st.markdown(f"""
        <div class="metric-container" style="border: 2px solid {score_color};">
            <div class="metric-value" style="color: {score_color};">{report.truth_score}%</div>
            <div class="metric-label">Trust Score</div>
        </div>
        """, unsafe_allow_html=True)

    # Status Distribution Progress Bar
    if report.total_claims > 0:
        pct_v = int((report.verified_count / report.total_claims) * 100)
        pct_i = int((report.inaccurate_count / report.total_claims) * 100)
        pct_f = 100 - pct_v - pct_i
        st.markdown(f"""
        <div style="background-color: #E2E8F0; border-radius: 8px; height: 14px; width: 100%; display: flex; overflow: hidden; margin-top: 14px; margin-bottom: 24px;">
            <div style="background-color: #22C55E; width: {pct_v}%; height: 100%;" title="Verified: {pct_v}%"></div>
            <div style="background-color: #F59E0B; width: {pct_i}%; height: 100%;" title="Inaccurate: {pct_i}%"></div>
            <div style="background-color: #EF4444; width: {pct_f}%; height: 100%;" title="False: {pct_f}%"></div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Multi-View Results Exploration Tabs
    # ---------------------------------------------------------
    view_tab_claims, view_tab_redline, view_tab_telemetry = st.tabs([
        "📋 Claim-by-Claim Inspection",
        "📝 Document Redline (Track Changes)",
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

        # Filtered Results Processing
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

        st.markdown(f"**Showing {len(filtered_results)} of {report.total_claims} claims**")

        for res in filtered_results:
            if res.status == ClaimStatus.VERIFIED:
                badge_html = f'<span class="badge-verified">✅ VERIFIED</span>'
            elif res.status == ClaimStatus.INACCURATE:
                badge_html = f'<span class="badge-inaccurate">⚠️ INACCURATE / OUTDATED</span>'
            else:
                badge_html = f'<span class="badge-false">❌ FALSE / CONTRADICTED</span>'

            page_info = f"&middot; Page {res.claim.page_number}" if res.claim.page_number else ""
            category_info = f"&middot; {res.claim.category.value}"

            sources_html = ""
            if res.sources:
                sources_html = "<div style='margin-top: 8px;'><b>Sources:</b> "
                for s in res.sources:
                    sources_html += f'<a href="{s.url}" target="_blank" class="source-pill">🔗 {s.title}</a>'
                sources_html += "</div>"
            else:
                sources_html = "<div style='margin-top: 6px; font-size: 0.8rem; color: #94A3B8;'><i>No external sources cited.</i></div>"

            correction_html = ""
            if res.correction:
                correction_html = f"""
                <div class="correction-box">
                    <b>💡 Real Fact / Correction:</b><br/>{res.correction}
                </div>
                """

            st.markdown(f"""
            <div class="claim-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>{badge_html} <span style="font-size: 0.85rem; color: #64748B; margin-left: 8px;">ID: <code>{res.claim.id}</code> {page_info} {category_info}</span></div>
                </div>
                <div class="claim-quote">"{res.claim.claim_text}"</div>
                {correction_html}
                <div class="evidence-box">
                    <b>Verification Context & Evidence:</b> {res.explanation}
                    <br/><span style="font-size: 0.85rem; color: #64748B;">{res.evidence_summary}</span>
                </div>
                {sources_html}
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 2: Visual Document Redline (Track Changes)
    # ---------------------------------------------------------
    with view_tab_redline:
        st.markdown("""
        **Document Track-Changes Redline View:**  
        Inaccuracies and false claims are struck through with exact live corrections placed beside them:
        """)
        
        # Build redline markup
        redline_content = []
        for res in report.results:
            if res.status == ClaimStatus.INACCURATE and res.correction:
                item_html = (
                    f'<p><span class="redline-del">{res.claim.claim_text}</span> '
                    f'<span class="redline-ins">➔ Real Fact: {res.correction}</span> '
                    f'<span style="font-size:0.8rem; color:#64748B;">(Pg {res.claim.page_number or 1})</span></p>'
                )
            elif res.status == ClaimStatus.FALSE:
                item_html = (
                    f'<p><span class="redline-del">{res.claim.claim_text}</span> '
                    f'<span style="background-color: #FEE2E2; color: #DC2626; font-weight:600; padding: 2px 6px; border-radius:4px;">'
                    f'[CONTRADICTED: {res.explanation}]</span> '
                    f'<span style="font-size:0.8rem; color:#64748B;">(Pg {res.claim.page_number or 1})</span></p>'
                )
            else:
                item_html = (
                    f'<p><span class="redline-verified">✓ {res.claim.claim_text}</span> '
                    f'<span style="font-size:0.8rem; color:#15803D;">(Verified Accurate)</span></p>'
                )
            redline_content.append(item_html)

        redline_html = "".join(redline_content)
        st.markdown(f"""
        <div class="redline-doc-card">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 14px; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px;">
                📄 Redline Markup: {summary.filename}
            </div>
            {redline_html}
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # TAB 3: Enterprise ROI & Operations Telemetry
    # ---------------------------------------------------------
    with view_tab_telemetry:
        st.markdown("### 🏢 Executive Business Impact & Operational ROI")
        
        # Calculate ROI
        analyst_minutes_saved = max(15, report.total_claims * 15)
        hours_saved = round(analyst_minutes_saved / 60, 1)
        est_dollars_saved = int(hours_saved * 75)  # $75/hour compliance analyst cost
        est_token_cost = "$0.004" if report.engine_used.startswith("Google") else "$0.000 (Open Source)"

        t1, t2, t3 = st.columns(3)
        with t1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value" style="color: #2563EB;">{hours_saved} hrs</div>
                <div class="metric-label">Human Review Saved</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">~${est_dollars_saved} in labor cost</div>
            </div>
            """, unsafe_allow_html=True)
        with t2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value" style="color: #16A34A;">{est_token_cost}</div>
                <div class="metric-label">Est. Compute Cost</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Sub-cent verification efficiency</div>
            </div>
            """, unsafe_allow_html=True)
        with t3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value" style="color: #9333EA;">{report.total_claims} / {summary.total_sentences}</div>
                <div class="metric-label">Claim Density Ratio</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">Signal-to-marketing-fluff filter</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        #### 🛡️ Compliance & Legal Risk Mitigation
        - **Regulatory Exposure**: Eliminates unsubstantiated claims before distribution to regulatory bodies or investors.
        - **Brand Equity Protection**: Prevents embarrassing public retractions on social media or in press releases.
        - **Audit Reproducibility**: Generates an immutable cryptographic hash (`SHA-256`) of the verified document for internal compliance records.
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
# Footer & Assessment Rubric Information
# ---------------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ About the Truth Layer Enterprise Verification Pipeline"):
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
