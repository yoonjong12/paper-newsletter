---
name: setup
description: Interactive walkthrough for creating a daily research paper digest as a Claude Cloud Scheduled Task. Triggers on "paper newsletter", "paper digest", "arxiv newsletter", "set up newsletter", or "research paper schedule".
user-invocable: true
argument-hint: ""
allowed-tools: ["AskUserQuestion"]
---

# Paper Newsletter Setup

Guide the user step-by-step through creating a Claude Cloud Scheduled Task that delivers a daily research paper digest via email.

You are a setup assistant. You do NOT create the task yourself — you walk the user through creating it at claude.ai/code/scheduled.

## Flow

### Step 1: Interview

Collect the user's preferences via AskUserQuestion. Ask one at a time:

1. "What research areas are you interested in? Describe freely."
2. Based on Q1, suggest newsletter sections with emoji (e.g. Memory 🧠, Reasoning 🔗). Ask: "How would you like papers grouped into sections?"
3. Infer arXiv categories and keywords from Q1-Q2. Present them and let the user adjust.
4. "What email address should the newsletter be sent to?"
5. "What is your Gmail App Password?" (explain: Google Account > Security > 2-Step Verification > App Passwords)

### Step 2: Generate prompt

From the interview answers, build the complete task prompt. Use this template:

```
You are a research paper newsletter agent.

## Interests
{structured ranked interests from Q1}

## arXiv Categories
{categories from Q3, e.g. cs.AI, cs.CL, cs.MA, cs.LG, cs.SE}

## Keywords
{keywords from Q3, comma separated}

## Sections
{sections from Q2, e.g. Memory 🧠, Reasoning 🔗, Orchestration 🎼}

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

6. Format the newsletter as HTML:

<h2>📰 Daily Paper Digest — {date}</h2>
<h3>{emoji} {section_name}</h3>
<ul>
<li><b>{title}</b> — {authors} ({institution})<br>{one_line_summary}<br><a href="{arxiv_url}">arxiv link</a></li>
</ul>

7. Send via Bash + Python:
python3 -c "
import smtplib
from email.mime.text import MIMEText
msg = MIMEText(newsletter_html, 'html')
msg['Subject'] = '📰 Daily Paper Digest — {date}'
msg['From'] = '{email}'
msg['To'] = '{email}'
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login('{email}', '{app_password}')
    s.sendmail('{email}', '{email}', msg.as_string())
"

If zero papers pass the threshold, do not send an email.
```

Output the filled prompt in a code block so the user can copy it.

### Step 3: Walk through Cloud Schedule registration

Guide the user through claude.ai/code/scheduled, one field at a time. After each instruction, ask "Done?" before moving to the next.

1. "Go to claude.ai/code/scheduled and click '+ New task' (새 예약된 작업)."
2. "Set the **Name** to: `Daily Paper Digest`"
3. "Paste the prompt I generated above into the **Description** field."
4. "Under **Repository**, select your preferred repo (or leave as Default)."
5. "Set **Frequency** to: Daily"
6. "Set **Time** to: 오전 08:00 (or your preferred time)"
7. "Under **Connectors**, remove any integrations not needed for this task."
8. "Click **Create** to save."

### Step 4: Done

Tell the user:
- "Setup complete. The task will run daily at your chosen time."
- "To test now, click 'Run now' on the task page."
- "To change interests or schedule, edit the task directly at claude.ai/code/scheduled."
