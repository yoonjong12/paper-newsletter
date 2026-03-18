"""Semantic Scholar API client — batch enrichment and recommendations."""

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

import httpx

BASE_URL = "https://api.semanticscholar.org/graph/v1"
RECOMMEND_URL = "https://api.semanticscholar.org/recommendations/v1/papers/forpaper"


@dataclass
class RelatedPaper:
    title: str
    citation_count: int
    year: int | None
    url: str


@dataclass
class Enrichment:
    citation_count: int
    tldr: str | None
    influential_citation_count: int
    affiliations: list[str] = field(default_factory=list)
    venue: str | None = None
    related_papers: list[RelatedPaper] = field(default_factory=list)


def _headers(api_key: str | None) -> dict[str, str]:
    if api_key:
        return {"x-api-key": api_key}
    return {}


def _request_with_backoff(url: str, headers: dict[str, str], method: str = "GET", json_body: dict | None = None) -> httpx.Response:
    """Make an HTTP request with exponential backoff on 429 responses."""
    delays = [3, 6, 12, 24]
    with httpx.Client(timeout=30) as client:
        for delay in delays:
            if method == "POST":
                resp = client.post(url, headers=headers, json=json_body)
            else:
                resp = client.get(url, headers=headers)
            if resp.status_code != 429:
                return resp
            print(f"    429 rate limited, waiting {delay}s...")
            time.sleep(delay)
        if method == "POST":
            return client.post(url, headers=headers, json=json_body)
        return client.get(url, headers=headers)


def _extract_affiliations(authors: list[dict]) -> list[str]:
    """Extract unique affiliations from first and last (corresponding) author."""
    seen: set[str] = set()
    result: list[str] = []
    for author in (authors[:1] + authors[-1:]):
        for aff in author.get("affiliations") or []:
            if aff and aff not in seen:
                seen.add(aff)
                result.append(aff)
    return result


def enrich_batch(arxiv_ids: list[str], api_key: str | None = None) -> dict[str, Enrichment]:
    """Batch-enrich papers via S2 POST /paper/batch endpoint, then fetch recommendations in parallel."""
    if not arxiv_ids:
        return {}

    headers = _headers(api_key)
    paper_fields = "paperId,externalIds,citationCount,influentialCitationCount,tldr,authors,venue"
    batch_url = f"{BASE_URL}/paper/batch?fields={paper_fields}"

    s2_ids = [f"ArXiv:{aid}" for aid in arxiv_ids]
    resp = _request_with_backoff(batch_url, headers, method="POST", json_body={"ids": s2_ids})

    if resp.status_code in (400, 429, 500):
        print(f"    S2 batch returned {resp.status_code}: {resp.text[:200]}")
        return {aid: Enrichment(0, None, 0) for aid in arxiv_ids}
    results = resp.json()

    # Build enrichments from batch response
    enrichments: dict[str, Enrichment] = {}
    paper_id_map: dict[str, str] = {}  # arxiv_id -> s2 paperId

    for i, data in enumerate(results):
        arxiv_id = arxiv_ids[i]
        if data is None:
            enrichments[arxiv_id] = Enrichment(0, None, 0)
            continue

        tldr_text = None
        if data.get("tldr"):
            tldr_text = data["tldr"].get("text")

        affiliations = _extract_affiliations(data.get("authors", []))
        venue = data.get("venue") or None

        enrichments[arxiv_id] = Enrichment(
            citation_count=data.get("citationCount", 0),
            tldr=tldr_text,
            influential_citation_count=data.get("influentialCitationCount", 0),
            affiliations=affiliations,
            venue=venue,
        )

        s2_paper_id = data.get("paperId", "")
        if s2_paper_id:
            paper_id_map[arxiv_id] = s2_paper_id

    # Fetch recommendations in parallel (one thread per paper)
    def _fetch_recs(arxiv_id: str) -> tuple[str, list[RelatedPaper]]:
        s2_id = paper_id_map.get(arxiv_id, "")
        if not s2_id:
            return arxiv_id, []
        time.sleep(1)  # stagger requests slightly
        return arxiv_id, _get_recommendations(s2_id, headers)

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(_fetch_recs, aid) for aid in paper_id_map]
        for future in futures:
            arxiv_id, recs = future.result()
            enrichments[arxiv_id].related_papers = recs

    return enrichments


def _get_recommendations(paper_id: str, headers: dict[str, str]) -> list[RelatedPaper]:
    """Get recommended papers from Semantic Scholar."""
    rec_fields = "title,citationCount,year,url"
    rec_url = f"{RECOMMEND_URL}/{paper_id}?fields={rec_fields}&limit=5"

    resp = _request_with_backoff(rec_url, headers)

    if resp.status_code != 200:
        return []

    data = resp.json()
    return [
        RelatedPaper(
            title=p.get("title", ""),
            citation_count=p.get("citationCount", 0),
            year=p.get("year"),
            url=p.get("url", ""),
        )
        for p in data.get("recommendedPapers", [])
    ]
