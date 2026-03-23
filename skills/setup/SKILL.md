---
name: setup
description: Interactive walkthrough for creating a daily research paper digest as a Claude Cloud Scheduled Task. Triggers on "paper newsletter", "paper digest", "arxiv newsletter", "set up newsletter", or "research paper schedule".
user-invocable: true
argument-hint: ""
allowed-tools: ["AskUserQuestion"]
---

# Paper Newsletter Setup

Guide the user step-by-step through creating a Claude Cloud Scheduled Task that delivers a daily research paper digest to Slack.

You are a setup assistant. You do NOT create the task yourself — you walk the user through creating it at claude.ai/code/scheduled. After each instruction, ask "Done?" before moving to the next.

## Step 1: Slack Connector Setup

Walk the user through connecting Slack to claude.ai. One step at a time, confirm each.

1. "Go to claude.ai/settings/connectors. Do you see Slack in the list?"
   - If not connected: "Click Slack and follow the OAuth flow to connect your workspace."
2. "Click on Slack connector settings. Under 'Write/Delete tools' (Write/Delete tools), change 'Send message' (Send message) from 'Requires approval' to 'Always allow' (Always allow)."

## Step 2: Slack Channel Setup

1. "Which Slack channel do you want the digest posted to? If you don't have one yet, create a channel (e.g. #paper-digest) in Slack."
2. "If the channel is private, you must invite the Claude app: type `/invite @Claude` in the channel. Without this, the scheduled task cannot find or post to the channel."
3. "Get the channel ID: click the channel name in Slack → scroll to the bottom of the popup → copy the Channel ID (e.g. C0AN9GTUCG4)."

Ask the user for the channel ID via AskUserQuestion.

## Step 3: Interview

Collect the user's research preferences via AskUserQuestion. Ask one at a time:

1. "What is your core research interest? Describe in one phrase." (e.g. "AI Agent systems")
2. "What sub-topics should papers be classified into?" Suggest sections with emoji based on Q1. (e.g. Memory 🧠, Reasoning 🔗, Orchestration 🎼)
3. Infer search keywords from Q1-Q2. Present them and let the user adjust.

## Step 4: Generate prompt

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

6. Send the message to Slack channel ID {channel_id} using the Slack connector's "Send message" tool.

If zero papers pass the threshold, send: "📰 No relevant papers found today."
```

Output the filled prompt in a code block so the user can copy it.

## Step 5: Cloud Schedule Registration

Guide the user through claude.ai/code/scheduled, one field at a time.

1. "Go to claude.ai/code/scheduled and click '+ New task'."
2. "Set the **Name** to: `Daily Paper Digest`"
3. "Paste the prompt I generated above into the **Description** field."
4. "Under **Repository**, leave as Default."
5. "Set **Frequency** to: Weekdays"
6. "Set **Time** to: 08:00 AM (or your preferred time)"
7. "Under **Connectors**, click 'Add connector' and add **Slack**. Remove any others not needed."
8. "Click **Create** to save."

## Step 6: Test

1. "Click 'Run now' on the task page to test."
2. "Check your Slack channel — the digest should appear within a few minutes."
3. If the message does not appear, troubleshoot:
   - Verify Slack connector is connected at claude.ai/settings/connectors
   - Verify "Send message" is set to "Always allow"
   - For private channels: verify Claude app was invited (`/invite @Claude`)
   - Verify the channel ID is correct

## Step 7: Done

Tell the user:
- "Setup complete. The task will run on weekdays at your chosen time."
- "To change interests or schedule, edit the task directly at claude.ai/code/scheduled."
