"""Paper newsletter orchestrator — daily digest."""

import argparse
import os
from datetime import datetime, timezone, timedelta

from src.arxiv_client import fetch_recent_papers
from src.config import load_config
from src.email_sender import send_email
from src.relevance_filter import score_papers, filter_relevant, group_by_category


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config.yml")
    args = parser.parse_args()

    cfg = load_config(args.config)

    gemini_key = os.environ["GEMINI_API_KEY"]
    email_to = os.environ["EMAIL_TO"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    now = datetime.now(timezone(timedelta(hours=9)))  # KST
    date_str = now.strftime("%Y-%m-%d")
    weekday = now.weekday()  # 0=Monday

    days_back_default = cfg.days_back_monday if weekday == 0 else cfg.days_back_weekday
    days_back = int(os.environ.get("DAYS_BACK") or days_back_default)

    print(f"[{date_str}] Fetching recent papers from arXiv ({days_back} days)...")

    papers = fetch_recent_papers(
        categories=cfg.arxiv_categories,
        keywords=cfg.keywords,
        days_back=days_back,
    )
    print(f"  Found {len(papers)} keyword-matched papers")

    if not papers:
        print("  No papers found. Skipping.")
        return

    print("  Scoring relevance with Gemini...")
    scores = score_papers(papers, gemini_key, interests=cfg.interests, sections=cfg.sections)

    relevant = filter_relevant(papers, scores, threshold=cfg.threshold)
    relevant.sort(key=lambda p: scores.get(p.arxiv_id, {}).get("score", 0), reverse=True)
    print(f"  {len(relevant)} papers scored >= {cfg.threshold}")

    if not relevant:
        print("  No highly relevant papers. Skipping.")
        return

    print("  Grouping by category...")
    grouped = group_by_category(relevant, scores, categories=cfg.categories)

    for cat, cat_papers in grouped.items():
        print(f"    {cat}: {len(cat_papers)} papers")

    print("  Sending email...")
    send_email(email_to, app_password, grouped, scores, sections=cfg.sections, date_str=date_str)
    print("  Done!")


if __name__ == "__main__":
    main()
