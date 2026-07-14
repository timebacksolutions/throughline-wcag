#!/usr/bin/env python3
"""Generate the WCAG 2.2 throughline source from the W3C canonical JSON.

Unlike the GOV.UK Design System (prose only), WCAG publishes a canonical machine-readable
serialisation — vendored here at ``tools/wcag-2.2.json`` (from
https://www.w3.org/WAI/WCAG22/wcag.json). This script turns it into throughline items,
mirroring the ASVS generator's discipline:

* **UIDs are permanent.** The mapping from a principle/guideline/criterion to a throughline
  UID is derived from the items already on disk, keyed by ``attrs.source_ref`` (the WCAG
  number: ``"Principle 1"``, ``"1.4"``, ``"1.4.3"``). Anything without an item yet gets a
  freshly allocated UID in document order, continuing from the highest in use; a UID, once
  allocated, never moves. Item bodies are regenerated from the JSON each run.

**The "why" spine is genuinely multi-root — the point of putting WCAG on the list.**
WCAG's four Principles (Perceivable, Operable, Understandable, Robust) are four *distinct*
reasons content must behave, so they are **four root intents** (INT-0001..INT-0004), not
one umbrella. Each Guideline is a ``user_requirement`` that ``derives_from`` its own
principle; each Success Criterion is a ``system_requirement`` that ``implements`` its
guideline. Because WCAG's hierarchy is strict (each guideline sits under exactly one
principle), grounding a criterion to a principle needs no extra edge — it flows up
implements→derives_from. The leaf *why* is preserved too: every criterion's ``rationale``
is the W3C "Intent of this Success Criterion" lead paragraph (``tools/fetch_intents.py``).

**Versions are attributes on one graph, not tags or folders.** WCAG 2.1 is a superset of
2.0 and 2.2 a near-superset of 2.1, so one graph carries all three: ``attrs.wcag_version``
records the version that *introduced* each criterion; ``attrs.level`` the A/AA/AAA grade.
The single criterion removed in 2.2 (4.1.1 Parsing) is kept as a throughline **tombstone**
(``status: deleted``, ``attrs.wcag_removed: "2.2"``) — never dropped. Version *releases*
are git tags of this one repo (v2.2.0, and a future v3.0.0), the same editions-as-tags
model as standard-asvs.

Usage:  python tools/generate.py   (run tools/fetch_intents.py first if intents are stale)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
INTENTS_DIR = REPO / "intents"       # intent (principle roots), prefix INT
GUIDELINES_DIR = REPO / "guidelines"  # user_requirement, prefix UR
CRITERIA_DIR = REPO / "criteria"      # system_requirement, prefix SR
SPEC = REPO / "docs" / "spec.md"

WCAG = json.loads((TOOLS / "wcag-2.2.json").read_text(encoding="utf-8"))
INTENTS = json.loads((TOOLS / "understanding_intents.json").read_text(encoding="utf-8"))

# The four principles are four co-equal roots — each a distinct "why". Text expands the
# principle's own statement into who it serves; faithful to POUR, not invented scope.
PRINCIPLE_INTENT = {
    "1": "Users can perceive the information and interface: content is available to sight, "
         "hearing or touch so no one is excluded because a single sense — for example vision "
         "or hearing — is unavailable to them. Information is never conveyed in a form only "
         "one sense can access.",
    "2": "Users can operate the interface and navigate the content whatever their input "
         "method — keyboard, pointer, voice, switch or assistive technology — and however "
         "much time, dexterity or precision they can bring, so no interaction demands an "
         "action a user cannot perform.",
    "3": "Users can understand both the information presented and how to operate the "
         "interface: content is readable and predictable and the system helps people avoid "
         "and recover from mistakes, so users with cognitive, learning or language "
         "differences are not shut out.",
    "4": "Content is coded so a wide range of user agents, including current and future "
         "assistive technologies, can reliably interpret it — so accessibility survives "
         "changes in browsers and tools rather than breaking as technology evolves.",
}

# One concise "why" per guideline (the guideline's own statement is its `text`). Faithful
# distillation of the published guideline purpose.
GUIDELINE_RATIONALE = {
    "1.1": "Text can be rendered as speech, braille, enlarged print or symbols, so non-text "
           "content reaches people who cannot see or process images.",
    "1.2": "Audio and video carry information some users cannot hear or see; captions, "
           "descriptions and transcripts make that information available to everyone.",
    "1.3": "When structure and relationships are encoded programmatically, content can be "
           "presented in different ways — spoken, reflowed, restyled — without losing meaning.",
    "1.4": "Users with low vision, colour blindness or hearing difficulty need enough "
           "contrast, control over audio and resizable text to separate content from its "
           "surroundings.",
    "2.1": "Many users cannot use a mouse; all functionality must be reachable and operable "
           "from a keyboard or keyboard interface.",
    "2.2": "People read and act at very different speeds; users must be able to turn off, "
           "adjust or extend time limits so they are not cut off mid-task.",
    "2.3": "Flashing content can trigger seizures; limiting flashes protects users with "
           "photosensitive epilepsy and vestibular disorders.",
    "2.4": "Users need ways to find content, orient themselves and know where they are — "
           "through titles, headings, focus order and visible focus — especially when they "
           "cannot scan a page visually.",
    "2.5": "People operate devices in many ways beyond a keyboard — touch, pointer, voice, "
           "motion — and each must work without requiring precise or tiring gestures.",
    "3.1": "Text must be readable and its language machine-identifiable so assistive "
           "technology can pronounce it and users can understand unusual words and "
           "abbreviations.",
    "3.2": "Interfaces that behave consistently and change only when the user expects it let "
           "people with cognitive differences build reliable mental models.",
    "3.3": "Everyone makes mistakes; clear labels, error identification, suggestions and "
           "prevention help users avoid and recover from them, especially on legal, "
           "financial or data submissions.",
    "4.1": "Content must expose correct name, role, value and status to assistive "
           "technologies so it keeps working across browsers, devices and future tools.",
}

VERSION_ORDER = {"2.0": 0, "2.1": 1, "2.2": 2}


def strip(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _dump(path: Path, item: dict) -> None:
    path.write_text(
        yaml.safe_dump(item, sort_keys=False, allow_unicode=True, width=90),
        encoding="utf-8",
    )


def _scan(dir_: Path) -> dict[str, str]:
    ref2uid: dict[str, str] = {}
    for f in dir_.glob("*.yml"):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        ref = (data.get("attrs") or {}).get("source_ref")
        if ref:
            ref2uid[ref] = data["uid"]
    return ref2uid


def _max(ref2uid: dict[str, str], prefix: str) -> int:
    return max((int(u.split("-")[1]) for u in ref2uid.values()
               if u.startswith(prefix + "-")), default=0)


def generate() -> dict[str, int]:
    int_ref = _scan(INTENTS_DIR)
    ur_ref = _scan(GUIDELINES_DIR)
    sr_ref = _scan(CRITERIA_DIR)
    n_int = _max(int_ref, "INT") + 1
    n_ur = _max(ur_ref, "UR") + 1
    n_sr = _max(sr_ref, "SR") + 1

    counts = {"int": 0, "ur": 0, "sr": 0, "tombstone": 0}

    for p in WCAG["principles"]:
        pref = f"Principle {p['num']}"
        int_uid = int_ref.get(pref)
        if int_uid is None:
            int_uid = f"INT-{n_int:04d}"; n_int += 1; int_ref[pref] = int_uid; counts["int"] += 1
        _dump(INTENTS_DIR / f"{int_uid}.yml", {
            "uid": int_uid,
            "type": "intent",
            "status": "approved",
            "title": f"{p['handle']} — {strip(p['title'])}",
            "text": PRINCIPLE_INTENT[p["num"]],
            "normative": False,
            "attrs": {"source_ref": pref},
        })

        for g in p["guidelines"]:
            gref = g["num"]
            ur_uid = ur_ref.get(gref)
            if ur_uid is None:
                ur_uid = f"UR-{n_ur:04d}"; n_ur += 1; ur_ref[gref] = ur_uid; counts["ur"] += 1
            _dump(GUIDELINES_DIR / f"{ur_uid}.yml", {
                "uid": ur_uid,
                "type": "user_requirement",
                "status": "approved",
                "title": f"{g['handle']} — {strip(g['title'])}",
                "text": strip(g["content"]) or strip(g["title"]),
                "rationale": GUIDELINE_RATIONALE[g["num"]],
                "links": [{"target": int_uid, "type": "derives_from"}],
                "attrs": {"source_ref": gref},
            })

            for sc in g["successcriteria"]:
                num = sc["num"]
                sr_uid = sr_ref.get(num)
                if sr_uid is None:
                    sr_uid = f"SR-{n_sr:04d}"; n_sr += 1; sr_ref[num] = sr_uid; counts["sr"] += 1
                versions = sc["versions"]
                introduced = min(versions, key=lambda v: VERSION_ORDER[v])
                removed = "2.2" not in versions  # only 4.1.1 Parsing
                level = sc["level"] or "A"       # 4.1.1 was Level A before removal
                attrs = {"source_ref": num, "level": level, "wcag_version": introduced}
                item = {
                    "uid": sr_uid,
                    "type": "system_requirement",
                    "status": "deleted" if removed else "approved",
                    "title": f"{sc['handle']} ({level})",
                    "text": strip(sc["content"]) or strip(sc["title"]),
                    "rationale": INTENTS.get(num, ""),
                    "links": [{"target": ur_uid, "type": "implements"}],
                    "attrs": attrs,
                }
                if removed:
                    item["attrs"]["wcag_removed"] = "2.2"
                    counts["tombstone"] += 1
                _dump(CRITERIA_DIR / f"{sr_uid}.yml", item)

    return counts


SPEC_HEADER = """\
# WCAG 2.2 — throughline source

Generated from the graph. Prose between `tl:item` / `tl:table` markers is injected by
`tl docs` — edit the YAML items (or `tools/wcag-2.2.json` + `tools/generate.py`), not the
injected regions.

The "why" spine is **multi-root by design**: WCAG's four Principles are four distinct
reasons — four root `intent`s, not one umbrella. Each Guideline is a `user_requirement`
that `derives_from` its principle and carries its own `rationale`; each Success Criterion
is a `system_requirement` that `implements` its guideline, with the W3C "Intent of this
Success Criterion" as its `rationale`. The WCAG number lives in `attrs.source_ref`
(`"1.4.3"`), the grade in `attrs.level`, and the version that introduced it in
`attrs.wcag_version` — so one graph carries WCAG 2.0, 2.1 and 2.2 at once. 4.1.1 Parsing,
removed in 2.2, is kept as a tombstone.

## The four principles — the roots

<!-- tl:item INT-0001 -->
<!-- tl:end -->

<!-- tl:item INT-0002 -->
<!-- tl:end -->

<!-- tl:item INT-0003 -->
<!-- tl:end -->

<!-- tl:item INT-0004 -->
<!-- tl:end -->
"""


def generate_spec() -> None:
    ur_ref = _scan(GUIDELINES_DIR)  # gref -> UR uid
    parts = [SPEC_HEADER]
    for p in WCAG["principles"]:
        parts.append(f"# Principle {p['num']}: {p['handle']}\n")
        for g in p["guidelines"]:
            parts.append(f"## {g['num']} {g['handle']}\n")
            parts.append(f"<!-- tl:item {ur_ref[g['num']]} -->\n<!-- tl:end -->\n")
            flt = ("type == 'system_requirement' and "
                   f"attrs.get('source_ref').startswith('{g['num']}.')")
            parts.append(f"<!-- tl:table {flt} -->\n<!-- tl:end -->\n")
    SPEC.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    c = generate()
    generate_spec()
    print(f"intents:    {c['int']} new (principles)")
    print(f"guidelines: {c['ur']} new (user_requirements)")
    print(f"criteria:   {c['sr']} new (system_requirements), {c['tombstone']} tombstoned")
    print(f"totals: {len(list(INTENTS_DIR.glob('INT-*.yml')))} INT, "
          f"{len(list(GUIDELINES_DIR.glob('UR-*.yml')))} UR, "
          f"{len(list(CRITERIA_DIR.glob('SR-*.yml')))} SR")
    print("next: run `tl docs` to inject content, then `tl check --strict`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
