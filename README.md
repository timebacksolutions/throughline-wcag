# throughline-wcag

The **Web Content Accessibility Guidelines (WCAG)** expressed as a
[throughline](https://pypi.org/project/throughline/) **source** — a standalone, grounded
requirements graph that a consuming project composes with
[throughline-compose](https://github.com/timebacksolutions/throughline-compose).

Each published WCAG version is a separate **edition on its own branch** (see *Editions are
branches* below); the live counts and [`docs/spec.md`](docs/spec.md) reflect whichever
branch you are viewing — `main` is WCAG 2.2.

This repository holds no application code. It is a directory of small YAML items with
permanent UIDs, validated by `tl check`. Consumers import it under a namespace and
reference its criteria as `wcag:SR-0019`.

## Status

A grounded graph of
<!-- tl:count type == 'intent' -->
4
<!-- tl:end --> principle intents,
<!-- tl:count type == 'user_requirement' -->
13
<!-- tl:end --> guideline requirements and
<!-- tl:count type == 'system_requirement' -->
86
<!-- tl:end --> success criteria, published to [`docs/spec.md`](docs/spec.md). The counts
are rendered from the live graph by `tl:count`, so they cannot drift.

## Why this source is multi-root

A throughline source gets **as many root intents as the standard has genuine "why"s** — a
single umbrella root would throw away the reason each criterion exists, which is the whole
point of IDD. WCAG's structure gives four distinct reasons, so this graph has **four
co-equal root intents** (all `normative: false`):

| Root | Principle |
|---|---|
| `INT-0001` | **Perceivable** — content is available to a sense the user has |
| `INT-0002` | **Operable** — the interface can be operated by any input method |
| `INT-0003` | **Understandable** — information and operation make sense |
| `INT-0004` | **Robust** — content survives across user agents and assistive tech |

- Each of WCAG's **guidelines** is a `user_requirement` that `derives_from` **its own
  principle** (not a catch-all), and carries a `rationale` — who it serves and why (the
  count is in *Status* above — 13 in 2.1/2.2, 12 in 2.0, which lacks Input Modalities).
- Each **success criterion** is a `system_requirement` that `implements` its guideline.
  Its `rationale` is the W3C **"Intent of this Success Criterion"** — the leaf-level *why*.
  WCAG's hierarchy is strict (one principle per guideline), so a criterion grounds up to a
  principle through `implements` → `derives_from` with no extra edge.

## Editions are branches — one version per ref

Each published WCAG version is a **complete, separate standard**, exactly as ASVS v5.0.0 is
a whole standard rather than "ASVS v4 plus a version attribute". WCAG 2.2 incorporates
criteria first published in 2.0 and 2.1, but a user of WCAG 2.2 wants *the WCAG 2.2 edition*
— not two versions overlaid and filtered apart. So this source cuts each version onto its
own branch, and a consumer selects the edition it wants by **pinning a git ref**:

| Edition | Branch | Tag | Live criteria |
|---|---|---|---|
| WCAG 2.2 | `main` | `v2.2.x` | 86 |
| WCAG 2.1 | `release/2.1` | `v2.1.0` | 78 |
| WCAG 2.0 | `release/2.0` | `v2.0.0` | 61 |

A branch holds **exactly its version's items** — no version attribute to filter on, no
removed-criteria to skip. The facets that remain are genuine *sub-filters within* an
edition, never selectors for it:

- `attrs.level` — the conformance grade (`A` / `AA` / `AAA`), used to pick a target such
  as "WCAG 2.2 AA".
- `attrs.source_ref` — the published WCAG number (`1.4.3`), never the UID.
- `attrs.wcag_version` — **provenance only**: the version that first introduced the
  criterion, so a reader can see "this first appeared in 2.1". It is *not* how you select an
  edition; the ref is.

**UIDs are stable across editions.** The release branches are cut from `main`, so a
criterion shared by two versions keeps the same UID in both (`1.4.3` is `SR-0019`
everywhere it appears). 4.1.1 Parsing, retired in 2.2, remains a throughline **tombstone**
(`status: deleted`) on `main` — throughline never erases a retired UID — and is live on the
2.0/2.1 editions where the criterion belongs.

**A future WCAG 3.0** (a different model, not an additive revision) would branch the same
way — `main` advances to it, `release/2.2` preserves this edition — the same
release-branch-per-edition model `throughline-asvs` uses for v4 → v5.

## Modelling conventions

- **throughline UIDs are this source's own** (`SR-0019`…), immutable and never the WCAG
  number. The WCAG number lives in `attrs.source_ref`.
- **Success-criterion `text`** is the criterion's normative statement; **`rationale`** is
  its published Intent. Both come from the authoritative W3C sources (see NOTICE).
- The graph is generated from the vendored canonical JSON by `tools/generate.py`, which cuts
  a single edition — the version in `tools/EDITION` (`2.2` on `main`) — keeping permanent
  UIDs and pruning any criterion the version doesn't publish. Editing the spec means editing
  the data + generator, not the YAML by hand.

## Composing it

In a consuming project's `throughline.toml`:

```toml
[sources.wcag]
url = "https://github.com/timebacksolutions/throughline-wcag"
ref = "v2.2.2"        # or v2.1.0 / v2.0.0 for an earlier edition
```

Then reference a criterion as `wcag:SR-0019` (Contrast Minimum) from your own items.

## Licence

Repository structure, tooling and configuration: Apache-2.0 (see `LICENSE`). The WCAG
criterion text and Intent paragraphs are © W3C, reused under the W3C Document License with
attribution — see `NOTICE`. Authoritative source: https://www.w3.org/TR/WCAG22/.
