import json

from paths import DATA_DIR
from datetime import date
from pathlib import Path


class ProgressStore:
    """Appends each fetched player to a JSONL (JSON Lines: one JSON object per line) file."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or DATA_DIR / f"progress_{date.today()}.jsonl")

    def load(self) -> dict:
        """Returns {player_id: api_response} for everything saved so far."""
        saved = {}
        if self.path.exists():
            with self.path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:  # Need to check what's up
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue  # half-written last line after a hard stop
                        # loading the full API response
                    saved[record["player_id"]] = record["data"]
        return saved

    def save(self, player_id: int, data: dict) -> None:
        """Appends one player. Reopening each time means it's on disk immediately."""
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"player_id": player_id, "data": data}) + "\n")
