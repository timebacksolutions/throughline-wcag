#!/usr/bin/env python3
"""Fetch the authoritative "Intent of this Success Criterion" lead paragraph for every
WCAG 2.2 success criterion from the W3C Understanding documents, and cache it to
``tools/understanding_intents.json`` (keyed by SC number).

The generator uses these as each ``system_requirement``'s ``rationale`` — the leaf-level
*why*. They are the W3C's own words (Understanding docs, W3C Document License), lightly
whitespace-normalised, not rewritten. Re-run only when refreshing against a new
Understanding publication; the cache is committed so a normal build needs no network.

Source: https://www.w3.org/WAI/WCAG22/Understanding/<slug>.html  (slug = SC ``id``).
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
WCAG = json.loads((TOOLS / "wcag-2.2.json").read_text(encoding="utf-8"))
OUT = TOOLS / "understanding_intents.json"
BASE = "https://www.w3.org/WAI/WCAG22/Understanding/{slug}.html"


def strip(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def intent_para(html: str) -> str:
    """First paragraph of the <section id="intent"> block."""
    m = re.search(r'id="intent".*?(?=</section>|<section)', html, re.S)
    seg = m.group(0) if m else html
    pm = re.search(r"<p>(.*?)</p>", seg, re.S)
    return strip(pm.group(1)) if pm else ""


def main() -> int:
    scs = [sc for p in WCAG["principles"] for g in p["guidelines"]
           for sc in g["successcriteria"]]
    out: dict[str, str] = json.loads(OUT.read_text()) if OUT.exists() else {}
    for sc in scs:
        num, slug = sc["num"], sc["id"]
        if num in out and out[num]:
            continue
        url = BASE.format(slug=slug)
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                html = r.read().decode("utf-8", "replace")
            para = intent_para(html)
        except Exception as e:  # noqa: BLE001 - best-effort fetch, report and continue
            para = ""
            print(f"  !! {num} {slug}: {e}", file=sys.stderr)
        out[num] = para
        print(f"  {num:8} {slug:45} {len(para):4d} chars")
        time.sleep(0.3)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    missing = [n for n, v in out.items() if not v]
    print(f"\nwrote {OUT} — {len(out)} intents, {len(missing)} missing: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
