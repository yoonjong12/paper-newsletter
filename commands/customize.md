# Customize

Change what papers are collected and how they're categorized.

## Interview the user

Ask one at a time:
1. "What research topics are you interested in?"
2. "How would you like papers grouped into sections?"
3. "Any specific keywords to filter arXiv papers?"

## Files to modify

**`src/arxiv_client.py`** — Pre-filter keywords and arXiv categories:
- `CATEGORIES`: list of arXiv category codes (e.g., `cs.AI`, `cs.CL`, `cs.MA`)
- `AGENT_KEYWORDS`: list of keyword strings for initial filtering

**`src/relevance_filter.py`** — Gemini scoring configuration:
- `CATEGORIES`: list of section names (e.g., `["Memory", "Optimization", ...]`)
- `RESEARCH_INTERESTS`: multi-line string describing the reader's research profile
- `SCORING_PROMPT`: update the category descriptions to match new categories

**`src/slack_sender.py`** — Section display:
- `SECTION_EMOJI`: dict mapping category names to emoji

## Important

Category names must match exactly across all three files. After changes, run `/paper-newsletter:send` to verify.
