#!/usr/bin/env python3
"""Generate a single-version WCAG throughline source from the W3C canonical JSON.

WCAG publishes a canonical machine-readable serialisation — vendored here at
``tools/wcag-2.2.json`` (from https://www.w3.org/WAI/WCAG22/wcag.json), which carries, per
Success Criterion, the set of WCAG versions it belongs to. This script turns *one* version
into throughline items.

**Each published WCAG version is a complete, separate edition — selected by ref, not by an
attribute.** WCAG 2.2 contains items first published in 2.0 and 2.1, but it is a whole
standard in its own right, exactly as ASVS v5.0.0 is. A consumer picks the edition it wants
by pinning a git ref (``v2.2.x`` on ``main``, ``v2.1.0`` on ``release/2.1``,
``v2.0.0`` on ``release/2.0``) and gets *only* that version's items — no version attribute
to filter on, no removed-criteria tombstones to skip. The edition to build is read from
``tools/EDITION`` (or ``argv[1]``).

**The "why" spine is genuinely multi-root — the point of putting WCAG on the list.**
WCAG's four Principles (Perceivable, Operable, Understandable, Robust) are four *distinct*
reasons content must behave, so they are **four root intents** (INT-0001..INT-0004), not
one umbrella. Each Guideline is a ``user_requirement`` that ``derives_from`` its own
principle; each Success Criterion is a ``system_requirement`` that ``implements`` its
guideline. WCAG's hierarchy is strict (each guideline sits under exactly one principle), so
grounding a criterion to a principle needs no extra edge. The leaf *why* is preserved: every
criterion's ``rationale`` is the W3C "Intent of this Success Criterion" lead paragraph.

**UIDs are permanent and stable across editions.** The mapping from a
principle/guideline/criterion to a throughline UID is keyed by ``attrs.source_ref`` (the
WCAG number: ``"Principle 1"``, ``"1.4"``, ``"1.4.3"``) and read from the items already on
disk. A criterion shared by two editions keeps the same UID in both, because the release
branches are cut from ``main`` and inherit its allocation; anything without an item yet gets
a freshly allocated UID in document order. When building a version, items whose source_ref
is absent from that version are **deleted** from the edition — the branch holds exactly the
criteria that version publishes.

``attrs.wcag_version`` records the version that *introduced* each criterion, as provenance
only — a reader can see "this first appeared in 2.1" — never as the mechanism for selecting a
version. That is what the ref is for.

Usage:  python tools/generate.py [VERSION]   (VERSION defaults to tools/EDITION, then "2.2")
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
INTENTS_DIR = REPO / "intents"        # intent (principle roots), prefix INT
GUIDELINES_DIR = REPO / "guidelines"  # user_requirement, prefix UR
CRITERIA_DIR = REPO / "criteria"      # system_requirement, prefix SR
SPEC = REPO / "docs" / "spec.md"
EDITION_FILE = TOOLS / "EDITION"

WCAG = json.loads((TOOLS / "wcag-2.2.json").read_text(encoding="utf-8"))
INTENTS = json.loads((TOOLS / "understanding_intents.json").read_text(encoding="utf-8"))

VERSION_ORDER = {"2.0": 0, "2.1": 1, "2.2": 2}

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


def edition() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    if EDITION_FILE.exists():
        return EDITION_FILE.read_text(encoding="utf-8").strip()
    return "2.2"


def strip(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _dump(path: Path, item: dict) -> None:
    path.write_text(
        yaml.safe_dump(item, sort_keys=False, allow_unicode=True, width=90),
        encoding="utf-8",
    )


def _items(dir_: Path):
    """Yield (path, data) for every real item file, skipping dir manifests (.register.yml)."""
    for f in dir_.glob("*.yml"):
        if f.name.startswith("."):
            continue
        yield f, yaml.safe_load(f.read_text(encoding="utf-8"))


def _scan(dir_: Path, include_deleted: bool = False) -> dict[str, str]:
    """Map source_ref -> uid for live items (tombstones excluded unless asked)."""
    ref2uid: dict[str, str] = {}
    for _, data in _items(dir_):
        if not include_deleted and data.get("status") == "deleted":
            continue
        ref = (data.get("attrs") or {}).get("source_ref")
        if ref:
            ref2uid[ref] = data["uid"]
    return ref2uid


def _high_water(dir_: Path, prefix: str) -> int:
    """Highest UID number ever used in this register, INCLUDING tombstones — a retired
    UID is never handed out again."""
    return max((int(data["uid"].split("-")[1]) for _, data in _items(dir_)
               if data["uid"].startswith(prefix + "-")), default=0)


def _prune(dir_: Path, keep_refs: set[str]) -> int:
    """Delete items whose source_ref is not published by this edition. A tombstone
    (status: deleted) is a permanent death-record and is never erased."""
    removed = 0
    for f, data in _items(dir_):
        if data.get("status") == "deleted":
            continue
        if (data.get("attrs") or {}).get("source_ref") not in keep_refs:
            f.unlink()
            removed += 1
    return removed


def generate(version: str) -> dict[str, int]:
    int_ref = _scan(INTENTS_DIR)
    ur_ref = _scan(GUIDELINES_DIR)
    sr_ref = _scan(CRITERIA_DIR)
    n_int = _high_water(INTENTS_DIR, "INT") + 1
    n_ur = _high_water(GUIDELINES_DIR, "UR") + 1
    n_sr = _high_water(CRITERIA_DIR, "SR") + 1

    counts = {"int": 0, "ur": 0, "sr": 0}
    keep_int: set[str] = set()
    keep_ur: set[str] = set()
    keep_sr: set[str] = set()

    for p in WCAG["principles"]:
        # A guideline is in this edition iff it has at least one criterion in this version.
        present_guidelines = [
            g for g in p["guidelines"]
            if any(version in sc["versions"] for sc in g["successcriteria"])
        ]
        if not present_guidelines:
            continue

        pref = f"Principle {p['num']}"
        keep_int.add(pref)
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

        for g in present_guidelines:
            gref = g["num"]
            keep_ur.add(gref)
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
                if version not in sc["versions"]:
                    continue
                num = sc["num"]
                keep_sr.add(num)
                sr_uid = sr_ref.get(num)
                if sr_uid is None:
                    sr_uid = f"SR-{n_sr:04d}"; n_sr += 1; sr_ref[num] = sr_uid; counts["sr"] += 1
                introduced = min(sc["versions"], key=lambda v: VERSION_ORDER[v])
                level = sc["level"] or "A"
                _dump(CRITERIA_DIR / f"{sr_uid}.yml", {
                    "uid": sr_uid,
                    "type": "system_requirement",
                    "status": "approved",
                    "title": f"{sc['handle']} ({level})",
                    "text": strip(sc["content"]) or strip(sc["title"]),
                    "rationale": INTENTS.get(num, ""),
                    "links": [{"target": ur_uid, "type": "implements"}],
                    "attrs": {"source_ref": num, "level": level, "wcag_version": introduced},
                })

    counts["pruned"] = (_prune(INTENTS_DIR, keep_int)
                        + _prune(GUIDELINES_DIR, keep_ur)
                        + _prune(CRITERIA_DIR, keep_sr))
    return counts


SPEC_HEADER = """\
# WCAG {version} — throughline source

Generated from the graph. Prose between `tl:item` / `tl:table` markers is injected by
`tl docs` — edit the YAML items (or `tools/wcag-2.2.json` + `tools/generate.py`), not the
injected regions.

This branch is the **complete WCAG {version} edition** — every Success Criterion that
version publishes, and nothing else. WCAG {version} incorporates criteria first introduced
in earlier versions, but it is a whole standard in its own right (as ASVS v5.0.0 is): a
consumer selects it by pinning this ref, not by filtering a version attribute. Other WCAG
versions live on their own branches (`main` = 2.2, `release/2.1`, `release/2.0`).

The "why" spine is **multi-root by design**: WCAG's four Principles are four distinct
reasons — four root `intent`s, not one umbrella. Each Guideline is a `user_requirement`
that `derives_from` its principle and carries its own `rationale`; each Success Criterion
is a `system_requirement` that `implements` its guideline, with the W3C "Intent of this
Success Criterion" as its `rationale`. The WCAG number lives in `attrs.source_ref`
(`"1.4.3"`), the grade in `attrs.level`, and the version that first introduced the
criterion in `attrs.wcag_version` — provenance only, never a selector.

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


def generate_spec(version: str) -> None:
    int_ref = _scan(INTENTS_DIR)
    ur_ref = _scan(GUIDELINES_DIR)
    parts = [SPEC_HEADER.format(version=version)]
    for p in WCAG["principles"]:
        if f"Principle {p['num']}" not in int_ref:
            continue
        parts.append(f"# Principle {p['num']}: {p['handle']}\n")
        for g in p["guidelines"]:
            if g["num"] not in ur_ref:
                continue
            parts.append(f"## {g['num']} {g['handle']}\n")
            parts.append(f"<!-- tl:item {ur_ref[g['num']]} -->\n<!-- tl:end -->\n")
            flt = ("type == 'system_requirement' and "
                   f"attrs.get('source_ref').startswith('{g['num']}.')")
            parts.append(f"<!-- tl:table {flt} -->\n<!-- tl:end -->\n")
    SPEC.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    version = edition()
    if version not in VERSION_ORDER:
        print(f"unknown WCAG version {version!r}; expected one of {sorted(VERSION_ORDER)}")
        return 2
    c = generate(version)
    generate_spec(version)
    print(f"edition: WCAG {version}")
    print(f"intents:    {c['int']} new (principles)")
    print(f"guidelines: {c['ur']} new (user_requirements)")
    print(f"criteria:   {c['sr']} new (system_requirements)")
    print(f"pruned:     {c['pruned']} item(s) not in this edition")
    print(f"totals: {len(list(INTENTS_DIR.glob('INT-*.yml')))} INT, "
          f"{len(list(GUIDELINES_DIR.glob('UR-*.yml')))} UR, "
          f"{len(list(CRITERIA_DIR.glob('SR-*.yml')))} SR")
    print("next: run `tl docs` to inject content, then `tl check --strict`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
