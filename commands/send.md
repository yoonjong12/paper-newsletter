# Send

Send the newsletter immediately, regardless of schedule.

## Local execution

```bash
cd <project-root>
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python -m src.main
```

## Via GitHub Actions

```bash
gh workflow run daily.yml
```

To override the lookback window (e.g., fetch last 7 days):
```bash
gh workflow run daily.yml -f days_back=7
```

Monitor with `gh run list --workflow=daily.yml --limit=3`.
