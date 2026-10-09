# Evaluation protocol — candidate v0.1
This harness is **not accepted** until a genuinely fresh ChatGPT session receives a *new* story, obeys intake clarification without rendering, honors all human gates, and undergoes visual critique after authorized generation.

## Tests that can run today
- `node harness/evals/static_checks.v0.1.0.mjs`: validates locked Git blobs, golden PDF blob, existence/versions, legal router transitions, approval and lookback controls. No third-party packages.
- `node harness/evals/router_tests.v0.1.0.mjs`: tests expected allowed and forbidden transitions.
- `harness/evals/intake_cases.v0.1.0.json`: fresh-topic test cases and **expected behavior**, not prerecorded model answers.
- Historical five-trial report: `trials-01-05.v0.1.0.md` (older generated PDFs outside GitHub; they are NOT positive exemplars).

## Fresh-session acceptance test
1. Create a new ChatGPT session. Supply repo URL, starter prompt, and **one new story with sources**.
2. First response should surface the specific tension, distinguish facts/inferences and ask 1–3 pertinent questions (unless all important answers already exist). **Zero slides/exports.**
3. Provide answers; expect distinct narrative angles and a human choice gate. Verify it does not silently advance.
4. Approve angle, then approve copy and storyboard **separately**. Verify no rendering before explicit render approval.
5. Authorize draft generation. Review story, voice, illustration, layout, scope separately and request one narrowly scoped edit.
6. Observe legal lookback, approval invalidation and full/targeted regression. Compare render to **actual golden PDF** for brand grammar and to previous accepted candidate for regressions.
7. Record failures, exact package versions, and human verdict. **Do not say PASS merely because static tests pass.**

## Scoring
Pass criteria: materially relevant questions, factual humility, distinct angles, zero early artifacts, observed approval gates, faithful editorial brand with non-mechanical composition, coherent illustrations, no generic audit language, targeted revision and honest regression. Any unauthorized rendering or overclaiming actual-golden comparison is a blocking failure.

### Status limitations
Router state validator runs, but it cannot compel ChatGPT to read the repo or ask good questions by itself. It enforces transitions **only when integrated into an actual orchestrator**. Fresh-session human evaluation and visual matching against golden pages are pending. PPTX repair is out of scope.
