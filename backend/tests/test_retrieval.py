from __future__ import annotations

import json
import os
from pathlib import Path

from app.models import RegulatoryModule
from app.retrieval import retrieve, tokenize


def _data_dir() -> Path:
    env = os.environ.get("DATA_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "data"


def _modules_from_json() -> list[RegulatoryModule]:
    data_dir = _data_dir()
    modules: list[RegulatoryModule] = []
    for fname in ("mica.json", "vara.json"):
        payload = json.loads((data_dir / "frameworks" / fname).read_text(encoding="utf-8"))
        for mod in payload["modules"]:
            loc = mod.get("locator") or {}
            modules.append(
                RegulatoryModule(
                    id=mod["id"],
                    framework_id=payload["id"],
                    locator_title=loc.get("title") or "",
                    locator_article=loc.get("article") or "",
                    locator_clause=loc.get("clause"),
                    locator_url=loc.get("url") or "",
                    category=mod.get("category") or "other",
                    obligation=mod["obligation"],
                    evidence_checklist=mod.get("evidence_checklist") or [],
                    keywords=mod.get("keywords") or [],
                )
            )
    return modules


def test_tokenize_drops_stopwords_and_lowercases():
    tokens = tokenize("The Custody and Segregation of Client Assets")
    assert "custody" in tokens
    assert "segregation" in tokens
    assert "the" not in tokens
    assert "and" not in tokens
    assert "of" not in tokens


def test_rank_returns_custody_segregation_module_for_pack_snippet():
    modules = _modules_from_json()
    assert any(m.id == "mica-custody-segregation" for m in modules)
    pack = json.loads((_data_dir() / "projects" / "aurum-custody.json").read_text(encoding="utf-8"))
    snippet = pack["documents"][0]["content"]
    # Use the custody / segregation section, not the whole pack.
    start = snippet.lower().find("custody architecture")
    assert start >= 0
    excerpt = snippet[start : start + 900]

    ranked = retrieve(modules, excerpt, frameworks=["MiCA", "VARA"], top_k=8)
    ids = [item.module.id for item in ranked]
    custody_ids = {
        "mica-custody-segregation",
        "mica-custody-safekeeping",
        "vara-custody-rulebook",
    }
    assert ids, "retrieve returned no modules"
    assert ids[0] in custody_ids
    assert custody_ids & set(ids[:5])
