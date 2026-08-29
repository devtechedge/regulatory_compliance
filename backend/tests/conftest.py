from __future__ import annotations

import os
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
os.environ.setdefault("DATA_DIR", str(_REPO / "data"))
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
