# Routing, lookback & regression contract — v0.1.0

## Agent collaboration
The owner of a state is a **logical responsibility**; a single ChatGPT session may perform multiple roles by loading the pinned context. There is no automatic separate-model process. The governor records current state, exact approved artifact revisions and allowed next transitions. Specialists cannot self-promote to later states.

**Intake → clarification** if decisive questions remain. **Clarification → intake** only after user answers or approves explicit assumptions; avoid asking the same questions twice. If no blocking gaps, **intake → narrative_options**. The narrative agent offers alternatives and **stops at human_story_gate**.

Story approval is necessary before copy. Copy must pass critic and human-copy gate before storyboard. Human storyboard approval and separate `render_ok` are both required before generation. The critic must not repair work without permission.

## When an agent may look back
**Read-only consultation** of locked exemplars and approved decisions is always permitted for relevance. **Editing backward** requires one of: human reopens scope; specific critic evidence of a defect; fact/source correction; package/version change. Critic attaches defect ticket and points to the earliest *responsible* upstream state. Never reflexively rewrite all upstream states.

- Truth/source issue → context/intake or narrative, invalidate story, copy, storyboard and rendering approvals.
- Story sequencing issue → narrative options; reopen story and dependent stages.
- Incorrect or unnatural wording → copy; invalidate copy and later approvals if semantics change.
- Visual concept/metaphor failure → storyboard or illustration; preserve accepted copy.
- Spacing/clipping/production error → composition/render; preserve approved story and figures if possible.
- Broken character grammar → illustration; preserve unrelated slides and copy.
- Scope violation → governor stops and seeks explicit revised authorization.

## Regression
Always compare the new revision to (a) the **actual** A–Folio golden PDF for editorial-brand grammar, and (b) the **previous accepted draft** to detect regressions in unchanged areas. For a different story, **do not demand pixel identity**. Inspect every new/affected page at mobile size, then check narrative arc, language, figures, consistency, clipping, page count, and authorized scope.

Run a targeted regression after any alteration. Run a full multi-axis regression after package changes, story or format changes, or before final release. If the golden cannot be inspected, mark brand fidelity UNKNOWN; never say PASS. Failure routes to the owning state with defect evidence. No silent loop of generated versions.

## Version discipline
A run pins all package versions from `harness/lock.json` and records the repository commit at start. Never edit a pinned module in place. New revision -> new versioned filename -> update lock -> compare changed package effects. Keep negative exemplars from failed attempts, label them as rejected, and never silently turn a failed visual into a positive brand reference.

## Approval semantics
Approval tokens are scoped to an artifact revision, not just the word "yes." Explicit user approval is required at human gates; an assistant's claim of completion is not evidence of approval. `Go` applies only to the last specifically agreed immediate step. A gate cannot be satisfied by the same model assuming what the user intended.
