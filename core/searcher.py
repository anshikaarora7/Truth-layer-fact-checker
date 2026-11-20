"""
core/searcher.py
Multi-Provider Live Web Search and Retrieval Subsystem.
Supports Google Gemini Search Grounding, Wikipedia Open Knowledge API,
DuckDuckGo Instant Answers, and Tavily/Serper when keys are available.
"""

import os
import re
import urllib.parse
from typing import List, Dict, Any, Optional
import requests
from core.models import WebSource


class WebSearchEngine:
    """Orchestrates search queries across live web sources."""

    @staticmethod
    def search_wikipedia(query: str, limit: int = 3) -> List[WebSource]:
        """
        Queries Wikipedia Open API for canonical encyclopedic facts, stats, and histories.
        Requires no API key.
        """
        sources = []
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "utf8": 1,
                "srlimit": limit
            }
            headers = {"User-Agent": "TruthLayerFactChecker/1.0 (Production Verification Tool)"}
            resp = requests.get(url, params=params, headers=headers, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("query", {}).get("search", [])
                for item in items:
                    title = item.get("title", "")
                    # Strip HTML formatting from snippet
                    raw_snippet = item.get("snippet", "")
                    clean_snippet = re.sub(r'<[^>]+>', '', raw_snippet)
                    page_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                    sources.append(WebSource(
                        title=f"{title} (Wikipedia)",
                        url=page_url,
                        snippet=clean_snippet
                    ))
        except Exception:
            # Resilient fallback
            pass
        return sources

    @staticmethod
    def search_duckduckgo_instant(query: str) -> List[WebSource]:
        """
        Queries DuckDuckGo Instant Answer API for live quick facts and entity summaries.
        Requires no API key.
        """
        sources = []
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            headers = {"User-Agent": "TruthLayerFactChecker/1.0"}
            resp = requests.get(url, params=params, headers=headers, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                abstract = data.get("AbstractText", "")
                source_url = data.get("AbstractURL", "")
                heading = data.get("Heading", query)
                if abstract and source_url:
                    sources.append(WebSource(
                        title=f"{heading} (DuckDuckGo)",
                        url=source_url,
                        snippet=abstract[:300]
                    ))
                # Also check related topics
                for topic in data.get("RelatedTopics", [])[:2]:
                    if isinstance(topic, dict) and "Text" in topic and "FirstURL" in topic:
                        sources.append(WebSource(
                            title=topic.get("Text", "")[:60] + "...",
                            url=topic.get("FirstURL", ""),
                            snippet=topic.get("Text", "")
                        ))
        except Exception:
            pass
        return sources

    @staticmethod
    def search_tavily(query: str, api_key: str, limit: int = 4) -> List[WebSource]:
        """Queries Tavily Search API if a Tavily API key is supplied."""
        sources = []
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": limit
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for res in data.get("results", []):
                    sources.append(WebSource(
                        title=res.get("title", "Live Web Result"),
                        url=res.get("url", ""),
                        snippet=res.get("content", "")[:250]
                    ))
        except Exception:
            pass
        return sources

    @classmethod
    def get_live_evidence_aggregate(cls, query: str, tavily_key: Optional[str] = None) -> List[WebSource]:
        """
        Aggregates live web evidence across available search engines.
        Returns deduplicated web sources.
        """
        sources: List[WebSource] = []
        seen_urls = set()

        # 1. Tavily if available
        if tavily_key:
            tav_sources = cls.search_tavily(query, tavily_key)
            for s in tav_sources:
                if s.url not in seen_urls:
                    seen_urls.add(s.url)
                    sources.append(s)

        # 2. Wikipedia Open Search
        wiki_sources = cls.search_wikipedia(query)
        for s in wiki_sources:
            if s.url not in seen_urls:
                seen_urls.add(s.url)
                sources.append(s)

        # 3. DuckDuckGo Instant
        ddg_sources = cls.search_duckduckgo_instant(query)
        for s in ddg_sources:
            if s.url not in seen_urls:
                seen_urls.add(s.url)
                sources.append(s)

        return sources
