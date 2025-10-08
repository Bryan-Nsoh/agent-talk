"""Structured logging for conversations."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def append_log(path: Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, separators=(",", ":")))
        fh.write("\n")
