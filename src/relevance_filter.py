"""Use Gemini to batch-score and categorize paper relevance based on user's research interests."""

import json
from google import genai

from src.arxiv_client import ArxivPaper


CATEGORIES = [
    "Memory",
    "Optimization",
    "Reasoning",
    "Benchmarks",
    "Self-evolving",
    "Orchestration",
]

# Derived from 104 papers the user has reviewed
RESEARCH_INTERESTS = """The reader is a researcher focused on LLM-based autonomous agent systems.
Their specific interests (ranked by depth of engagement):

1. Agent Orchestration & Skill Composition — multi-agent coordination, DAG-based workflows,
   tool integration, function calling, skill ecosystems (AgentSkillOS, SkillOrchestra, ToolLLM)
2. Memory Systems — hierarchical/episodic/semantic memory for agents, long-term persistence,
   retrieval optimization (Mem0, MemoryOS, A-Mem, BudgetMem)
3. Prompt & Cost Optimization — automatic prompt refinement, model routing, cost-efficient
   inference, RL-based policy optimization (DLPO, TextGrad, FrugalGPT, RouteLLM, Router-R1)
4. Reasoning & Planning — CoT variants, ReAct, test-time compute scaling, multi-step planning,
   multi-agent debate
5. Self-evolving Systems — reflexion, learning from failure, online adaptation, experience
   accumulation (Reflexion, ExpeL, SCOPE, Memento)
6. Benchmarks & Evaluation — SWE-bench, agent evaluation frameworks, safety/alignment testing,
   real-world task benchmarks (Terminal-Bench, SkillsBench, DeepResearch-Bench)"""

SCORING_PROMPT = f"""You are a research paper relevance scorer.

## Reader Profile
{RESEARCH_INTERESTS}

## Scoring Rules
- Score 8-10: Directly advances one of the reader's core interests listed above
- Score 6-7: Related to LLM agents but tangential to the reader's specific focus
- Score 1-5: Not relevant to the reader's research

## Exclude
- Pure LLM training/fine-tuning without agent context
- RL agents without LLMs
- Chatbots/dialogue without agency
- Generic NLP tasks unless agent-related

## Categories
Assign exactly ONE:
- "Memory": long-term memory, episodic/semantic memory, retrieval, context persistence
- "Optimization": prompt optimization, cost routing, RL/policy, efficiency
- "Reasoning": CoT, ReAct, planning, test-time compute, multi-step reasoning
- "Benchmarks": evaluation frameworks, leaderboards, safety, alignment testing
- "Self-evolving": reflexion, learning from failure, online adaptation, self-refine
- "Orchestration": multi-agent, skill composition, tool use, DAG, function calling

## Output
For each paper, output a JSON object:
- "id": the arxiv_id
- "score": integer 1-10
- "category": one of the 6 categories
- "reason": one sentence explaining relevance to the reader's interests

Output a JSON array. Nothing else."""


def score_papers(papers: list[ArxivPaper], api_key: str) -> dict[str, dict]:
    """Score and categorize all papers in a single Gemini call."""
    if not papers:
        return {}

    paper_texts = []
    for p in papers:
        paper_texts.append(f"[{p.arxiv_id}] {p.title}\n{p.abstract[:500]}")

    user_content = "\n\n---\n\n".join(paper_texts)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"{SCORING_PROMPT}\n\nPapers:\n\n{user_content}",
    )

    raw_text = response.text
    # Extract JSON array — handle markdown code fences or extra text
    start = raw_text.index("[")
    end = raw_text.rindex("]") + 1
    scores_list = json.loads(raw_text[start:end])

    return {
        item["id"]: {
            "score": item["score"],
            "category": item["category"],
            "reason": item["reason"],
        }
        for item in scores_list
    }


def filter_relevant(papers: list[ArxivPaper], scores: dict[str, dict], threshold: int = 7) -> list[ArxivPaper]:
    """Return papers scoring at or above the threshold."""
    return [
        p for p in papers
        if scores.get(p.arxiv_id, {}).get("score", 0) >= threshold
    ]


def group_by_category(papers: list[ArxivPaper], scores: dict[str, dict]) -> dict[str, list[ArxivPaper]]:
    """Group papers by their assigned category, preserving category order."""
    groups: dict[str, list[ArxivPaper]] = {}
    for cat in CATEGORIES:
        groups[cat] = []

    for p in papers:
        cat = scores.get(p.arxiv_id, {}).get("category", "Orchestration")
        if cat not in groups:
            cat = "Orchestration"
        groups[cat].append(p)

    return {cat: papers for cat, papers in groups.items() if papers}
