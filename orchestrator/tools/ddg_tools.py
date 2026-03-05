import requests
from dataclasses import dataclass
from typing import List
from ddgs import DDGS
from bs4 import BeautifulSoup


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


def ddg_search(query: str, num_results: int = 5) -> List[SearchResult]:
    """
    Perform a DuckDuckGo search.

    Args:
        query: Search query.
        num_results: Maximum number of results.

    Returns:
        List of SearchResult objects.
    """
    results: List[SearchResult] = []

    with DDGS() as ddgs:
        for r in ddgs.text(query=query, max_results=num_results):
            results.append(
                SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    snippet=r.get("body", ""),
                )
            )

    return results


def fetch_web_content(url: str, timeout: int = 10) -> str:
    """
    Fetch and extract readable text from a webpage.

    Args:
        url: Target webpage.
        timeout: Request timeout.

    Returns:
        Extracted text content.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AI-Agent/1.0)"
        }

        with requests.Session() as session:
            response = session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text

    except requests.exceptions.RequestException as e:
        return f"[ERROR] Failed to fetch {url}: {e}"
