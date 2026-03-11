"""Fetch new papers from arXiv for target categories."""

import arxiv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class ArxivPaper:
    arxiv_id: str
    title: str
    abstract: str
    authors: list[str]
    categories: list[str]
    published: datetime
    pdf_url: str


CATEGORIES = ["cs.AI", "cs.CL", "cs.MA"]

AGENT_KEYWORDS = [
    "agent",
    "agentic",
    "tool use",
    "tool-use",
    "function calling",
    "ReAct",
    "chain-of-thought",
    "multi-agent",
    "LLM agent",
    "language model agent",
    "autonomous agent",
]


def fetch_recent_papers(days_back: int = 1, max_per_category: int = 200) -> list[ArxivPaper]:
    """Fetch papers from the last N days across target categories, pre-filtered by keywords."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    seen_ids: set[str] = set()
    papers: list[ArxivPaper] = []

    for category in CATEGORIES:
        query = f"cat:{category}"
        search = arxiv.Search(
            query=query,
            max_results=max_per_category,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        client = arxiv.Client(page_size=100, delay_seconds=3.0)

        for result in client.results(search):
            if result.published.replace(tzinfo=timezone.utc) < cutoff:
                break

            paper_id = result.entry_id.split("/abs/")[-1]
            if paper_id in seen_ids:
                continue

            title_lower = result.title.lower()
            abstract_lower = result.summary.lower()
            has_keyword = any(
                kw.lower() in title_lower or kw.lower() in abstract_lower
                for kw in AGENT_KEYWORDS
            )
            if not has_keyword:
                continue

            seen_ids.add(paper_id)
            papers.append(ArxivPaper(
                arxiv_id=paper_id,
                title=result.title.replace("\n", " ").strip(),
                abstract=result.summary.replace("\n", " ").strip(),
                authors=[a.name for a in result.authors],
                categories=[c for c in result.categories],
                published=result.published,
                pdf_url=result.pdf_url,
            ))

    return papers
