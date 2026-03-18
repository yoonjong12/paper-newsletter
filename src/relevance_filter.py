"""Use Gemini to batch-score and categorize paper relevance based on user's research interests."""

import json
from google import genai

from src.arxiv_client import ArxivPaper


def _build_scoring_prompt(interests: str, sections: dict[str, str]) -> str:
    """Build the Gemini scoring prompt from config."""
    category_lines = []
    for name, emoji in sections.items():
        category_lines.append(f'- "{name}"')

    category_list = "\n".join(category_lines)
    category_names = list(sections.keys())
    first_category = category_names[0]

    return f"""You are a research paper relevance scorer.

## Reader Profile
{interests}

## Scoring Rules
- Score 8-10: Directly advances one of the reader's core interests listed above
- Score 6-7: Related but tangential to the reader's specific focus
- Score 1-5: Not relevant to the reader's research

## Categories
Assign exactly ONE:
{category_list}

## Output
For each paper, output a JSON object:
- "id": the arxiv_id
- "score": integer 1-10
- "category": one of the categories above
- "reason": one sentence explaining relevance to the reader's interests

Output a JSON array. Nothing else."""


def score_papers(papers: list[ArxivPaper], api_key: str, interests: str, sections: dict[str, str]) -> dict[str, dict]:
    """Score and categorize all papers in a single Gemini call."""
    if not papers:
        return {}

    prompt = _build_scoring_prompt(interests, sections)

    paper_texts = []
    for p in papers:
        paper_texts.append(f"[{p.arxiv_id}] {p.title}\n{p.abstract[:500]}")

    user_content = "\n\n---\n\n".join(paper_texts)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"{prompt}\n\nPapers:\n\n{user_content}",
    )

    raw_text = response.text
    start = raw_text.index("[")
    end = raw_text.rindex("]") + 1
    scores_list = json.loads(raw_text[start:end])

    return {
        item["id"]: {
            "score": item["score"],
            "category": item["category"],
            "reason": item["reason"],
        }
        for item in scores_list
    }


def filter_relevant(papers: list[ArxivPaper], scores: dict[str, dict], threshold: int = 7) -> list[ArxivPaper]:
    """Return papers scoring at or above the threshold."""
    return [
        p for p in papers
        if scores.get(p.arxiv_id, {}).get("score", 0) >= threshold
    ]


def group_by_category(
    papers: list[ArxivPaper],
    scores: dict[str, dict],
    categories: list[str],
) -> dict[str, list[ArxivPaper]]:
    """Group papers by their assigned category, preserving category order."""
    groups: dict[str, list[ArxivPaper]] = {}
    for cat in categories:
        groups[cat] = []

    first_category = categories[0]

    for p in papers:
        cat = scores.get(p.arxiv_id, {}).get("category", first_category)
        if cat not in groups:
            cat = first_category
        groups[cat].append(p)

    return {cat: papers for cat, papers in groups.items() if papers}
