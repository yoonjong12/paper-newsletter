# Schedule

Change when the newsletter runs.

## Interview the user

1. "얼마나 자주 받고 싶으세요?" (매일 평일 / 특정 요일 / 주 1회)
2. "몇 시에 받고 싶으세요?" (사용자 타임존으로 묻고, UTC로 변환)

## Cron format reference

| Schedule | Cron | Notes |
|----------|------|-------|
| Weekdays KST 08:00 | `0 23 * * 0-4` | Sun-Thu UTC 23:00 |
| Weekdays KST 11:00 | `0 2 * * 1-5` | Mon-Fri UTC 02:00 |
| Every Monday KST 17:00 | `0 8 * * 1` | Mon UTC 08:00 |
| Daily KST 18:00 | `0 9 * * *` | Every day UTC 09:00 |

## Apply

1. Clone the user's newsletter repo
2. Update `config.yml` schedule section
3. Update `.github/workflows/daily.yml` cron value
4. Commit and push

Also adjust `days_back` in config.yml:

| Frequency | days_back_weekday | days_back_monday |
|-----------|-------------------|-----------------|
| Daily weekdays | 1 | 3 |
| Weekly | 7 | 7 |
