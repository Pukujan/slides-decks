# slides-decks — editorial creative harness

A versioned, **candidate** LLM harness for story-led slide decks: editorial taste, narrative choices, language constraints, illustration grammar, agent-role routing, explicit approvals and regression review.

### Start with [START_HERE.md](START_HERE.md)

**New ChatGPT session?** Provide your new story *and* paste the starter prompt from **[harness/prompts/starter/v0.1.0.md](harness/prompts/starter/v0.1.0.md)**. Merely sharing a repository URL does not automatically load or execute the harness.

The first response should analyze the story and, where useful, ask up to three specific clarifying questions. **No slides, PDF, images or PPTX during intake.** Story, copy, storyboard, render and release require separate approvals. See [router](harness/router/state-machine.v0.1.0.json) and [lookback rules](harness/router/rules.v0.1.0.md).

### Source of truth
The [eight-page Golden A–Folio PDF v0.1](transcripts/6ac92692-6758-83e9-b1bf-17dc695462a0/attachments/agent_figures_A_Folio(3).pdf) is a **visual/editorial exemplar**, not a fixed eight-slide template. The old editable PPTX is still broken and is **not** a validated brand exemplar.

### Modules and versioning
Individual modules: [intake](harness/modules/intake/v0.1.0.md), [scope](harness/modules/scope/v0.1.0.md), [narrative](harness/modules/narrative/v0.1.0.md), [language](harness/modules/language/v0.1.0.md), [brand](harness/modules/brand/v0.1.0.md), [illustration](harness/modules/illustration/v0.1.0.md), [exemplars](harness/modules/exemplars/v0.1.0.md), [critic](harness/modules/critic/v0.1.0.md).

Versions and Git blob SHAs are frozen in **[harness/lock.json](harness/lock.json)**. Do not mutate versioned packages in place. GitHub Actions checks integrity and routing rules.

### Validation status
- Prior five PDF-generation trials: completed, **not golden-validated**, repetitive composition and typography issues remain.
- Package integrity / router tests: automated CI.
- Single-session story-intake dry run: [read findings](harness/evals/intake-dry-run.v0.1.0.md).
- **Independent fresh-session creative behavior: NOT YET TESTED.**
- **Human approval of harness: PENDING.**

Read [harness/evals/README.md](harness/evals/README.md) before claiming this harness is production-ready.
