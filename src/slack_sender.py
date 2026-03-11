"""Send formatted newsletter to Slack via incoming webhook — one message per category."""

import time

import httpx

from src.arxiv_client import ArxivPaper
from src.semantic_scholar import Enrichment


def format_paper_block(paper: ArxivPaper, enrichment: Enrichment, score_reason: str) -> str:
    """Format a single paper into a Slack mrkdwn block."""
    authors_str = ", ".join(paper.authors[:3])
    if len(paper.authors) > 3:
        authors_str += f" +{len(paper.authors) - 3}"

    lines = [
        f"*<{paper.pdf_url}|{paper.title}>*",
        f"_{authors_str}_ | Citations: {enrichment.citation_count}",
    ]

    if enrichment.tldr:
        lines.append(f"TLDR: {enrichment.tldr}")

    lines.append(f"Relevance: {score_reason}")

    if enrichment.related_papers:
        lines.append("")
        lines.append("Related papers:")
        for rp in enrichment.related_papers:
            year_str = f" ({rp.year})" if rp.year else ""
            lines.append(
                f"  • <{rp.url}|{rp.title}>{year_str} — {rp.citation_count} citations"
            )

    return "\n".join(lines)


SECTION_EMOJI = {
    "Memory": "🧠",
    "Optimization": "⚡",
    "Reasoning": "🔗",
    "Benchmarks": "📊",
    "Self-evolving": "🔄",
    "Orchestration": "🎼",
}


def build_header_message(date_str: str, total: int, num_categories: int) -> dict:
    """Build the header message."""
    return {"blocks": [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"LLM Agent Papers — {date_str}"},
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"{total} relevant papers across {num_categories} categories"}],
        },
    ]}


def build_section_message(
    category: str,
    papers: list[ArxivPaper],
    enrichments: dict[str, Enrichment],
    scores: dict[str, dict],
) -> dict:
    """Build one Slack message per category section."""
    emoji = SECTION_EMOJI.get(category, "📄")
    blocks = [
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*{emoji} Agent > {category}* ({len(papers)})"},
        },
    ]

    for paper in papers:
        enrichment = enrichments.get(paper.arxiv_id, Enrichment(0, None, 0))
        reason = scores.get(paper.arxiv_id, {}).get("reason", "")

        text = format_paper_block(paper, enrichment, reason)
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": text},
        })

    return {"blocks": blocks}


def send_to_slack(
    webhook_url: str,
    grouped_papers: dict[str, list[ArxivPaper]],
    enrichments: dict[str, Enrichment],
    scores: dict[str, dict],
    date_str: str,
) -> None:
    """Send newsletter as header + one message per category to stay under Slack's 50-block limit."""
    total = sum(len(papers) for papers in grouped_papers.values())

    with httpx.Client(timeout=30) as client:
        # Header
        header = build_header_message(date_str, total, len(grouped_papers))
        resp = client.post(webhook_url, json=header)
        resp.raise_for_status()
        time.sleep(1)

        # One message per category
        for category, papers in grouped_papers.items():
            msg = build_section_message(category, papers, enrichments, scores)
            resp = client.post(webhook_url, json=msg)
            resp.raise_for_status()
            time.sleep(1)
