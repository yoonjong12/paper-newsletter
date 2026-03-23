# paper-newsletter

Daily LLM agent paper digest via Claude Cloud Schedule.

arXiv → Claude scoring → Semantic Scholar enrichment → Email

## Quick Start

Install the plugin in [Claude Code](https://claude.ai/code):

```
/plugin marketplace add yoonjong12/paper-newsletter
/plugin install paper-newsletter@paper-newsletter-marketplace
```

Then run:

```
/paper-newsletter:install
```

The agent creates a Claude Cloud Scheduled Task — interviews your interests, sets up email delivery, and schedules daily digests.

## API Keys

| Key | Required | Where to get it |
|-----|----------|----------------|
| Gmail App Password | Yes | Google Account > Security > 2-Step Verification > App Passwords |
| Semantic Scholar API Key | Optional | [S2 API](https://www.semanticscholar.org/product/api#api-key) |

## Commands

| Command | Description |
|---------|-------------|
| `/paper-newsletter:install` | Create Cloud Scheduled Task with your interests and email |

Frequency, interests, and sections are managed directly at [claude.ai/code/scheduled](https://claude.ai/code/scheduled).

## How It Works

1. **Fetch** — Pulls recent papers from arXiv via WebFetch
2. **Score** — Claude rates each paper against your research interests (no external LLM needed)
3. **Enrich** — Semantic Scholar adds institution, venue, and TLDR
4. **Deliver** — Sends categorized digest via Gmail SMTP
