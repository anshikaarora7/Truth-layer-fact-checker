"""
core package initialization
"""
from core.models import Claim, ClaimStatus, ClaimCategory, VerificationResult, FactCheckReport
from core.extractor import DocumentExtractor, ClaimExtractor
from core.searcher import WebSearchEngine
from core.verifier import FactCheckVerifier
