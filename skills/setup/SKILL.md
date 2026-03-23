---
name: setup
description: Interactive walkthrough for creating a daily research paper digest as a Claude Cloud Scheduled Task. Triggers on "paper newsletter", "paper digest", "arxiv newsletter", "set up newsletter", or "research paper schedule".
user-invocable: true
argument-hint: ""
allowed-tools: ["AskUserQuestion"]
---

# Paper Newsletter Setup

Guide the user step-by-step through creating a Claude Cloud Scheduled Task that delivers a daily research paper digest to Slack.

You are a setup assistant. You do NOT create the task yourself — you walk the user through creating it at claude.ai/code/scheduled.

## Prerequisites

Before starting, the user must have:

- Slack connector enabled at claude.ai/settings/connectors
- Slack "메시지 보내기" (Send message) permission set to "항상 허용" (Always allow)
- A Slack channel for the digest (e.g. #paper-digest)

If any prerequisite is missing, guide the user to set it up before continuing.

## Flow

### Step 1: Interview

Collect the user's preferences via AskUserQuestion. Ask one at a time:

1. "What is your core research interest? Describe in one phrase." (e.g. "AI Agent systems")
2. "What sub-topics should papers be classified into?" Suggest sections with emoji based on Q1. (e.g. Memory 🧠, Reasoning 🔗, Orchestration 🎼)
3. Infer search keywords from Q1-Q2. Present them and let the user adjust.
4. "What is the Slack channel ID for the digest?" (explain: click channel name in Slack → channel ID at the bottom, e.g. C0AN9GTUCG4)

### Step 2: Generate prompt

From the interview answers, build the complete task prompt. Use this template:

```text
You are a research paper newsletter agent.

## Core Interest
{core interest from Q1 — e.g. AI Agent systems — architecture, orchestration, and multi-agent coordination}

## Sections (classification categories, not priority)
{sections from Q2, e.g. Memory 🧠, Optimization ⚡, Reasoning 🔗, Benchmarks 📊, Self-evolving 🔄, Orchestration 🎼}

## Search Keywords
{keywords from Q3, comma separated}

## Procedure

1. Spawn 3 subagents in parallel to search for papers:

   Agent 1: "Search for recent papers. Run WebSearch: 'arxiv {keyword_group_1} site:arxiv.org 2026'. For each result, extract: title, authors, abstract, arxiv URL. Return a list."

   Agent 2: "Search for recent papers. Run WebSearch: 'arxiv {keyword_group_2} site:arxiv.org 2026'. For each result, extract: title, authors, abstract, arxiv URL. Return a list."

   Agent 3: "Search for recent papers. Run WebSearch: 'arxiv {keyword_group_3} site:arxiv.org 2026'. For each result, extract: title, authors, abstract, arxiv URL. Return a list."

2. Merge all results and deduplicate by arxiv URL.

3. Score each paper against [Core Interest] on a 0-10 scale in a single batch. Keep only papers scoring 8 or above.

4. Classify selected papers into [Sections].

5. Format the digest as a Slack message:

📰 *Daily Paper Digest — {date}*

{emoji} *{section_name}*
• *{title}* — {authors}
  {one_line_summary}
  <{arxiv_url}|arxiv link>

6. Send the message to Slack channel ID {channel_id} using the Slack connector's "메시지 보내기" tool.

If zero papers pass the threshold, send: "📰 No relevant papers found today."
```

Output the filled prompt in a code block so the user can copy it.

### Step 3: Walk through Cloud Schedule registration

Guide the user through claude.ai/code/scheduled, one field at a time. After each instruction, ask "Done?" before moving to the next.

1. "Go to claude.ai/code/scheduled and click '+ New task'."
2. "Set the **Name** to: `Daily Paper Digest`"
3. "Paste the prompt I generated above into the **Description** field."
4. "Under **Repository**, leave as Default."
5. "Set **Frequency** to: Weekdays"
6. "Set **Time** to: 오전 08:00 (or your preferred time)"
7. "Under **Connectors**, make sure **Slack** is included. Remove any others not needed."
8. "Click **Create** to save."

### Step 4: Done

Tell the user:
- "Setup complete. The task will run on weekdays at your chosen time."
- "To test now, click 'Run now' on the task page."
- "To change interests or schedule, edit the task directly at claude.ai/code/scheduled."
