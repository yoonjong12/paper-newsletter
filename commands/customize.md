# Customize

Change what papers are collected and how they're categorized.

## Interview the user

Ask one at a time:
1. "어떤 연구 주제에 관심이 있나요?"
2. "논문을 어떤 섹션으로 나눌까요?"
3. "arXiv 검색 키워드를 바꾸고 싶으세요?"

## Apply

1. Clone the user's newsletter repo
2. Update `config.yml` with new values:
   - `arxiv.categories` — arXiv category codes
   - `arxiv.keywords` — keyword filter strings
   - `scoring.interests` — structure user's free-text into ranked interests
   - `newsletter.sections` — section names with emoji
3. Commit and push
4. Run `/paper-newsletter:send` to verify
