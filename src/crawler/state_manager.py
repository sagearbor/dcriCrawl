"""State manager for incremental crawling and site mapping."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Set


class StateManager:
    """Track visited URLs and their hashes to enable incremental crawling."""

    def __init__(
        self,
        state_file: str = "data/visited_urls.json",
        site_map_file: str = "data/site_map.json",
    ) -> None:
        self.state_path = Path(state_file)
        self.site_map_path = Path(site_map_file)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.site_map_path.parent.mkdir(parents=True, exist_ok=True)
        self._hashes: Dict[str, str] = {}
        self._site_map: Set[str] = set()
        if self.state_path.exists():
            try:
                self._hashes = json.loads(self.state_path.read_text())
            except json.JSONDecodeError:
                self._hashes = {}
        if self.site_map_path.exists():
            try:
                self._site_map = set(json.loads(self.site_map_path.read_text()))
            except json.JSONDecodeError:
                self._site_map = set()

    def is_visited(self, url: str) -> bool:
        """Return ``True`` if ``url`` has been visited before."""
        return url in self._hashes

    def has_changed(self, url: str, html: str) -> bool:
        """Return ``True`` if ``html`` differs from the stored hash for ``url``."""
        new_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
        old_hash = self._hashes.get(url)
        return old_hash != new_hash

    def mark_visited(self, url: str, html: str) -> None:
        """Record ``url`` as visited and store a hash of its ``html``."""
        self._hashes[url] = hashlib.sha256(html.encode("utf-8")).hexdigest()
        self.state_path.write_text(json.dumps(self._hashes, indent=2))

    def record_discovered(self, url: str) -> None:
        """Record a discovered ``url`` for building a site map."""
        self._site_map.add(url)
        self.site_map_path.write_text(json.dumps(sorted(self._site_map)))
