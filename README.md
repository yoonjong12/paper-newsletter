# Paper Newsletter

Automated weekly digest of LLM agent papers: arXiv → Gemini relevance scoring → Semantic Scholar enrichment → Slack.

## How it works

1. **Fetch** — Pulls recent papers from arXiv (`cs.AI`, `cs.CL`, `cs.MA`) with keyword pre-filtering
2. **Score** — Gemini Flash scores each paper (1-10) against your research interest profile
3. **Enrich** — Semantic Scholar adds citation counts, TLDR summaries, and related papers
4. **Deliver** — Sends categorized digest to Slack (one message per section)

### Categories

| Section | Emoji |
|---------|-------|
| Memory | 🧠 |
| Optimization | ⚡ |
| Reasoning | 🔗 |
| Benchmarks | 📊 |
| Self-evolving | 🔄 |
| Orchestration | 🎼 |

## Setup

### Requirements

- Python ≥ 3.11
- API keys: Gemini (required), Semantic Scholar (optional), Slack Webhook (required)

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Configure

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```
GEMINI_API_KEY=...
SEMANTIC_SCHOLAR_API_KEY=...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Run

```bash
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m src.main
```

## Automation

GitHub Actions workflow runs every Monday at KST 17:00 (UTC 08:00).

Add these secrets to your repo: `GEMINI_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`, `SLACK_WEBHOOK_URL`.

Manual trigger:

```bash
gh workflow run daily.yml
```

## Claude Code Skill

If you use [Claude Code](https://claude.com/claude-code), a skill is available at `.claude/skills/paper-newsletter/`:

- `/paper-newsletter install` — guided setup
- `/paper-newsletter send` — send now
- `/paper-newsletter schedule` — change cron schedule
- `/paper-newsletter customize` — change research topics
