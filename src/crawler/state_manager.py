"""State manager for incremental crawling."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Set

class StateManager:
    """Track visited URLs to enable incremental crawling."""

    def __init__(self, state_file: str = "data/visited_urls.json"):
        self.state_path = Path(state_file)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self._visited: Set[str] = set()
        if self.state_path.exists():
            try:
                self._visited = set(json.loads(self.state_path.read_text()))
            except json.JSONDecodeError:
                self._visited = set()

    def is_visited(self, url: str) -> bool:
        return url in self._visited

    def mark_visited(self, url: str) -> None:
        self._visited.add(url)
        self.state_path.write_text(json.dumps(sorted(self._visited)))
