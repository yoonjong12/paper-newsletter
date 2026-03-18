# Install

Set up a personal paper newsletter with GitHub Actions. Handle everything for the user.

## Step 1: Collect info via AskUserQuestion

Ask one at a time:

1. "GitHub 레포 이름을 정해주세요." (default: my-paper-newsletter)
2. "Gemini API Key를 입력해주세요." (link: https://aistudio.google.com/apikeys)
3. "Slack Webhook URL을 입력해주세요." (link: https://api.slack.com/apps → Incoming Webhooks)
4. "Semantic Scholar API Key가 있으면 입력해주세요. 없으면 Enter" (optional)
5. "어떤 연구 분야에 관심이 있나요? 자유롭게 설명해주세요."
6. "논문을 어떤 섹션으로 나눌까요?" (suggest examples with emoji)
7. "arXiv에서 검색할 키워드를 알려주세요." (suggest defaults based on their interests)

## Step 2: Generate config.yml

From the user's answers, build a config.yml:

```yaml
arxiv:
  categories: [...]   # infer from their research area
  keywords: [...]      # from step 7

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

## Step 3: Create repo and push

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
      - run: pip install git+https://github.com/yoonjong12/paper-newsletter.git
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

## Step 4: Register secrets

```bash
gh secret set GEMINI_API_KEY --repo <user>/<name> --body "<key>"
gh secret set SLACK_WEBHOOK_URL --repo <user>/<name> --body "<url>"
# Only if provided:
gh secret set SEMANTIC_SCHOLAR_API_KEY --repo <user>/<name> --body "<key>"
```

## Step 5: Test run

```bash
gh workflow run daily.yml --repo <user>/<name>
```

Monitor: `gh run list --repo <user>/<name> --limit 1`

Tell the user: "설정 완료. 내일 아침부터 뉴스레터가 도착합니다."
