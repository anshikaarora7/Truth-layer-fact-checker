# 🛡️ Truth Layer Enterprise: Automated Fact-Checking & Pre-Publication Risk Gatekeeper

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://truth-layer-fact-checker.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/Deployment-Streamlit%20Cloud%20%7C%20Render-success.svg)]()
[![Code Architecture](https://img.shields.io/badge/Architecture-Pydantic%20%7C%20GenAI%20Grounding-purple.svg)]()

> **Acts as an objective "Truth Layer" that ingests PDF collateral, cross-references factual assertions against live web consensus, flags liabilities with verified real-fact corrections, renders visual redline track-changes, and generates cryptographic C-suite compliance certificates.**

Developed by **Anshika Arora** &middot; Official Submission for the **CogCulture Assessment: Part 1 (GEO Product Strategy) & Part 2 ("The Fact-Check Agent")**.

---

## 🎯 Submission Deliverables Quick Access

| Deliverable | Description | Format / Link |
| :--- | :--- | :--- |
| **🌐 Live Web Application** | Production-ready Streamlit Cloud web application | [truth-layer-fact-checker.streamlit.app](https://truth-layer-fact-checker.streamlit.app) |
| **📊 Part 1 Presentation (PPTX)** | 10-slide GEO AI Competitor Benchmarking & Monetization Roadmap | [geo_product_presentation.pptx](geo_product_presentation.pptx) |
| **📄 Part 1 Presentation (PDF)** | Executive slide deck in high-res landscape PDF | [geo_product_presentation.pdf](geo_product_presentation.pdf) |
| **🧪 Multi-Document Benchmark** | Full empirical results testing across 3 distinct PDF domains | [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md) |
| **🎬 30-Second Video Script** | Action-by-action walkthrough with timestamped voiceover | [screen_recording_script.md](screen_recording_script.md) |
| **💻 GitHub Repository** | Clean, modular Python codebase with automated tests | [github.com/anshikaarora7/Truth-layer-fact-checker](https://github.com/anshikaarora7/Truth-layer-fact-checker) |

---

## 📌 Part 1: Generative Engine Optimization (GEO) Product Strategy

### Product Concept:
An AI analytics platform that helps brands **measure, benchmark, and grow their visibility across major LLMs** (ChatGPT, Perplexity, Gemini, Claude).

### Core Feature: "Cross-LLM Share of Voice & Competitor Benchmarking Dashboard"
1. **Synthetic Prompt Simulation**: Evaluates hundreds of high-intent buying queries (e.g., *"What is the best CRM for mid-market fintech?"*).
2. **Citation Source Attribution Graph**: Pinpoints the exact publisher links, Reddit threads, and review sites LLMs cite as grounding evidence.
3. **Competitor Displacement Intelligence**: Discloses where competitors win over your brand and why.
4. **Automated GEO Playbook**: Reverse-engineers knowledge graph gaps (JSON-LD schema, Wikipedia entity anchors, PR targeting).

### Monetization & Product Roadmap (Summary):
- **Short-Term (Months 1–3)**: Multi-LLM crawling MVP (4 engines), weekly SoV shift alerts, closed beta with design partners.
- **Long-Term (Months 4–12)**: Autonomous content optimizer, voice AI search engine tracking (Apple Intelligence, Meta AI), predictive visibility model, white-label agency portal.
- **Pricing**: Starter ($299/mo), Professional ($899/mo), Enterprise & Agency Retainer ($2,499+/mo).

*(Complete details available in [geo_product_presentation.pptx](geo_product_presentation.pptx) and [geo_product_presentation.pdf](geo_product_presentation.pdf)).*

---

## 📌 Part 2: The "Fact-Check" Agent (Truth Layer)

### Measurable Enterprise Impact
| Operational Metric | Manual Legal/Compliance Review | Truth Layer Enterprise Agent |
| :--- | :--- | :--- |
| **Audit Turnaround Time** | 3.5 – 5.0 hours / document | **< 5 seconds / document** |
| **Verification Cost** | ~$250 – $375 / document ($75/hr analyst) | **<$0.005 / document (sub-cent API cost)** |
| **Hallucination Shield** | Vulnerable to reviewer oversight | **Deterministic grounding against live web consensus** |
| **Audit Reproducibility** | Subjective sticky notes | **SHA-256 cryptographic checksum + PDF Certificate** |

---

## 🏗️ Architecture & Pipeline Flow

```
[ Uploaded PDF / 1-Click Industry Preset ]
               │
               ▼
   [ Document Text Stream & Cleaner (pypdf) ]
   ├── Splits on periods & bullet newlines (•, -, 1.)
   └── Strips non-printable artifacts
               │
               ▼
   [ Verifiable Claim Extraction Engine ]
   ├── Reject: Subjective Marketing Fluff / Buzzwords
   └── Accept: Stats (%), Dates, Financials ($/€/₹), Tech Specs
               │
               ▼
   [ Multi-Engine Live Web Verification ]
   ├── Engine A: Google GenAI + Google Search Grounding (gemini-2.0 / gemini-2.5)
   ├── Engine B: Keyless Live Web Engine (Wikipedia Open Knowledge + DuckDuckGo)
   └── Engine C: Tavily / Serper External Search API
               │
               ▼
   [ Strict 3-Tier Classification & Correction ]
   ├── ✅ Verified: Corroborated by live web consensus
   ├── ⚠️ Inaccurate: Outdated stat -> Provided exact Real Fact Correction
   └── ❌ False: Contradicted / Fabricated / No Evidence Found
               │
               ▼
   [ Executive Streamlit Dashboard & Trust Score ]
   ├── Tab 1: Claim-by-Claim Inspection (Cards + Filters)
   ├── Tab 2: Document Redline (Word/Docs Track-Changes View)
   ├── Tab 3: Analytics & Visual Breakdown (Altair Donut & Bar Charts)
   └── Tab 4: Enterprise ROI & Telemetry
               │
               ▼
   [ Exportable C-Suite Compliance Deliverables ]
   ├── 📄 Executive PDF Compliance Certificate (ReportLab + SHA-256 Checksum)
   ├── 📊 Structured CSV Audit Table
   ├── 📦 Machine-Readable Audit JSON
   └── 📝 Markdown Summary
```

---

## 🧪 Multi-Document Testing & Benchmark Results

The agent was empirically tested across **3 distinct document domains** containing intentional errors, outdated figures, and verifiable anchors:

| Document | Scenario | Total Claims | Verified | Inaccurate | False | Trust Score |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`trap_marketing_document.pdf`** | Official CogCulture Trap Benchmark | 8 | 2 | 4 | 2 | **40.0%** (Rejected) |
| **`series_b_pitch_deck.pdf`** | Tech Startup Investment Memo | 5 | 2 | 1 | 2 | **46.0%** (Rejected) |
| **`corporate_esg_audit.pdf`** | Corporate ESG & Sustainability | 4 | 2 | 1 | 1 | **57.5%** (Conditional) |

> 📖 **Read the full granular claim-by-claim evaluation report with primary citations and context: [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md)**

---

## 🕵️‍♂️ How to Test the Deployed Application (Incognito Checklist)

To verify the application as an external evaluator before final submission:

1. **Open an Incognito / Private Window**:
   - Chrome / Edge: `Ctrl + Shift + N` (Windows) or `Cmd + Shift + N` (Mac).
2. **Navigate to the Live Link**:
   - `https://truth-layer-fact-checker.streamlit.app`
3. **Verify Zero-Credit / Keyless Functionality**:
   - Leave the Gemini API Key field blank in the sidebar (`🌐 Keyless Live Web Engine Active`).
   - Click the **"🧪 1-Click Industry Presets"** tab.
   - Click **"🚀 Load Trap Document"** ➔ click **"🔍 Verify Claims Against Live Web Data"**.
   - Confirm that all claims are classified, Trust Score is calculated, and corrections are visible.
4. **Test PDF File Upload**:
   - Click the **"📄 Upload PDF Document"** tab.
   - Upload any custom PDF file or one from the `sample_data/` folder.
   - Click **"Extract Claims from Uploaded PDF"** to confirm the extraction summary metrics appear.
5. **Inspect Executive Redline & Deliverables**:
   - Switch to the **"📝 Document Redline (Track Changes)"** tab to view Word-style strikethroughs and corrections.
   - Click **"📄 Executive PDF Certificate"** under the export section to download the compliance certificate.

---

## 📂 Repository Structure

```
truth-layer-fact-checker/
│
├── app.py                      # Main Streamlit web application & executive UI
├── requirements.txt            # Streamlit Cloud & Render ready dependencies
├── .env.example                # Clean template for API keys & environment variables
├── BENCHMARK_RESULTS.md        # Comprehensive multi-document empirical audit results
├── screen_recording_script.md  # 30-second walkthrough recording script
├── geo_product_presentation.pptx # Part 1: Official GEO Strategy Presentation (PowerPoint)
├── geo_product_presentation.pdf  # Part 1: Official GEO Strategy Presentation (PDF)
│
├── core/
│   ├── __init__.py             # Core package initialization
│   ├── models.py               # Pydantic schemas (Claim, ClaimStatus, VerificationResult, Report)
│   ├── extractor.py            # PDF parsing (pypdf) & verifiable claim boundary detection
│   ├── searcher.py             # Multi-engine search manager (Google Grounding, Wikipedia, DuckDuckGo, Tavily)
│   ├── verifier.py             # Claim cross-referencing, verdict classification & correction engine
│   ├── pdf_exporter.py         # ReportLab executive PDF compliance certificate generator
│   └── sample_generator.py     # Multi-domain PDF generator (Trap Doc, Pitch Deck, ESG Audit)
│
├── sample_data/
│   ├── trap_marketing_document.pdf  # CogCulture assessment trap document
│   ├── series_b_pitch_deck.pdf      # Venture due-diligence sample
│   └── corporate_esg_audit.pdf      # Sustainability compliance sample
│
└── tests/
    ├── test_extraction.py      # Unit tests for text cleaning and claim isolation
    └── test_verification.py    # Unit tests for classification and verdict rules
```

---

## 🚀 Local Quickstart

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/anshikaarora7/Truth-layer-fact-checker.git
cd Truth-layer-fact-checker
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
python -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### 4. Run the Automated Test Suite
```bash
python -m unittest discover tests
```

---

## 📜 Evaluation Criteria Checklist (CogCulture Rubric)

- [x] **Part 1 (GEO Product Feature)**: Detailed feature design comparing market tools with a 3-month & 1-year product and monetization roadmap.
- [x] **Part 1 Submission (PPT/PDF)**: 10 concise, visually compelling slides formatted in both native `.pptx` and `.pdf`.
- [x] **PDF Document Parsing**: Clean text stream parsing with page tracking via `pypdf`, bullet newline splitting, and formatting preservation.
- [x] **Verifiable Claim Extraction**: Isolates dates, statistics, metrics, and financials while ignoring non-falsifiable marketing buzzwords.
- [x] **Live Web Cross-Referencing**: Dual-engine verification via Google Search Grounding and keyless open-source search (Wikipedia/DuckDuckGo).
- [x] **Strict 3-Status Classification**: Categorizes claims into Verified, Inaccurate, or False.
- [x] **Mandatory Real Fact Corrections**: Every inaccurate claim includes the verified correct figure and primary source citation.
- [x] **Multi-Document Empirical Testing**: Comprehensive multi-doc benchmark report published in `BENCHMARK_RESULTS.md`.
- [x] **Executive Deliverables**: Visual document redline, interactive Altair charts, and cryptographic SHA-256 PDF compliance certificate.
- [x] **Live Cloud Deployment**: Deployed on Streamlit Community Cloud with incognito testing validation.
- [x] **Demo Video Script**: 30-second screen recording script ready for submission in case of API credit exhaustion.
