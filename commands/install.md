# Install

Set up a personal paper newsletter with GitHub Actions. Handle everything for the user.
Automate all scripted steps silently. Only ask questions that require the user's creative input.

## Step 1: Prerequisites

Verify silently (do NOT ask the user):
- `gh auth status` — must be logged in
- `gh` CLI available

If not met, print what's missing and stop.

## Step 2: Interview (AskUserQuestion)

Only these 3 questions require human input. Ask one at a time:

1. "어떤 연구 분야에 관심이 있나요? 자유롭게 설명해주세요."
2. "논문을 어떤 섹션으로 나눌까요?" (suggest examples with emoji based on Q1 answer)
3. Review & confirm: infer arXiv categories + keywords from Q1-Q2, present them, let user adjust

Optional (ask only after Q3):
4. "GitHub 레포 이름을 정해주세요." (default: my-paper-newsletter)

## Step 3: Generate config.yml

From the user's answers, build a config.yml:

```yaml
arxiv:
  categories: [...]   # infer from their research area
  keywords: [...]      # infer from interests, confirmed in Q3

scoring:
  interests: |
    # Structure the user's free-text answer into ranked interests
  threshold: 8

newsletter:
  sections:
    SectionName: "emoji"

schedule:
  cron: "0 23 * * 0-4"
  days_back_weekday: 1
  days_back_monday: 3
```

## Step 4: Create repo, push, and register secrets

Run all of these automatically:

```bash
gh repo create <name> --private --clone
cd <name>
```

Write config.yml and .github/workflows/daily.yml into the repo.

The workflow template:
```yaml
name: Paper Newsletter
on:
  schedule:
    - cron: "<from config>"
  workflow_dispatch:
    inputs:
      days_back:
        description: "Override days_back"
        required: false
jobs:
  newsletter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install git+https://github.com/yoonjong12/paper-newsletter.git@main
      - run: paper-newsletter --config config.yml
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          SEMANTIC_SCHOLAR_API_KEY: ${{ secrets.SEMANTIC_SCHOLAR_API_KEY }}
          DAYS_BACK: ${{ github.event.inputs.days_back }}
```

```bash
git add -A && git commit -m "Initial newsletter setup" && git push -u origin main
```

## Step 5: API Keys (automated — user stays in chat)

The user must NEVER leave the chat to run commands manually.
Ask via AskUserQuestion: "API 키가 담긴 .env 파일 경로를 알려주세요. 없으면 직접 입력할게요."

**Option A: .env 파일 경로** (Recommended)
- Read the file, extract GEMINI_API_KEY, SLACK_WEBHOOK_URL, SEMANTIC_SCHOLAR_API_KEY
- Register each non-empty key: `gh secret set <KEY> --repo <user>/<name> --body "<value>"`

**Option B: 직접 입력**
- AskUserQuestion으로 각 키를 받아서 동일하게 `--body`로 등록

For missing keys, print where to get them:
- Gemini: https://aistudio.google.com/apikeys
- Slack: https://api.slack.com/apps → Incoming Webhooks
- Semantic Scholar (optional): https://www.semanticscholar.org/product/api#api-key
  - Skip if empty (rate limit만 느려짐, 동작에는 문제 없음)

## Step 6: Test run

```bash
gh workflow run daily.yml --repo <user>/<name>
```

Monitor: `gh run list --repo <user>/<name> --limit 1`

Tell the user: "설정 완료. 내일 아침부터 뉴스레터가 도착합니다."
