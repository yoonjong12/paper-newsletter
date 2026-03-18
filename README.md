# Paper Newsletter

Daily paper digest from arXiv, scored by Gemini, enriched with Semantic Scholar, delivered to Slack.

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

The agent sets up your personal newsletter repo with GitHub Actions — API keys, schedule, and a test delivery.

## API Keys

| Key | Required | Where to get it |
|-----|----------|----------------|
| Gemini API Key | Yes | [Google AI Studio](https://aistudio.google.com/apikeys) |
| Slack Webhook URL | Yes | [Slack Apps](https://api.slack.com/apps) → Incoming Webhooks |
| Semantic Scholar API Key | Optional | [S2 API](https://www.semanticscholar.org/product/api#api-key) |

## Commands

| Command | Description |
|---------|-------------|
| `/paper-newsletter:install` | Create your newsletter repo, register keys, test delivery |
| `/paper-newsletter:send` | Send newsletter now |
| `/paper-newsletter:schedule` | Change delivery frequency and time |
| `/paper-newsletter:customize` | Change topics, keywords, and categories |

## How It Works

1. **Fetch** — Pulls recent papers from arXiv with keyword pre-filtering
2. **Score** — Gemini rates each paper against your research interests
3. **Enrich** — Semantic Scholar adds institution, venue, TLDR, and related papers
4. **Deliver** — Sends categorized digest to Slack

## Configuration

Your newsletter repo contains a `config.yml`:

```yaml
arxiv:
  categories: ["cs.AI", "cs.CL"]
  keywords: ["agent", "tool use", "multi-agent"]

scoring:
  interests: |
    1. Your research interest
    2. Another interest
  threshold: 8

newsletter:
  sections:
    Memory: "🧠"
    Reasoning: "🔗"

schedule:
  cron: "0 23 * * 0-4"
  days_back_weekday: 1
  days_back_monday: 3
```

Use `/paper-newsletter:customize` to change these.
