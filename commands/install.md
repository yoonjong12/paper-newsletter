# Install

Set up a daily paper newsletter as a Claude Cloud Scheduled Task.
No GitHub repo, no Python, no external LLM API needed — Claude does everything.

## Step 1: Interview (AskUserQuestion)

Ask one at a time:

1. "What research areas are you interested in? Describe freely."
2. "How would you like papers grouped into sections?" (suggest examples with emoji based on Q1 answer)
3. Review & confirm: infer arXiv categories + keywords from Q1-Q2, present them, let user adjust
4. "What email address should the newsletter be sent to?"
5. "How often and when do you want it?" (default: weekdays 08:00 KST)

## Step 2: Email credentials

AskUserQuestion: "Gmail App Password is required for sending. Choose one:
1. Provide a .env file path (containing EMAIL_TO and GMAIL_APP_PASSWORD)
2. Enter values directly"

**Option A: .env file path**
- Read the file, extract EMAIL_TO and GMAIL_APP_PASSWORD

**Option B: Direct input**
- Ask for each value via AskUserQuestion

For missing keys, print where to get them:
- Gmail App Password: Google Account > Security > 2-Step Verification > App Passwords

## Step 3: Create Cloud Scheduled Task

Use CronCreate to register the scheduled task with the following prompt template.
Convert the user's preferred frequency/time to a cron expression (KST to local timezone).

### Prompt template

Fill in {placeholders} from interview answers:

```
You are a research paper newsletter agent.

## Interests
{scoring_interests — structure user's free-text into ranked priorities}

## arXiv Categories
{categories — e.g. cs.AI, cs.CL, cs.MA, cs.LG, cs.SE}

## Keywords
{keywords — comma separated}

## Sections
{sections — e.g. Memory 🧠, Reasoning 🔗, Orchestration 🎼}

## Email Settings
- To: {email_to}
- Gmail App Password: {app_password}

## Procedure

1. Fetch recent papers from arXiv (1 day on weekdays, 3 days on Monday).
   URL: http://export.arxiv.org/api/query?search_query=cat:{cat1}+OR+cat:{cat2}+...&sortBy=submittedDate&start=0&max_results=100
   Use WebFetch to call the API and parse the Atom XML response.

2. Pre-filter candidates by matching [Keywords] against title + abstract.

3. Score each candidate against [Interests] on a 0-10 scale. Keep only papers scoring 8 or above.

4. Enrich selected papers via Semantic Scholar API.
   URL: https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=authors,venue,tldr,externalIds
   Use WebFetch to call the API.

5. Group papers into [Sections].

6. Format the newsletter:

📰 Daily Paper Digest — {date}

{emoji} {section_name}
• **{title}** — {authors} ({institution})
  {one_line_summary}
  🔗 {arxiv_url}

7. Send via Gmail SMTP:
   - SMTP server: smtp.gmail.com:465 (SSL)
   - From/To: {email_to}
   - Auth: {email_to} / {app_password}
   - Subject: "📰 Daily Paper Digest — {date}"
   - Body: newsletter content above (HTML format)

If zero papers pass the threshold, do not send an email.
```

## Step 4: Verify

Tell the user:
- "Cloud Scheduled Task created successfully."
- "Visit claude.ai/code/scheduled to view it and use 'Run now' to test."
- "To change frequency or interests, edit the task prompt directly at claude.ai/code/scheduled."
