"""
app.py
Production-Ready Fact-Checking Web Application: Truth Layer.
Verifies factual claims inside uploaded PDF documents against live web data.
Built for deployment on Streamlit Community Cloud and Render.
"""

import os
import sys
import json
import pandas as pd
import streamlit as st

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from core.models import Claim, ClaimStatus, ClaimCategory, FactCheckReport, DocumentExtractionSummary
from core.extractor import DocumentExtractor, ClaimExtractor
from core.verifier import FactCheckVerifier

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Truth Layer | Automated Fact-Checking Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Executive UI Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Metric Cards */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
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
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        transition: all 0.2s ease-in-out;
    }
    .claim-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #94A3B8;
    }
    .claim-quote {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1E293B;
        line-height: 1.5;
        margin-bottom: 12px;
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: Setup & Verification Controls
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("Truth Layer")
    st.caption("AI-Powered Document Fact-Checking")
    st.markdown("---")

    st.subheader("⚙️ Engine Configuration")
    
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
    st.subheader("🧪 Assessment Quick Test")
    st.write("One-click benchmark test using CogCulture's sample 'Trap Document'.")
    load_trap_clicked = st.button("📥 Load Official Trap Document", use_container_width=True)

    st.markdown("---")
    st.caption("Developed for CogCulture Product Management Assessment")
    st.caption("Status: Production-Ready & Streamlit Cloud Deployable")

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

# Handle "Load Trap Document" button
trap_pdf_path = os.path.join(os.path.dirname(__file__), "sample_data", "trap_marketing_document.pdf")
if load_trap_clicked:
    if os.path.exists(trap_pdf_path):
        with open(trap_pdf_path, "rb") as f:
            pdf_bytes = f.read()
        full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
        claims = ClaimExtractor.extract_claims_from_pages(pages_data)
        summary = ClaimExtractor.summarize_extraction("trap_marketing_document.pdf", full_text, pages_data, claims)
        st.session_state.doc_summary = summary
        st.session_state.claims = claims
        st.session_state.raw_text = full_text
        st.session_state.report = None
        st.success("Loaded 'Trap Document' containing intentional lies, outdated figures, and verifiable facts.")
    else:
        st.error("Trap document PDF not found. Please regenerate it.")

# ---------------------------------------------------------
# Header & Hero Section
# ---------------------------------------------------------
st.title("🛡️ Truth Layer: Automated Fact-Checking Agent")
st.markdown("""
Marketing collateral, executive pitches, and technical decks often harbor **outdated stats, hallucinated figures, or subtle misstatements**. 
The **Truth Layer** parses your PDF, isolates testable claims (dates, metrics, financials, statistics), cross-references them against live web data, and returns an audited fact-check report.
""")

# ---------------------------------------------------------
# Input Methods (Tabs)
# ---------------------------------------------------------
tab_upload, tab_presets, tab_text = st.tabs([
    "📄 Upload PDF Document", 
    "🧪 Test Fixtures (Trap Document)", 
    "✍️ Paste Direct Text"
])

with tab_upload:
    uploaded_file = st.file_uploader(
        "Choose a PDF file to analyze", 
        type=["pdf"],
        help="Upload any marketing brief, whitepaper, earnings deck, or report."
    )
    if uploaded_file is not None:
        if st.button("Extract Claims from Uploaded PDF", type="primary"):
            with st.spinner("Extracting text and identifying verifiable claims..."):
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
    st.markdown("""
    **Evaluation Benchmark Document:**
    The preset *Trap Document* is structured to test the agent's discrimination ability against the exact evaluation rubric:
    - **Intentional Fake Stats**: ChatGPT 100M users in 2021 (actually Jan 2023), India GDP $1.8T (actually >$3.9T in 2024).
    - **Blatant Hallucinations**: Google founded in 1975 by Bill Gates (contradicted by Microsoft history).
    - **Inflated Agency Figures**: CogCulture having 500,000 employees.
    - **Subjective Fluff**: Unverifiable marketing buzzwords (automatically filtered out).
    - **Accurate Anchors**: Apollo 11 Moon landing (1969) and Python release (1991).
    """)
    if st.button("⚡ Analyze Trap Document Now", key="btn_preset_analyze"):
        if os.path.exists(trap_pdf_path):
            with open(trap_pdf_path, "rb") as f:
                pdf_bytes = f.read()
            full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
            claims = ClaimExtractor.extract_claims_from_pages(pages_data)
            summary = ClaimExtractor.summarize_extraction("trap_marketing_document.pdf", full_text, pages_data, claims)
            st.session_state.doc_summary = summary
            st.session_state.claims = claims
            st.session_state.raw_text = full_text
            st.session_state.report = None
            st.rerun()

with tab_text:
    pasted_text = st.text_area(
        "Or paste raw marketing copy / claims directly:",
        height=180,
        placeholder="e.g., Tesla was founded in 2008 by Elon Musk. OpenAI ChatGPT reached 100 million active users in March 2021. Our vision represents an industry-leading paradigm shift..."
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

        with st.spinner("Querying live web engines, corroborating facts, and calculating Truth Score..."):
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
    st.info("👈 Upload a PDF above or click **'Load Official Trap Document'** in the sidebar to start fact-checking.")

# ---------------------------------------------------------
# Verification Results Dashboard
# ---------------------------------------------------------
if st.session_state.report:
    report: FactCheckReport = st.session_state.report

    st.markdown("---")
    st.header("📊 Truth Layer Fact-Check Dashboard")
    st.caption(f"Verification Timestamp: {report.timestamp} | Engine: {report.engine_used}")

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
            <div class="metric-label">Inaccurate (Outdated)</div>
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
            <div class="metric-label">Overall Trust Score</div>
        </div>
        """, unsafe_allow_html=True)

    # Trust Score Warning / Alert Banner
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if report.truth_score < 60:
        st.error(
            f"⚠️ **High Inaccuracy Warning:** The document has a Trust Score of **{report.truth_score}%**. "
            f"Found **{report.inaccurate_count}** outdated/inaccurate figures and **{report.false_count}** contradicted claims. "
            "See corrections below before publishing or relying on this document."
        )
    elif report.truth_score < 85:
        st.warning(
            f"🔔 **Moderate Accuracy:** Trust Score is **{report.truth_score}%**. Some claims contain outdated data."
        )
    else:
        st.success(f"✨ **High Integrity Document:** Trust Score is **{report.truth_score}%**. Claims are corroborated by live web data.")

    # Status Distribution Progress Bar
    if report.total_claims > 0:
        pct_v = int((report.verified_count / report.total_claims) * 100)
        pct_i = int((report.inaccurate_count / report.total_claims) * 100)
        pct_f = 100 - pct_v - pct_i
        st.markdown(f"""
        <div style="background-color: #E2E8F0; border-radius: 8px; height: 16px; width: 100%; display: flex; overflow: hidden; margin-top: 10px; margin-bottom: 24px;">
            <div style="background-color: #22C55E; width: {pct_v}%; height: 100%;" title="Verified: {pct_v}%"></div>
            <div style="background-color: #F59E0B; width: {pct_i}%; height: 100%;" title="Inaccurate: {pct_i}%"></div>
            <div style="background-color: #EF4444; width: {pct_f}%; height: 100%;" title="False: {pct_f}%"></div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # Filtering & Search Controls
    # ---------------------------------------------------------
    st.subheader("🔍 Claim Inspection & Real Fact Corrections")
    
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

    # ---------------------------------------------------------
    # Individual Claim Result Cards
    # ---------------------------------------------------------
    for res in filtered_results:
        # Determine badge CSS
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
                <b>💡 Correction / Real Fact:</b><br/>{res.correction}
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
    # Export Capabilities
    # ---------------------------------------------------------
    st.markdown("---")
    st.subheader("📥 Export Fact-Check Report")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)

    # 1. JSON Export
    with col_exp1:
        json_data = report.model_dump_json(indent=2)
        st.download_button(
            label="Download Complete Report (JSON)",
            data=json_data,
            file_name=f"truth_layer_report_{summary.filename}.json",
            mime="application/json",
            use_container_width=True
        )

    # 2. CSV Export
    with col_exp2:
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
            label="Download Claim Audit Table (CSV)",
            data=csv_data,
            file_name=f"truth_layer_audit_{summary.filename}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # 3. Markdown Audit Export
    with col_exp3:
        md_text = f"# Truth Layer Audit Report: {summary.filename}\n"
        md_text += f"**Timestamp:** {report.timestamp} | **Trust Score:** {report.truth_score}%\n\n"
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
            label="Download Audit Summary (Markdown)",
            data=md_text,
            file_name=f"truth_layer_summary_{summary.filename}.md",
            mime="text/markdown",
            use_container_width=True
        )

# ---------------------------------------------------------
# Footer & Assessment Rubric Information
# ---------------------------------------------------------
st.markdown("---")
with st.expander("ℹ️ About the Truth Layer Fact-Checking Pipeline"):
    st.markdown("""
    ### How It Works:
    1. **PDF Text Stream & Clean Normalization**:
       `pypdf` extracts text page-by-page, resolves cross-line word hyphens, and maintains exact page references.
    2. **Verifiable Claim Identification**:
       Distinguishes quantitative metrics (dates, percentages, financial valuations, headcount, and technical milestones) 
       from non-falsifiable marketing buzzwords ("disruptive innovation", "best-in-class synergy").
    3. **Live Web Grounding & Verification**:
       Cross-references each factual assertion against live web consensus via **Google GenAI Search Grounding** (or keyless live encyclopedic endpoints).
    4. **Strict Three-Tier Classification**:
       - **Verified**: Confirmed by current live web data.
       - **Inaccurate**: Contains outdated statistics or slightly shifted dates — **always includes a Real Fact correction**.
       - **False**: Contradicted by evidence or fabricated ("no evidence found").
    5. **Automated Trust Score**:
       Quantifies document reliability as an executive KPI.
    """)
