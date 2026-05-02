import json
from datetime import datetime, timezone
from pathlib import Path

_USAGE_FILE = Path.home() / ".yusufbot_usage.json"


def _today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_daily_tokens() -> int:
    """Return tokens used today (UTC). Returns 0 if the date has rolled over."""
    if not _USAGE_FILE.exists():
        return 0
    try:
        data = json.loads(_USAGE_FILE.read_text())
        if data.get("date") == _today_utc():
            return int(data.get("tokens", 0))
    except (json.JSONDecodeError, ValueError, OSError):
        pass
    return 0


def add_tokens(n: int) -> int:
    """Add n to today's count, persist to disk, and return the new total."""
    new_total = load_daily_tokens() + n
    try:
        _USAGE_FILE.write_text(json.dumps({"date": _today_utc(), "tokens": new_total}))
    except OSError:
        pass
    return new_total
