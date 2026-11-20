"""
tests/test_extraction.py
Tests PDF loading, text extraction, and verifiable claim identification.
"""

import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.extractor import DocumentExtractor, ClaimExtractor
from core.models import ClaimCategory



class TestExtraction(unittest.TestCase):

    def setUp(self):
        self.sample_pdf = os.path.join(
            os.path.dirname(__file__), "..", "sample_data", "trap_marketing_document.pdf"
        )
        self.assertTrue(os.path.exists(self.sample_pdf), "Trap sample PDF must exist")

    def test_pdf_extraction(self):
        with open(self.sample_pdf, "rb") as f:
            pdf_bytes = f.read()

        full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
        self.assertGreater(len(pages_data), 0)
        self.assertIn("Technology Trends", full_text)
        self.assertIn("ChatGPT", full_text)

    def test_claim_filtering_vs_fluff(self):
        # Fluff sentence should be rejected
        fluff = "Our digital ecosystem delivers unprecedented paradigm-shifting synergy to hyper-growth enterprises."
        is_claim, cat = ClaimExtractor.is_verifiable_claim(fluff)
        self.assertFalse(is_claim, "Pure subjective fluff must be rejected")

        # Fluff with 'we believe'
        fluff2 = "We believe our team has the most extraordinary passion for driving world-class innovation."
        is_claim2, cat2 = ClaimExtractor.is_verifiable_claim(fluff2)
        self.assertFalse(is_claim2, "Aspirational claims without numbers must be rejected")

        # Concrete statistics should be accepted
        stat_claim = "OpenAI ChatGPT reached 100 million active users in March 2021."
        is_claim3, cat3 = ClaimExtractor.is_verifiable_claim(stat_claim)
        self.assertTrue(is_claim3)
        self.assertIn(cat3, [ClaimCategory.STATISTIC, ClaimCategory.TECHNICAL, ClaimCategory.DATE])

        # Financial figure claim
        fin_claim = "India's nominal GDP stands at approximately $1.8 Trillion."
        is_claim4, cat4 = ClaimExtractor.is_verifiable_claim(fin_claim)
        self.assertTrue(is_claim4)
        self.assertEqual(cat4, ClaimCategory.FINANCIAL)

    def test_trap_pdf_full_pipeline(self):
        with open(self.sample_pdf, "rb") as f:
            pdf_bytes = f.read()

        full_text, pages_data = DocumentExtractor.extract_from_pdf(pdf_bytes)
        claims = ClaimExtractor.extract_claims_from_pages(pages_data)

        # Must have extracted the key test claims
        claim_texts = [c.claim_text for c in claims]
        self.assertTrue(any("ChatGPT" in t for t in claim_texts))
        self.assertTrue(any("Tesla" in t for t in claim_texts))
        self.assertTrue(any("Google" in t for t in claim_texts))
        self.assertTrue(any("GDP" in t or "$1.8" in t for t in claim_texts))
        self.assertTrue(any("Apollo 11" in t for t in claim_texts))
        self.assertTrue(any("Python" in t for t in claim_texts))


if __name__ == "__main__":
    unittest.main()
