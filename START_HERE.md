# Start here — editorial slide-deck harness

**Current release:** [candidate v0.1](harness/lock.json). **Golden artifact:** [A–Folio v0.1 PDF](transcripts/6ac92692-6758-83e9-b1bf-17dc695462a0/attachments/agent_figures_A_Folio(3).pdf). **Known problem:** the corresponding PPTX needs repair; it is *not* the visual source of truth.

## What this does
This is a modular context + prompt + critic + state-routing system for generating **new stories** with a consistent editorial identity, strong narrative judgment, and controlled iteration. The output is not a deterministic eight-slide template. It should transfer creative taste, not copy the old story.

## Quick start for a fresh ChatGPT session
1. In a new session with access to this repository, paste the **starter prompt** from [harness/prompts/starter/v0.1.0.md](harness/prompts/starter/v0.1.0.md), together with your new story (and sources if available). Alternatively provide the repo URL and explicitly ask it to read these files.
2. The first turn **must be INTAKE**: understand context, classify claims, identify uncertainty, ask at most 3 specific questions that materially change the story or audience outcome. No slides or rendering.
3. After you answer, the agent proposes narrative angles; you approve an angle. Later it submits copy and storyboard for separate review and explicit authorization to render.
4. For each revision the critic records what failed, why, which state owns the defect, and which downstream approvals and checks need to be repeated.
5. Final human acceptance follows visual comparison to the *actual* golden PDF, while recognizing that **brand fidelity** is not pixel identity for a different story.

## Load order
- `harness/lock.json` (pin exact module and prompt versions).
- `harness/router/state-machine.v0.1.0.json` and `harness/router/rules.v0.1.0.md`.
- `harness/modules/scope/v0.1.0.md` and `harness/modules/intake/v0.1.0.md` at start.
- Load narrative, language, brand, illustration, exemplars and critic modules when their owners are active. Avoid overloading each turn with unrelated transcript excerpts.
- See `harness/evals/README.md` for evaluation cases and limitations.

## Independent versioning
Each package is a standalone file at `harness/modules/<name>/vX.Y.Z.md` or `harness/prompts/<name>/vX.Y.Z.md`. A run records its exact `lock.json` revision/commit before creative work begins. Changing a package means adding a *new versioned file*, updating the lock in a separate revision, and running regression checks. **Never change a file behind an existing version label.**

## What is not solved
There is no fully automated model-to-model orchestration in this repo. A ChatGPT session can follow the router as a protocol if it reads the entrypoint and cooperates; for enforcement beyond prompts, attach permissions and approval gates in an external runtime. The five prior rendered visual trials exposed repeatability failures, not an accepted reference match.

No files in this repository authorize edits to the golden PDF, broken PPTX, Google Drive, or public social accounts.
