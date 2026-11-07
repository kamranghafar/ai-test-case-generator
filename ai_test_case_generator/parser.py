"""Input parsers — read requirements from text, file, or URL."""

from __future__ import annotations

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def read_requirement(source: str) -> str:
    """Read a requirement from a string, file path, or URL."""
    if source.startswith(("http://", "https://")):
        return _fetch_url(source)

    path = Path(source)
    if path.is_file():
        return path.read_text(encoding="utf-8")

    # Treat as raw text
    return source


def _fetch_url(url: str) -> str:
    """Fetch and extract text content from a URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; ai-test-case-generator/0.3.0; "
            "+https://github.com/kamranghafar/ai-test-case-generator)"
        )
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script/style noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    # Limit to 8000 chars to stay within reasonable token budgets
    return text[:8000]
