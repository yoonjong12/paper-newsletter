"""Paper newsletter orchestrator — daily weekday digest."""

import os
import time
from datetime import datetime, timezone, timedelta

from src.arxiv_client import fetch_recent_papers
from src.relevance_filter import score_papers, filter_relevant, group_by_category
from src.semantic_scholar import enrich_batch
from src.slack_sender import send_to_slack


def main() -> None:
    gemini_key = os.environ["GEMINI_API_KEY"]
    s2_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    slack_url = os.environ["SLACK_WEBHOOK_URL"]

    now = datetime.now(timezone(timedelta(hours=9)))  # KST
    date_str = now.strftime("%Y-%m-%d")
    weekday = now.weekday()  # 0=Monday
    days_back = int(os.environ.get("DAYS_BACK", 3 if weekday == 0 else 1))

    print(f"[{date_str}] Fetching recent papers from arXiv ({days_back} days)...")

    papers = fetch_recent_papers(days_back=days_back)
    print(f"  Found {len(papers)} keyword-matched papers")

    if not papers:
        print("  No papers found. Skipping.")
        return

    print("  Scoring relevance with Gemini...")
    scores = score_papers(papers, gemini_key)

    relevant = filter_relevant(papers, scores, threshold=8)
    relevant.sort(key=lambda p: scores.get(p.arxiv_id, {}).get("score", 0), reverse=True)
    max_enrich = int(os.environ.get("MAX_ENRICH", "20"))
    to_enrich = relevant[:max_enrich]
    print(f"  {len(relevant)} papers scored >= 8 (enriching top {len(to_enrich)})")

    if not relevant:
        print("  No highly relevant papers. Skipping.")
        return

    print("  Grouping by category...")
    grouped = group_by_category(relevant, scores)

    print("  Enriching with Semantic Scholar (batch per section)...")
    enrichments = {}
    for cat, cat_papers in grouped.items():
        batch_ids = []
        for p in cat_papers:
            if p in to_enrich:
                clean_id = p.arxiv_id.split("v")[0] if "v" in p.arxiv_id else p.arxiv_id
                batch_ids.append(clean_id)

        if not batch_ids:
            continue

        print(f"    {cat}: batch of {len(batch_ids)} papers")
        cat_enrichments = enrich_batch(batch_ids, api_key=s2_key)

        # Map back to original arxiv_ids (with version suffix)
        for p in cat_papers:
            clean_id = p.arxiv_id.split("v")[0] if "v" in p.arxiv_id else p.arxiv_id
            if clean_id in cat_enrichments:
                enrichments[p.arxiv_id] = cat_enrichments[clean_id]

        # Pause between category batches for rate limit
        time.sleep(3)

    for cat, cat_papers in grouped.items():
        print(f"    {cat}: {len(cat_papers)} papers")

    print("  Sending to Slack (1 message per section)...")
    send_to_slack(slack_url, grouped, enrichments, scores, date_str)
    print("  Done!")


if __name__ == "__main__":
    main()
