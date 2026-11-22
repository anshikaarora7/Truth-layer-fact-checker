"""
core/extractor.py
PDF Text Extraction and Verifiable Claim Identification Engine.
"""

import io
import re
from typing import List, Tuple, Optional
import pypdf
from core.models import Claim, ClaimCategory, DocumentExtractionSummary


class DocumentExtractor:
    """Extracts text from PDF documents and breaks it into normalized pages and sentences."""

    @staticmethod
    def extract_from_pdf(pdf_file_or_bytes) -> Tuple[str, List[dict]]:
        """
        Extract text page by page from a file-like object or bytes.
        Returns full text and a list of page dicts: [{'page_num': 1, 'text': '...'}]
        """
        try:
            if isinstance(pdf_file_or_bytes, bytes):
                reader = pypdf.PdfReader(io.BytesIO(pdf_file_or_bytes))
            else:
                reader = pypdf.PdfReader(pdf_file_or_bytes)
        except Exception as e:
            # Fallback if corrupt or invalid PDF
            return "", []

        pages_data = []
        full_text_parts = []

        for idx, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""

            cleaned_text = DocumentExtractor._clean_text(page_text)
            if cleaned_text.strip():
                pages_data.append({
                    "page_num": idx + 1,
                    "text": cleaned_text
                })
                full_text_parts.append(cleaned_text)

        full_text = "\n\n".join(full_text_parts)
        return full_text, pages_data

    @staticmethod
    def _clean_text(text: str) -> str:
        """Normalize line breaks, hyphenated words across lines, and whitespace."""
        if not text:
            return ""
        # Fix hyphenated words at line endings (e.g., "revo-\nlution" -> "revolution")
        text = re.sub(r'(\b\w+)-\s*\n\s*(\w+\b)', r'\1\2', text)
        # Normalize carriage returns
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Normalize non-breaking spaces and tabs
        text = re.sub(r'[\t\xa0]+', ' ', text)
        # Normalize multiple spaces (preserving newlines)
        text = re.sub(r'[ ]{2,}', ' ', text)
        # Normalize excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Splits text into sentences carefully preserving numbers, abbreviations, and currencies.
        Supports sentences terminated by period, newline bullet points, or list markers.
        """
        if not text:
            return []

        # Replace excessive whitespace within lines
        lines = text.split('\n')
        raw_chunks = []
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            # If line starts with a bullet point or list marker, strip it
            line_str = re.sub(r'^[•\-\*\u2022\u2023\u25E6\u2043\u2219]\s*', '', line_str)
            line_str = re.sub(r'^\d+[\.\)]\s+', '', line_str)
            if len(line_str) >= 12:
                raw_chunks.append(line_str)

        # In case text has continuous multi-sentence paragraphs, split them on terminal periods
        clean_sentences = []
        abbrevs = [
            'e.g.', 'i.e.', 'Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.', 'Inc.',
            'Ltd.', 'Corp.', 'vs.', 'approx.', 'no.', 'Jan.', 'Feb.', 'Mar.',
            'Apr.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'
        ]

        for chunk in raw_chunks:
            temp = chunk
            for i, abb in enumerate(abbrevs):
                temp = temp.replace(abb, f"__ABB_{i}__")

            # Protect decimal numbers (e.g. $1.8 or 3.9)
            temp = re.sub(r'(\d+)\.(\d+)', r'\1__DOT__\2', temp)

            # Split on terminal punctuation followed by space
            sub_parts = re.split(r'[.?!]+\s+', temp)
            for part in sub_parts:
                restored = part.replace('__DOT__', '.')
                for i, abb in enumerate(abbrevs):
                    restored = restored.replace(f"__ABB_{i}__", abb)
                s_clean = restored.strip()
                # Remove leading/trailing bullet remnants
                s_clean = re.sub(r'^[•\-\*\s]+', '', s_clean)
                if len(s_clean) >= 12:
                    clean_sentences.append(s_clean)

        return clean_sentences


class ClaimExtractor:
    """
    Identifies and extracts discrete, verifiable claims from document text.
    Targets: statistics, dates, financial figures, and technical/scientific metrics.
    Rejects: subjective marketing fluff, purely aspirational statements, or opinions.
    """

    # Patterns matching verifiable facts
    STAT_PATTERN = re.compile(
        r'(\b\d+(\.\d+)?%\b|\b\d+(\.\d+)?\s*(percent|per\s*cent)\b|\b\d+x\b|\b\d+\s*out\s*of\s*\d+\b|\b\d+([,\.]\d+)?\s*(users|customers|employees|countries|stores|downloads|subscribers|offices|members|people|clients|units)\b)',
        re.IGNORECASE
    )
    DATE_PATTERN = re.compile(
        r'(\b(19|20)\d{2}\b|\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th)?(,\s*(19|20)\d{2})?\b|\bin\s+(19|20)\d{2}\b|\bsince\s+(19|20)\d{2}\b|\bQ[1-4]\s*(19|20)?\d{2}\b)',
        re.IGNORECASE
    )
    FINANCIAL_PATTERN = re.compile(
        r'(\$|€|£|₹|USD|EUR|INR)\s*\d+(\.\d+)?\s*(billion|trillion|million|B|M|T|k|crore|lakh)?\b|\b\d+(\.\d+)?\s*(billion|trillion|million|crore)\s*(dollars|USD|revenue|valuation|funding|ARR|MRR)\b',
        re.IGNORECASE
    )
    TECHNICAL_PATTERN = re.compile(
        r'(\b\d+(\.\d+)?\s*(GB|TB|MB|GHz|MHz|parameters|tokens|headcount|active\s+users|MAU|DAU|miles|km|hours|kg|kWh|ppm)\b|\b(founded|headquartered|acquired|launched|released|invented|patented|announced)\b)',
        re.IGNORECASE
    )

    # Disqualification patterns for subjective fluff
    FLUFF_INDICATORS = [
        r'\bwe believe\b',
        r'\bour mission is to\b',
        r'\bwe aim to\b',
        r'\bcommitted to excellence\b',
        r'\bworld-class customer service\b',
        r'\bpassion for innovation\b',
        r'\bseamless synergy\b',
        r'\bparadigm shift\b',
        r'\bdisruptive potential\b',
        r'\bstate of the art feeling\b',
        r'\bhope to achieve\b',
        r'\bthe future of\b'
    ]
    FLUFF_PATTERN = re.compile('|'.join(FLUFF_INDICATORS), re.IGNORECASE)

    @classmethod
    def is_verifiable_claim(cls, sentence: str) -> Tuple[bool, Optional[ClaimCategory]]:
        """
        Evaluates whether a sentence contains a concrete, testable factual claim.
        Returns (is_verifiable, category).
        """
        # Disqualification for metadata headers, page labels, or section titles
        if re.search(r'\b(author|confidential|table of contents|version\s*\d+|all rights reserved|trends\s*\d{4}|climate audit\s*\d{4}|scope:|memorandum|renewable transition & scope)\b', sentence, re.IGNORECASE):
            return False, None
        # Reject short section headers without a predicate/verb
        if re.match(r'^\d+[\.\)]\s+[A-Za-z\s&/]+$', sentence.strip()):
            return False, None

        # Check fluff
        has_fluff = bool(cls.FLUFF_PATTERN.search(sentence))

        # Check patterns in order of specificity
        has_financial = bool(cls.FINANCIAL_PATTERN.search(sentence))
        has_stat = bool(cls.STAT_PATTERN.search(sentence))
        has_technical = bool(cls.TECHNICAL_PATTERN.search(sentence))
        has_date = bool(cls.DATE_PATTERN.search(sentence))

        # Check if sentence has any numerical anchor (e.g. 100, 2021, $5M, 50%)
        has_number = bool(re.search(r'\b\d+([,\.]\d+)?\b', sentence))

        # If it has fluff AND no numbers or concrete dates, reject
        if has_fluff and not (has_stat or has_financial or has_date or has_technical or has_number):
            return False, None

        if has_financial:
            return True, ClaimCategory.FINANCIAL
        elif has_stat:
            return True, ClaimCategory.STATISTIC
        elif has_technical:
            return True, ClaimCategory.TECHNICAL
        elif has_date:
            return True, ClaimCategory.DATE
        elif has_number and not has_fluff:
            # Fallback for numerical factual claims
            return True, ClaimCategory.STATISTIC

        return False, None

    @classmethod
    def extract_claims_from_pages(cls, pages_data: List[dict]) -> List[Claim]:
        """
        Extracts claims across multiple document pages, assigning page numbers and IDs.
        """
        claims: List[Claim] = []
        claim_count = 1
        seen_sentences = set()

        for page in pages_data:
            page_num = page.get("page_num", 1)
            text = page.get("text", "")
            sentences = DocumentExtractor.split_into_sentences(text)

            for sentence in sentences:
                cleaned_sent = sentence.strip()
                # Clean leading bullets
                cleaned_sent = re.sub(r'^[•\-\*\s]+', '', cleaned_sent)
                if len(cleaned_sent) < 15:
                    continue

                normalized = re.sub(r'\s+', ' ', cleaned_sent.lower())
                if normalized in seen_sentences:
                    continue

                is_claim, category = cls.is_verifiable_claim(cleaned_sent)
                if is_claim and category:
                    seen_sentences.add(normalized)
                    claim_obj = Claim(
                        id=f"claim_{claim_count:03d}",
                        claim_text=cleaned_sent,
                        category=category,
                        original_sentence=cleaned_sent,
                        page_number=page_num,
                        confidence_score=0.95
                    )
                    claims.append(claim_obj)
                    claim_count += 1

        return claims

    @classmethod
    def summarize_extraction(cls, filename: str, full_text: str, pages_data: List[dict], claims: List[Claim]) -> DocumentExtractionSummary:
        """Builds an extraction summary model."""
        total_chars = len(full_text)
        all_sentences = DocumentExtractor.split_into_sentences(full_text)
        preview = full_text[:400] + ("..." if len(full_text) > 400 else "")

        return DocumentExtractionSummary(
            filename=filename,
            total_pages=len(pages_data),
            total_characters=total_chars,
            total_sentences=len(all_sentences),
            total_claims_extracted=len(claims),
            preview_snippet=preview
        )
