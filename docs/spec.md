# WCAG 2.2 — throughline source

Generated from the graph. Prose between `tl:item` / `tl:table` markers is injected by
`tl docs` — edit the YAML items (or `tools/wcag-2.2.json` + `tools/generate.py`), not the
injected regions.

This branch is the **complete WCAG 2.2 edition** — every Success Criterion that
version publishes, and nothing else. WCAG 2.2 incorporates criteria first introduced
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
**INT-0001 — Perceivable — Information and user interface components must be presentable to users in ways they can perceive.** — `intent`, status `approved`

> Users can perceive the information and interface: content is available to sight, hearing or touch so no one is excluded because a single sense — for example vision or hearing — is unavailable to them. Information is never conveyed in a form only one sense can access.

**source_ref**: Principle 1
<!-- tl:end -->

<!-- tl:item INT-0002 -->
**INT-0002 — Operable — User interface components and navigation must be operable.** — `intent`, status `approved`

> Users can operate the interface and navigate the content whatever their input method — keyboard, pointer, voice, switch or assistive technology — and however much time, dexterity or precision they can bring, so no interaction demands an action a user cannot perform.

**source_ref**: Principle 2
<!-- tl:end -->

<!-- tl:item INT-0003 -->
**INT-0003 — Understandable — Information and the operation of the user interface must be understandable.** — `intent`, status `approved`

> Users can understand both the information presented and how to operate the interface: content is readable and predictable and the system helps people avoid and recover from mistakes, so users with cognitive, learning or language differences are not shut out.

**source_ref**: Principle 3
<!-- tl:end -->

<!-- tl:item INT-0004 -->
**INT-0004 — Robust — Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies.** — `intent`, status `approved`

> Content is coded so a wide range of user agents, including current and future assistive technologies, can reliably interpret it — so accessibility survives changes in browsers and tools rather than breaking as technology evolves.

**source_ref**: Principle 4
<!-- tl:end -->

# Principle 1: Perceivable

## 1.1 Text Alternatives

<!-- tl:item UR-0001 -->
**UR-0001 — Text Alternatives — Provide text alternatives for any non-text content so that it can be changed into other forms people need, such as large print, braille, speech, symbols or simpler language.** — `user_requirement`, status `approved`

> Provide text alternatives for any non-text content so that it can be changed into other forms people need, such as large print, braille, speech, symbols or simpler language.

*Rationale:* Text can be rendered as speech, braille, enlarged print or symbols, so non-text content reaches people who cannot see or process images.

*Derives from:* INT-0001

**source_ref**: 1.1
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('1.1.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0001 | system_requirement | approved | Non-text Content (A) |
<!-- tl:end -->

## 1.2 Time-based Media

<!-- tl:item UR-0002 -->
**UR-0002 — Time-based Media — Provide alternatives for time-based media.** — `user_requirement`, status `approved`

> Provide alternatives for time-based media.

*Rationale:* Audio and video carry information some users cannot hear or see; captions, descriptions and transcripts make that information available to everyone.

*Derives from:* INT-0001

**source_ref**: 1.2
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('1.2.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0002 | system_requirement | approved | Audio-only and Video-only (Prerecorded) (A) |
| SR-0003 | system_requirement | approved | Captions (Prerecorded) (A) |
| SR-0004 | system_requirement | approved | Audio Description or Media Alternative (Prerecorded) (A) |
| SR-0005 | system_requirement | approved | Captions (Live) (AA) |
| SR-0006 | system_requirement | approved | Audio Description (Prerecorded) (AA) |
| SR-0007 | system_requirement | approved | Sign Language (Prerecorded) (AAA) |
| SR-0008 | system_requirement | approved | Extended Audio Description (Prerecorded) (AAA) |
| SR-0009 | system_requirement | approved | Media Alternative (Prerecorded) (AAA) |
| SR-0010 | system_requirement | approved | Audio-only (Live) (AAA) |
<!-- tl:end -->

## 1.3 Adaptable

<!-- tl:item UR-0003 -->
**UR-0003 — Adaptable — Create content that can be presented in different ways (for example simpler layout) without losing information or structure.** — `user_requirement`, status `approved`

> Create content that can be presented in different ways (for example simpler layout) without losing information or structure.

*Rationale:* When structure and relationships are encoded programmatically, content can be presented in different ways — spoken, reflowed, restyled — without losing meaning.

*Derives from:* INT-0001

**source_ref**: 1.3
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('1.3.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0011 | system_requirement | approved | Info and Relationships (A) |
| SR-0012 | system_requirement | approved | Meaningful Sequence (A) |
| SR-0013 | system_requirement | approved | Sensory Characteristics (A) |
| SR-0014 | system_requirement | approved | Orientation (AA) |
| SR-0015 | system_requirement | approved | Identify Input Purpose (AA) |
| SR-0016 | system_requirement | approved | Identify Purpose (AAA) |
<!-- tl:end -->

## 1.4 Distinguishable

<!-- tl:item UR-0004 -->
**UR-0004 — Distinguishable — Make it easier for users to see and hear content including separating foreground from background.** — `user_requirement`, status `approved`

> Make it easier for users to see and hear content including separating foreground from background.

*Rationale:* Users with low vision, colour blindness or hearing difficulty need enough contrast, control over audio and resizable text to separate content from its surroundings.

*Derives from:* INT-0001

**source_ref**: 1.4
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('1.4.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0017 | system_requirement | approved | Use of Color (A) |
| SR-0018 | system_requirement | approved | Audio Control (A) |
| SR-0019 | system_requirement | approved | Contrast (Minimum) (AA) |
| SR-0020 | system_requirement | approved | Resize Text (AA) |
| SR-0021 | system_requirement | approved | Images of Text (AA) |
| SR-0022 | system_requirement | approved | Contrast (Enhanced) (AAA) |
| SR-0023 | system_requirement | approved | Low or No Background Audio (AAA) |
| SR-0024 | system_requirement | approved | Visual Presentation (AAA) |
| SR-0025 | system_requirement | approved | Images of Text (No Exception) (AAA) |
| SR-0026 | system_requirement | approved | Reflow (AA) |
| SR-0027 | system_requirement | approved | Non-text Contrast (AA) |
| SR-0028 | system_requirement | approved | Text Spacing (AA) |
| SR-0029 | system_requirement | approved | Content on Hover or Focus (AA) |
<!-- tl:end -->

# Principle 2: Operable

## 2.1 Keyboard Accessible

<!-- tl:item UR-0005 -->
**UR-0005 — Keyboard Accessible — Make all functionality available from a keyboard.** — `user_requirement`, status `approved`

> Make all functionality available from a keyboard.

*Rationale:* Many users cannot use a mouse; all functionality must be reachable and operable from a keyboard or keyboard interface.

*Derives from:* INT-0002

**source_ref**: 2.1
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('2.1.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0030 | system_requirement | approved | Keyboard (A) |
| SR-0031 | system_requirement | approved | No Keyboard Trap (A) |
| SR-0032 | system_requirement | approved | Keyboard (No Exception) (AAA) |
| SR-0033 | system_requirement | approved | Character Key Shortcuts (A) |
<!-- tl:end -->

## 2.2 Enough Time

<!-- tl:item UR-0006 -->
**UR-0006 — Enough Time — Provide users enough time to read and use content.** — `user_requirement`, status `approved`

> Provide users enough time to read and use content.

*Rationale:* People read and act at very different speeds; users must be able to turn off, adjust or extend time limits so they are not cut off mid-task.

*Derives from:* INT-0002

**source_ref**: 2.2
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('2.2.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0034 | system_requirement | approved | Timing Adjustable (A) |
| SR-0035 | system_requirement | approved | Pause, Stop, Hide (A) |
| SR-0036 | system_requirement | approved | No Timing (AAA) |
| SR-0037 | system_requirement | approved | Interruptions (AAA) |
| SR-0038 | system_requirement | approved | Re-authenticating (AAA) |
| SR-0039 | system_requirement | approved | Timeouts (AAA) |
<!-- tl:end -->

## 2.3 Seizures and Physical Reactions

<!-- tl:item UR-0007 -->
**UR-0007 — Seizures and Physical Reactions — Do not design content in a way that is known to cause seizures or physical reactions.** — `user_requirement`, status `approved`

> Do not design content in a way that is known to cause seizures or physical reactions.

*Rationale:* Flashing content can trigger seizures; limiting flashes protects users with photosensitive epilepsy and vestibular disorders.

*Derives from:* INT-0002

**source_ref**: 2.3
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('2.3.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0040 | system_requirement | approved | Three Flashes or Below Threshold (A) |
| SR-0041 | system_requirement | approved | Three Flashes (AAA) |
| SR-0042 | system_requirement | approved | Animation from Interactions (AAA) |
<!-- tl:end -->

## 2.4 Navigable

<!-- tl:item UR-0008 -->
**UR-0008 — Navigable — Provide ways to help users navigate, find content, and determine where they are.** — `user_requirement`, status `approved`

> Provide ways to help users navigate, find content, and determine where they are.

*Rationale:* Users need ways to find content, orient themselves and know where they are — through titles, headings, focus order and visible focus — especially when they cannot scan a page visually.

*Derives from:* INT-0002

**source_ref**: 2.4
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('2.4.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0043 | system_requirement | approved | Bypass Blocks (A) |
| SR-0044 | system_requirement | approved | Page Titled (A) |
| SR-0045 | system_requirement | approved | Focus Order (A) |
| SR-0046 | system_requirement | approved | Link Purpose (In Context) (A) |
| SR-0047 | system_requirement | approved | Multiple Ways (AA) |
| SR-0048 | system_requirement | approved | Headings and Labels (AA) |
| SR-0049 | system_requirement | approved | Focus Visible (AA) |
| SR-0050 | system_requirement | approved | Location (AAA) |
| SR-0051 | system_requirement | approved | Link Purpose (Link Only) (AAA) |
| SR-0052 | system_requirement | approved | Section Headings (AAA) |
| SR-0053 | system_requirement | approved | Focus Not Obscured (Minimum) (AA) |
| SR-0054 | system_requirement | approved | Focus Not Obscured (Enhanced) (AAA) |
| SR-0055 | system_requirement | approved | Focus Appearance (AAA) |
<!-- tl:end -->

## 2.5 Input Modalities

<!-- tl:item UR-0009 -->
**UR-0009 — Input Modalities — Make it easier for users to operate functionality through various inputs beyond keyboard.** — `user_requirement`, status `approved`

> Make it easier for users to operate functionality through various inputs beyond keyboard.

*Rationale:* People operate devices in many ways beyond a keyboard — touch, pointer, voice, motion — and each must work without requiring precise or tiring gestures.

*Derives from:* INT-0002

**source_ref**: 2.5
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('2.5.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0056 | system_requirement | approved | Pointer Gestures (A) |
| SR-0057 | system_requirement | approved | Pointer Cancellation (A) |
| SR-0058 | system_requirement | approved | Label in Name (A) |
| SR-0059 | system_requirement | approved | Motion Actuation (A) |
| SR-0060 | system_requirement | approved | Target Size (Enhanced) (AAA) |
| SR-0061 | system_requirement | approved | Concurrent Input Mechanisms (AAA) |
| SR-0062 | system_requirement | approved | Dragging Movements (AA) |
| SR-0063 | system_requirement | approved | Target Size (Minimum) (AA) |
<!-- tl:end -->

# Principle 3: Understandable

## 3.1 Readable

<!-- tl:item UR-0010 -->
**UR-0010 — Readable — Make text content readable and understandable.** — `user_requirement`, status `approved`

> Make text content readable and understandable.

*Rationale:* Text must be readable and its language machine-identifiable so assistive technology can pronounce it and users can understand unusual words and abbreviations.

*Derives from:* INT-0003

**source_ref**: 3.1
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('3.1.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0064 | system_requirement | approved | Language of Page (A) |
| SR-0065 | system_requirement | approved | Language of Parts (AA) |
| SR-0066 | system_requirement | approved | Unusual Words (AAA) |
| SR-0067 | system_requirement | approved | Abbreviations (AAA) |
| SR-0068 | system_requirement | approved | Reading Level (AAA) |
| SR-0069 | system_requirement | approved | Pronunciation (AAA) |
<!-- tl:end -->

## 3.2 Predictable

<!-- tl:item UR-0011 -->
**UR-0011 — Predictable — Make web pages appear and operate in predictable ways.** — `user_requirement`, status `approved`

> Make web pages appear and operate in predictable ways.

*Rationale:* Interfaces that behave consistently and change only when the user expects it let people with cognitive differences build reliable mental models.

*Derives from:* INT-0003

**source_ref**: 3.2
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('3.2.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0070 | system_requirement | approved | On Focus (A) |
| SR-0071 | system_requirement | approved | On Input (A) |
| SR-0072 | system_requirement | approved | Consistent Navigation (AA) |
| SR-0073 | system_requirement | approved | Consistent Identification (AA) |
| SR-0074 | system_requirement | approved | Change on Request (AAA) |
| SR-0075 | system_requirement | approved | Consistent Help (A) |
<!-- tl:end -->

## 3.3 Input Assistance

<!-- tl:item UR-0012 -->
**UR-0012 — Input Assistance — Help users avoid and correct mistakes.** — `user_requirement`, status `approved`

> Help users avoid and correct mistakes.

*Rationale:* Everyone makes mistakes; clear labels, error identification, suggestions and prevention help users avoid and recover from them, especially on legal, financial or data submissions.

*Derives from:* INT-0003

**source_ref**: 3.3
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('3.3.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0076 | system_requirement | approved | Error Identification (A) |
| SR-0077 | system_requirement | approved | Labels or Instructions (A) |
| SR-0078 | system_requirement | approved | Error Suggestion (AA) |
| SR-0079 | system_requirement | approved | Error Prevention (Legal, Financial, Data) (AA) |
| SR-0080 | system_requirement | approved | Help (AAA) |
| SR-0081 | system_requirement | approved | Error Prevention (All) (AAA) |
| SR-0082 | system_requirement | approved | Redundant Entry (A) |
| SR-0083 | system_requirement | approved | Accessible Authentication (Minimum) (AA) |
| SR-0084 | system_requirement | approved | Accessible Authentication (Enhanced) (AAA) |
<!-- tl:end -->

# Principle 4: Robust

## 4.1 Compatible

<!-- tl:item UR-0013 -->
**UR-0013 — Compatible — Maximize compatibility with current and future user agents, including assistive technologies.** — `user_requirement`, status `approved`

> Maximize compatibility with current and future user agents, including assistive technologies.

*Rationale:* Content must expose correct name, role, value and status to assistive technologies so it keeps working across browsers, devices and future tools.

*Derives from:* INT-0004

**source_ref**: 4.1
<!-- tl:end -->

<!-- tl:table type == 'system_requirement' and attrs.get('source_ref').startswith('4.1.') -->
| UID | Type | Status | Title |
|---|---|---|---|
| SR-0086 | system_requirement | approved | Name, Role, Value (A) |
| SR-0087 | system_requirement | approved | Status Messages (AA) |
<!-- tl:end -->

