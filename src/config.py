"""Load newsletter configuration from YAML."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Config:
    categories: list[str]
    keywords: list[str]
    arxiv_categories: list[str]
    interests: str
    sections: dict[str, str]
    threshold: int = 8
    days_back_weekday: int = 1
    days_back_monday: int = 3


def load_config(path: str) -> Config:
    """Load config from a YAML file."""
    raw = yaml.safe_load(Path(path).read_text())

    arxiv = raw["arxiv"]
    scoring = raw["scoring"]
    newsletter = raw["newsletter"]
    schedule = raw.get("schedule", {})

    return Config(
        arxiv_categories=arxiv["categories"],
        keywords=arxiv["keywords"],
        interests=scoring["interests"],
        threshold=scoring.get("threshold", 8),
        sections=newsletter["sections"],
        categories=list(newsletter["sections"].keys()),
        days_back_weekday=schedule.get("days_back_weekday", 1),
        days_back_monday=schedule.get("days_back_monday", 3),
    )
