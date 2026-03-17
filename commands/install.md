# Install

Guide the user through complete setup. Verify each step before moving to the next.

## Step 1: Python environment

Check Python version (requires >=3.11):
```bash
python3 --version
```

## Step 2: Install dependencies

```bash
cd <project-root>
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

Verify: `python -c "from src.arxiv_client import fetch_recent_papers; print('OK')"`

## Step 3: API Keys

Walk through each key one at a time:

**Gemini API Key** (required):
- Get from https://aistudio.google.com/apikeys

**Slack Webhook URL** (required):
- Go to https://api.slack.com/apps → Create New App → Incoming Webhooks → Activate → Add to channel
- Format: `https://hooks.slack.com/services/T.../B.../...`

**Semantic Scholar API Key** (optional — works without it, just slower rate limits):
- Get from https://www.semanticscholar.org/product/api#api-key

## Step 4: Create .env file

Write a `.env` file in the project root with the keys from Step 3.

## Step 5: Test run

```bash
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m src.main
```

Confirm papers appear in Slack.

## Step 6: GitHub Actions (optional)

If the user wants automated daily delivery:
1. Push repo to GitHub
2. Use `gh secret set` to register: `GEMINI_API_KEY`, `SLACK_WEBHOOK_URL`, and optionally `SEMANTIC_SCHOLAR_API_KEY`
3. The workflow at `.github/workflows/daily.yml` runs every weekday at KST 08:00
