# Candidate intake-to-story-gate dry run · v0.1.0
**Status:** one *authored, same-session dry run* against an unrelated example. NOT a fresh-session LLM experiment and NOT a demonstration of automatic multi-agent enforcement. Used to test clarity of intake behavior and to exercise the router's intended gates.

### Input (case: library_storm)
"A neighborhood library's volunteers reportedly reopened a room of water-damaged books by sunrise after a storm. One person estimates 800 books were rescued. No date or supporting report. Create a LinkedIn editorial carousel."

### Proposed INTAKE response
> This could become a story about a community racing a clock, but "reopened by sunrise" and "800 books" are not yet verified. Before selecting the angle:
>
> 1. Is the 800 figure from an inventory or a rough volunteer estimate?
> 2. Was the room reopened **to the public**, or simply accessible to staff, and when did the event happen?
> 3. Who should tell the story and who should read it—library staff, neighbors, donors or other readers?
>
> I haven't storyboarded or generated anything yet. Current state: `intake`; next: `clarification`.

**Intake review:** avoids unsupported certainty, poses three consequential questions, no design output. This conforms to the intake *content rubric*. A new independent model could still fail.

### Hypothetical clarification answers (test data, not facts)
"800 is a rough estimate from volunteers. By sunrise the room was usable by staff, not open to visitors. Audience is local community members; narrator is a volunteer coordinator. We want to honor the overnight team."

### Proposed NARRATIVE OPTIONS response
**A — An overnight rescue:** readers follow concrete decisions under time pressure; the reveal is what could be saved, carefully attributing rough figures.
**B — A room brought back to life:** begin with one flooded room, show collective work, end with the community meaning rather than a generic lesson.
**C — The volunteer's viewpoint:** center the person making the first tough choice and the small acts of coordination.

**Human decision requested:** choose the narrative emphasis and acceptable claim language. No fixed eight-slide structure and no rendering. State becomes `human_story_gate`.

### Router gate observations
- `intake → clarification`: allowed.
- `clarification → intake`: blocked until answers recorded.
- `intake → narrative_options → human_story_gate`: allowed after context.
- `human_story_gate → copy`: blocked without `story_ok` attached to the chosen angle.
- `human_story_gate → copy`: allowed by validator once an explicit, scoped `story_ok` token is present.
- Even after story approval, **render is not allowed** without copy, storyboard and separate render approvals.

### Remaining work
Execute this test on an actually fresh ChatGPT session with repo access; score its *real* first response, its questions, handling of answers and pause at approval. Test a different story for full visual output, including golden page inspection, figure consistency, critique and targeted rollback. Current tests do not demonstrate that the LLM can or will obey the protocol autonomously.
