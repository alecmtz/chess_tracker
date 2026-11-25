import json
from datetime import date

from paths import DATA_DIR
from pathlib import Path


class RawStorage:
    """Appends each fetched record to a per-section JSONL (JSON Lines) file."""

    def __init__(self, section: str):
        self.path = DATA_DIR / f"progress_{date.today()}_{section}.jsonl"

    def load(self) -> dict:
        """Returns {player_id: api_response} for everything saved so far."""
        saved = {}
        if not self.path.exists():
            return saved

        with self.path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue  # half-written last line after a hard stop

                if record.get("player_id") is not None:
                    saved[record["player_id"]] = record["data"]
                else:
                    saved[record["category"]] = record["data"]
        return saved

    def save(self, data: dict, player_id: int | None = None, category: str | None = None) -> None:
        """Appends one record. Reopening each time means it's on disk immediately."""
        # Save the raw API response data
        record = {"data": data}

        if player_id is not None:
            record["player_id"] = player_id

        if category is not None:
            record["category"] = category

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

