# Schedule

Change when the newsletter runs.

The schedule is defined in `.github/workflows/daily.yml` in the `cron` field.

## Interview the user

1. How often? (daily weekdays / specific days / weekly)
2. What time? (ask in their timezone, convert to UTC)

## Cron format reference

| Schedule | Cron | Notes |
|----------|------|-------|
| Weekdays KST 08:00 | `0 23 * * 0-4` | Sun-Thu UTC 23:00 |
| Weekdays KST 11:00 | `0 2 * * 1-5` | Mon-Fri UTC 02:00 |
| Every Monday KST 17:00 | `0 8 * * 1` | Mon UTC 08:00 |
| Daily KST 18:00 | `0 9 * * *` | Every day UTC 09:00 |

## Apply the change

Edit `.github/workflows/daily.yml`:
- Update the `cron` value
- Update the comment to match

Also update `days_back` logic in `src/main.py` if frequency changes:

| Frequency | days_back |
|-----------|-----------|
| Daily weekdays | Mon=3, Tue-Fri=1 |
| Weekly | 7 |
