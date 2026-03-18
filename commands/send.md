# Send

Send the newsletter immediately.

## Find the user's newsletter repo

```bash
gh repo list --json name,description --jq '.[] | select(.name | test("newsletter|paper"))'
```

If ambiguous, ask the user which repo.

## Trigger

```bash
gh workflow run daily.yml --repo <user>/<repo>
```

To override the lookback window:
```bash
gh workflow run daily.yml --repo <user>/<repo> -f days_back=7
```

## Monitor

```bash
gh run list --repo <user>/<repo> --workflow=daily.yml --limit=3
```
