# Paper Newsletter

Daily digest of LLM agent papers from arXiv, scored by Gemini, enriched with Semantic Scholar, delivered to Slack.

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

The agent handles everything — environment, API keys, GitHub Actions, and your first test delivery.

## API Keys

| Key | Required | Where to get it |
|-----|----------|----------------|
| Gemini API Key | Yes | [Google AI Studio](https://aistudio.google.com/apikeys) |
| Slack Webhook URL | Yes | [Slack Apps](https://api.slack.com/apps) → Incoming Webhooks |
| Semantic Scholar API Key | Optional | [S2 API](https://www.semanticscholar.org/product/api#api-key) |

> Semantic Scholar key improves rate limits but is not required. The newsletter works without it.

## Commands

| Command | Description |
|---------|-------------|
| `/paper-newsletter:install` | Setup environment, keys, and first delivery |
| `/paper-newsletter:send` | Send newsletter now |
| `/paper-newsletter:schedule` | Change delivery frequency and time |
| `/paper-newsletter:customize` | Change topics, keywords, and categories |

## How It Works

1. **Fetch** — Pulls recent papers from arXiv (`cs.AI`, `cs.CL`, `cs.MA`) with keyword pre-filtering
2. **Score** — Gemini Flash rates each paper (1-10) against your research interest profile
3. **Enrich** — Semantic Scholar adds citation counts, TLDR summaries, and related papers
4. **Deliver** — Sends categorized digest to Slack

## Default Categories

| Section | |
|---------|---|
| Memory | 🧠 |
| Optimization | ⚡ |
| Reasoning | 🔗 |
| Benchmarks | 📊 |
| Self-evolving | 🔄 |
| Orchestration | 🎼 |

Use `/paper-newsletter:customize` to change these.
