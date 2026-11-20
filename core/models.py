"""
core/models.py
Data structures and domain models for the Truth Layer Fact-Checking Agent.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ClaimStatus(str, Enum):
    """The three exact claim classifications required by the Truth Layer specification."""
    VERIFIED = "Verified"
    INACCURATE = "Inaccurate"
    FALSE = "False"


class ClaimCategory(str, Enum):
    """Categories of verifiable factual claims."""
    STATISTIC = "Statistic"
    DATE = "Date / Timeline"
    FINANCIAL = "Financial Figure"
    TECHNICAL = "Technical / Metric"
    GENERAL_FACT = "General Fact"


class WebSource(BaseModel):
    """A web citation or evidence source corroborating or refuting a claim."""
    title: str
    url: str
    snippet: Optional[str] = None


class Claim(BaseModel):
    """A discrete verifiable factual claim extracted from a document."""
    id: str
    claim_text: str
    category: ClaimCategory = ClaimCategory.GENERAL_FACT
    original_sentence: Optional[str] = None
    page_number: Optional[int] = None
    confidence_score: float = 1.0


class VerificationResult(BaseModel):
    """Verification analysis and classification for a single claim."""
    claim: Claim
    status: ClaimStatus
    explanation: str
    correction: Optional[str] = None  # Mandatory for Inaccurate; Real Fact details
    evidence_summary: str
    sources: List[WebSource] = Field(default_factory=list)
    search_queries_used: List[str] = Field(default_factory=list)


class DocumentExtractionSummary(BaseModel):
    """Metadata about the parsed document."""
    filename: str
    total_pages: int
    total_characters: int
    total_sentences: int
    total_claims_extracted: int
    preview_snippet: str


class FactCheckReport(BaseModel):
    """Complete fact-checking report for an uploaded document."""
    document_summary: DocumentExtractionSummary
    results: List[VerificationResult]
    total_claims: int
    verified_count: int
    inaccurate_count: int
    false_count: int
    truth_score: float  # Percentage score 0 - 100
    timestamp: str
    engine_used: str
