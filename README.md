# paper-newsletter

Interactive setup guide for a daily research paper digest via Claude Cloud Scheduled Task.

Papers are discovered via WebSearch, scored by Claude, and delivered to Slack.

## Quick Start

```
/plugin marketplace add yoonjong12/paper-newsletter
/plugin install paper-newsletter@paper-newsletter-marketplace
```

Then run:

```
/paper-newsletter:setup
```

The assistant walks you through:
1. Defining your research interests and newsletter sections
2. Generating the task prompt
3. Registering the scheduled task at claude.ai/code/scheduled

## Requirements

- Claude Pro/Max/Team/Enterprise plan
- Slack connector enabled at claude.ai/settings/connectors
- Access to claude.ai/code/scheduled
