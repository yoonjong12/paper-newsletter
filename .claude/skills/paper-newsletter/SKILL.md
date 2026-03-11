---
name: paper-newsletter
description: "Manage an automated LLM agent paper newsletter that fetches from arXiv, scores relevance with Gemini, enriches with Semantic Scholar, and delivers to Slack. Use this skill when the user mentions paper newsletter, arxiv newsletter, research paper digest, or wants to install/send/schedule/customize their paper newsletter. Commands: /paper-newsletter install, /paper-newsletter send, /paper-newsletter schedule, /paper-newsletter customize."
---

# Paper Newsletter Skill

Automated weekly digest of LLM agent papers from arXiv → Gemini relevance scoring → Semantic Scholar enrichment → Slack delivery.

**Repository location**: Detect via `find ~ -maxdepth 4 -name "paper-newsletter" -type d 2>/dev/null | head -5` or ask the user.

## Commands

Parse the user's intent to determine which command to run:
- **install**: user says "설치", "setup", "install", or is starting fresh
- **send**: user says "발송", "send", "run", "보내줘", or wants immediate delivery
- **schedule**: user says "스케쥴", "schedule", "cron", "주기", or wants to change timing
- **customize**: user says "수집", "주제", "토픽", "customize", "topics", or wants to change what papers are collected

---

## 1. Install

Guide the user through complete setup. Verify each step before moving to the next.

### Step 1: Python environment
Check Python version (requires >=3.11):
```bash
python3 --version
```
If below 3.11, guide them to install via conda or pyenv.

### Step 2: Clone and install
```bash
git clone <repo-url> paper-newsletter  # or confirm existing location
cd paper-newsletter
python3 -m venv .venv
source .venv/bin/activate
pip install .
```
Verify: `python -c "from src.arxiv_client import fetch_recent_papers; print('OK')"`

### Step 3: API Keys
The user needs 3 credentials. Walk through each one:

**Gemini API Key** (required):
- Get from https://aistudio.google.com/apikeys
- Verify: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=<KEY>" 2>/dev/null | head -c 100`

**Semantic Scholar API Key** (optional but recommended):
- Get from https://www.semanticscholar.org/product/api#api-key
- Without it, rate limits are stricter (100 req/5min vs 1 req/sec)

**Slack Webhook URL** (required):
- Go to https://api.slack.com/apps → Create New App → Incoming Webhooks → Activate → Add to channel
- Format: `https://hooks.slack.com/services/T.../B.../...`
- Verify: `curl -X POST -H 'Content-type: application/json' --data '{"text":"Newsletter test"}' <WEBHOOK_URL>`

### Step 4: Create .env file
Write a `.env` file in the project root:
```
GEMINI_API_KEY=<user's key>
SEMANTIC_SCHOLAR_API_KEY=<user's key>
SLACK_WEBHOOK_URL=<user's webhook>
```

### Step 5: Test run
```bash
cd <project-root>
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m src.main
```
Confirm papers appear in Slack. If errors occur, diagnose and fix before proceeding.

### Step 6: GitHub Actions (optional)
If the user wants automated weekly delivery:
- Push repo to GitHub
- Add secrets in Settings → Secrets → Actions: `GEMINI_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`, `SLACK_WEBHOOK_URL`
- The workflow at `.github/workflows/daily.yml` runs every Monday at KST 17:00

---

## 2. Send

Send the newsletter immediately, regardless of schedule.

```bash
cd <project-root>
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m src.main
```

If the user wants to send from GitHub Actions manually:
```bash
gh workflow run daily.yml
```

Monitor with `gh run list --workflow=daily.yml --limit=3`.

---

## 3. Schedule

The schedule is defined in `.github/workflows/daily.yml` in the `cron` field.

### Interview the user:
1. How often? (daily / weekly / specific days)
2. What time? (ask in their timezone, convert to UTC)

### Cron format reference:
| Schedule | Cron | Notes |
|----------|------|-------|
| Every Monday 17:00 KST | `0 8 * * 1` | KST = UTC+9 |
| Every weekday 09:00 KST | `0 0 * * 1-5` | Mon-Fri |
| Daily 18:00 KST | `0 9 * * *` | Every day |

### Apply the change:
Edit `.github/workflows/daily.yml`:
- Update the `cron` value
- Update the Korean comment to match
- If switching from weekly to daily, also update `days_back` in `src/main.py` (line with `fetch_recent_papers(days_back=...)`)

| Frequency | days_back |
|-----------|-----------|
| Daily | 1 |
| Every 2 days | 2 |
| Weekly | 7 |

---

## 4. Customize

Change what papers are collected and how they're categorized.

### Interview the user:
Ask these questions one at a time:
1. "What research topics are you interested in?" — Get their main areas of focus
2. "How would you like papers grouped into sections?" — Get category names
3. "Any specific keywords to filter arXiv papers?" — Get pre-filter keywords

### Files to modify:

**`src/arxiv_client.py`** — Pre-filter keywords and arXiv categories:
- `CATEGORIES`: list of arXiv category codes (e.g., `cs.AI`, `cs.CL`, `cs.MA`)
- `AGENT_KEYWORDS`: list of keyword strings for initial filtering

**`src/relevance_filter.py`** — Gemini scoring configuration:
- `CATEGORIES`: list of section names (e.g., `["Memory", "Optimization", ...]`)
- `RESEARCH_INTERESTS`: multi-line string describing the reader's research profile
- `SCORING_PROMPT`: the full prompt sent to Gemini — update the category descriptions in the "Categories" section to match new categories

**`src/slack_sender.py`** — Section display:
- `SECTION_EMOJI`: dict mapping category names to emoji

### Apply changes:
After the user confirms their preferences, edit all three files to reflect the new configuration. Ensure consistency across files — category names must match exactly in `relevance_filter.py` CATEGORIES list, SCORING_PROMPT category descriptions, and `slack_sender.py` SECTION_EMOJI keys.

Run a test send (command 2) to verify the changes work correctly.
