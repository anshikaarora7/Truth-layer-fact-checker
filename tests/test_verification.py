"""
tests/test_verification.py
Tests the verification pipeline on intentional traps, outdated stats, and accurate facts.
"""

import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import Claim, ClaimCategory, ClaimStatus
from core.verifier import FactCheckVerifier


class TestVerification(unittest.TestCase):

    def setUp(self):
        self.verifier = FactCheckVerifier()

    def test_inaccurate_outdated_stat_flagging(self):
        # Trap 1: ChatGPT 100M users in 2021 (actually Jan 2023)
        c1 = Claim(
            id="test_001",
            claim_text="OpenAI ChatGPT reached 100 million active users in March 2021.",
            category=ClaimCategory.STATISTIC
        )
        res1 = self.verifier.verify_claim(c1)
        self.assertEqual(res1.status, ClaimStatus.INACCURATE)
        self.assertIsNotNone(res1.correction)
        self.assertIn("January 2023", res1.correction)

    def test_inaccurate_founding_year(self):
        # Trap 2: Tesla founded in 2008 by Elon Musk (actually 2003 by Eberhard & Tarpenning)
        c2 = Claim(
            id="test_002",
            claim_text="Tesla Inc. was founded in 2008 by Elon Musk in San Carlos, California.",
            category=ClaimCategory.DATE
        )
        res2 = self.verifier.verify_claim(c2)
        self.assertEqual(res2.status, ClaimStatus.INACCURATE)
        self.assertIsNotNone(res2.correction)
        self.assertIn("2003", res2.correction)

    def test_inaccurate_gdp(self):
        # Trap 3: India GDP $1.8 Trillion (outdated, now >$3.9T)
        c3 = Claim(
            id="test_003",
            claim_text="In global economic evaluations, India's nominal GDP stands at approximately $1.8 Trillion.",
            category=ClaimCategory.FINANCIAL
        )
        res3 = self.verifier.verify_claim(c3)
        self.assertEqual(res3.status, ClaimStatus.INACCURATE)
        self.assertIsNotNone(res3.correction)
        self.assertIn("3.9", res3.correction)

    def test_false_fabricated_claim(self):
        # Trap 4: Google founded in 1975 by Bill Gates (False)
        c4 = Claim(
            id="test_004",
            claim_text="Google was founded in 1975 by Bill Gates in Seattle, Washington.",
            category=ClaimCategory.DATE
        )
        res4 = self.verifier.verify_claim(c4)
        self.assertEqual(res4.status, ClaimStatus.FALSE)
        self.assertIn("Microsoft", res4.explanation)

    def test_verified_fact(self):
        # True fact: Apollo 11 moon landing July 20, 1969
        c5 = Claim(
            id="test_005",
            claim_text="The Apollo 11 mission landed astronauts on the Moon on July 20, 1969.",
            category=ClaimCategory.DATE
        )
        res5 = self.verifier.verify_claim(c5)
        self.assertEqual(res5.status, ClaimStatus.VERIFIED)


if __name__ == "__main__":
    unittest.main()
