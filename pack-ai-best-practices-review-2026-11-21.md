# AI Best-Practices Review — health-interop-superpowers v0.40.2

**Reviewer:** independent expert review (read-only; no files edited, no pushes)
**Date:** 2026-11-21
**Pack:** `~/workspace/custom-skills/health-interop-superpowers/`, v0.40.2, 18 skills,
201 reference files, 457,988 tokens (tiktoken `cl100k_base`), HIGH 0 / MEDIUM 76
**External sources verified live:** Anthropic, "Skill authoring best practices"
(docs.claude.com, via mirror — third-person rule, frontmatter limits, 500-line
bodies); Anthropic, "Building agents with Skills" (claude.com engineering blog —
progressive disclosure, three tiers); obra/superpowers skill patterns (GitHub
docs mirrors — mandatory workflows, brainstorming-first, subagent-driven
development, verification-before-completion). Where two sources disagreed, the
verbatim quote with line numbers wins; no claim below rests on memory.

## Verdict

This is a well-built agentic product that faithfully implements Anthropic's
progressive-disclosure architecture and obra/superpowers' mandatory-workflow
pattern: 18 routers all under the 5,000-token cap, 201 reference files loaded
on demand, a bootstrap with triple enforcement (SessionStart hook + 
`<EXTREMELY-IMPORTANT>` + `<SUBAGENT-STOP>`), hard gates between the six steps,
a "verify live, never from memory" rule in seven routers, and a test suite
that currently passes 8/8 with 294 anchor references resolving and 0 broken
bare references out of 694 checked. The two demonstrated failures in the
school vision screening case both trace to the same structural pattern: a rule
that exists in exactly one place, or not at all. The SUSHI rebuild loop
(~20 rebuilds stuck at 85 errors) is now covered by a stop rule — but only in
one skill, only for one loop shape, with no escalation path. The expert-review
gate — the pack's central safety mechanism — has no independence requirement
at all: the same agent that built an artefact can invoke the review on itself,
and in the school case it did, recording zero findings while nine defects
existed. The top fixes are therefore not more vocabulary but enforcement:
encode reviewer independence, generalise the loop-stop rule pack-wide, and fix
the one place where the bootstrap contradicts its own router.

## HIGH

### [H1] HIGH — The expert-review gate has no independence requirement; a builder can review its own work

**Evidence.**

- `skills/process-expert-review/SKILL.md:3` (description): "Nothing reaches the
  user for validation without the expert reviewer's approval."
- `skills/process-expert-review/SKILL.md:168-170` (`<HARD-GATE>`): "Nothing
  reaches the user for validation without the expert reviewer's approval. A
  review that finds critical or high findings blocks presentation until they
  are fixed and re-reviewed."
- `skills/using-health-interop/SKILL.md:89` (bootstrap): "After each important
  task, run `process-expert-review` and get its approval before presenting
  anything to the user for validation."
- Grep for `independent|fresh subagent|separate agent|review your own|
  self-review` across `skills/process-expert-review/SKILL.md`,
  `skills/using-health-interop/SKILL.md` and `AGENTS.md`: **zero hits**. The
  word "independent" appears in the bootstrap only as "independently testable
  deliverable" (`skills/using-health-interop/SKILL.md:90`).

**Problem.** The gate says *what* must happen (review + approval) but never
*who* must do it. A skill is invoked by the agent that is already working;
nothing in the pack text prevents the builder from invoking
`process-expert-review` on its own artefact in the same session and recording
its own approval in `validation.md` — the same file the builder writes. The
demonstrated failure is the school vision screening step 5: the agent
self-invoked `process-expert-review` in-session, recorded no findings, and
the assistant's independent spot-check then found 9 defects (1 SUSHI error +
3 warnings + 5 further defects). A gate that can be self-certified is not a
gate; it is a checkbox the builder ticks. The independence rule currently
lives only in the parent agent's operating process, not in the pack, so any
other user or harness following the pack alone gets a self-review.

**Fix.** Add to `skills/process-expert-review/SKILL.md` (top, next to the
HARD-GATE) and to the bootstrap (`skills/using-health-interop/SKILL.md:89`):
"The review must run in a fresh subagent that did not build the artefact; the
builder never reviews its own work. Record the reviewer's identity (subagent /
session) in `validation.md` next to the verdict." Reword the HARD-GATE to
"approval by an independent reviewer". Add a check to `tests/check_pack.py`
that the independence sentence is present in both files, so a future edit
cannot silently drop it.

## MEDIUM

### [M1] MEDIUM — The loop-stop rule covers one loop shape, in one skill, with no escalation

**Evidence.**

- `skills/implementation-guide-sushi/SKILL.md:113`: "If a SUSHI rebuild shows
  the same error count as the previous build, STOP and re-read the error lines
  instead of rebuilding again — rebuilding without a new fix is a loop, not
  progress. Match each error line to its section in
  `references/implementation-guide-sushi/fsh-syntax-sushi3.md` before touching
  a file."
- Grep for `STOP and re-read|same error|rebuild.*loop` across all 18 routers:
  the only hit is the line above. `skills/component-building/SKILL.md`,
  `skills/test-driven-interop/SKILL.md`, `skills/bpmn-modeling/SKILL.md` and
  `skills/fhir-modeling/SKILL.md` — all loop-prone (failing test suites,
  RED-GREEN cycles, mechanical BPMN checks, validator runs) — have no stop
  rule at all.
- `references/implementation-guide-sushi/fsh-syntax-sushi3.md`: grep for
  `stop|loop|escalat|not listed|not covered|unmatched` returns nothing except
  the quoted SUSHI error text `"Value does not match element type"` (line
  278). The reference has no branch for an error outside its 9 patterns, so
  the router's instruction "match each error line to its section" is
  unexecutable for a tenth error.
- `references/implementation-guide-sushi/fsh-syntax-sushi3.md:5`: "Load it
  when SUSHI reports a parse error … — before rewriting the file for the
  third time." The reference tolerates two rewrites before it is consulted;
  the router stops after one non-improving rebuild. The two triggers disagree.

**Problem.** The rule as written fires only on *identical consecutive* error
counts. A loop whose count oscillates (85 → 87 → 85 → 86) or climbs
(85 → 107, as the school fixes run did) never triggers it. There is no cap
on total rebuilds and no escalation: after STOP + re-read, if the error is
not in the 9 patterns, the agent has no next step (no "check the SUSHI docs",
no "report to the user with the error log"). The same failure mode exists
uncovered in every other build/test loop in the pack. Anthropic's own
determinism guidance is relevant here: "An instruction is a request; a hook
is a guarantee" — a prose stop rule is the weakest enforcement available,
which is one more reason it should be pack-wide and paired with an
escalation, not a single-skill footnote.

**Fix.** Generalise the rule into `skills/using-health-interop/SKILL.md`
("Rules that always apply"): "Any build, test, or check that fails with the
same result twice → stop, re-read the full output, and change strategy; a
third failure with no new diagnosis → report to the user with the error log
and stop — never rebuild or retest without a new fix." Add to the SUSHI
reference an unmatched-error branch ("If no section matches your error, do
not guess a fix: check the SUSHI / FSH reference live, and if still unmatched,
report the error verbatim to the user"). Align the reference's "third time"
line with the router's one-rebuild trigger. Add the stop sentence to
`tests/check_pack.py` as a presence check so it cannot regress silently.

### [M2] MEDIUM — All 18 frontmatter descriptions contradict Anthropic's official third-person rule

**Evidence.**

- Every router description starts "You MUST use this …" (16/18) or "Load
  this skill …" (`skills/using-health-interop/SKILL.md:3`, root `SKILL.md:3`).
  Description lengths are 96–399 characters — all inside Anthropic's 1,024
  cap — and all state what the skill does and when to use it, which the
  guidance requires.
- Anthropic, "Skill authoring best practices" (verified live):
  "**Always write in third person**. The description is injected into the
  system prompt, and inconsistent point-of-view can cause discovery
  problems." Good: "Processes Excel files and generates reports". Avoid: "I
  can help you process Excel files".
- The pack's choice is deliberate (v0.5.0 strengthened descriptions to the
  "You MUST use this…" style, modelled on obra/superpowers' imperative
  voice) and it has one empirical success: the OpenCode/Nemotron harness
  test, Phase 1, where the first substantive action was a `skill` call
  loading `brainstorming-health`. It is untested on Claude Code, the
  guidance's primary target.

**Problem.** The description is a discovery field, not an instruction channel:
Anthropic loads only name + description at startup and matches the request
against them. Smuggling "MUST" into metadata tries to make a trigger do an
enforcer's job, and it does so in the exact voice the official guidance says
causes discovery problems. The pack's own enforcement already lives where it
belongs — the bootstrap's `<EXTREMELY-IMPORTANT>` block, the SessionStart
hook, and the `<HARD-GATE>` blocks — so the imperative description buys
little and costs a deviation from the standard every other skill in the
ecosystem follows.

**Fix.** Rewrite the 18 descriptions in third person, keeping the what +
when and the sequencing clauses ("Do not model in BPMN … until the spec is
validated"), e.g. `brainstorming-health`: "Defines a clinical use case, its
users, roles, departments, and a written spec for validation. Use before any
health interoperability work; do not model in BPMN or choose FHIR resources
until the spec is validated." Keep "MUST" in the bodies and gates. A/B test
triggering on Claude Code before and after (the pack already has a harness
acceptance test to reuse).

### [M3] MEDIUM — The bootstrap contradicts its own router on the CI workflow filename

**Evidence.**

- `skills/using-health-interop/SKILL.md:66` (step 5): "Generate the Git
  workflow (`.github/workflows/ig-build.yml` at the repo root)…"
- `skills/implementation-guide-sushi/SKILL.md` (CI/CD section): "If the repo
  already has a workflow for another guide, create `ig-build-<slug>.yml` for
  this guide instead of overwriting it (one workflow per guide)".
- `references/implementation-guide-sushi/ci-cd.md:33`: "Generate
  `.github/workflows/ig-build.yml` at the repo root" — the singular name
  leads; the per-guide rule only appears at `ci-cd.md:64-66` ("One workflow
  per guide. If the repo already has a workflow for another guide, do **not**
  overwrite it…").

**Problem.** The file the agent reads first and follows as the workflow map
names the wrong file for any repo that already holds a guide. The correct
rule is stated in exactly one router and buried 30 lines into its reference,
while the singular filename appears in the bootstrap, in the reference's own
lead, and in the template the router tells the agent to copy verbatim. The
demonstrated consequence is the school case: the agent overwrote
`.github/workflows/ig-build.yml` three times (the third overwrite would have
deployed the school guide to the site root and broken the referral subpath).
The router had the right rule and the agent still overwrote — the bootstrap
is where the fix has to land, because it is read first.

**Fix.** Change `skills/using-health-interop/SKILL.md:66` to "Generate one Git
workflow per guide (`ig-build-<slug>.yml`; `ig-build.yml` only for the first
guide in a repo) — see `references/implementation-guide-sushi/ci-cd.md`."
Move the per-guide rule to the top of `ci-cd.md` (before line 33), so the
singular filename never appears unqualified. Consider a `check_pack.py`
assertion that the string `ig-build.yml` never appears in the bootstrap
without the per-guide qualifier.

### [M4] MEDIUM — Step 5's "Done when" has no privacy gate before a public deploy

**Evidence.**

- `skills/implementation-guide-sushi/SKILL.md:146` ("## Done when"): five
  items (SUSHI 0/0, examples validate, operations link to IHE, diagrams have
  pages, expert review + user validation). No privacy item.
- Grep for `privacy|synthetic|PHI` in
  `skills/implementation-guide-sushi/SKILL.md`: one hit only, line 38 —
  "Keep the guide in a versioned folder: `sushi-config.yaml`, FSH files,
  synthetic examples." The CI/CD section never mentions the privacy
  checklist (`references/privacy-checklist.md`), which `validating-interop`
  requires before sharing anything.
- The deploy target is public GitHub Pages (`ci-cd.md`: the workflow
  "deploys the built site to GitHub Pages" on every push from `main`).

**Problem.** Synthetic-only is the pack's core safety promise (bootstrap:
"Use synthetic data by default in every example, test, prompt, log, and
plan"; `privacy-safety-health` applies "at every step"). The bootstrap states
the principle, but the tick-list the agent actually uses to declare step 5
done — immediately before a push that publishes the guide to the public web —
never asks for the privacy check. A real identifier slipping into an example
would be published, not merely written to a local file.

**Fix.** Add to "Done when": "Privacy checklist run
(`references/privacy-checklist.md`): no real identifiers, names, or clinical
records in the guide." Add the same line to the CI/CD task in
`05-implementation-guide/plan.md`'s template, before the deploy step.

### [M5] MEDIUM — `check_pack.py` reports "8/8 checks passed" when the budget check was skipped

**Evidence.**

- `tests/check_pack.py:51-66` (`check_budget`): if tiktoken is not importable,
  it prints a WARNING and calls `report("budget", True, "SKIPPED …")`.
- `tests/check_pack.py:260`: the summary line is
  `f"\n{8 - len(FAILURES)}/8 checks passed"`.
- `AGENTS.md` (release checklist): "Run the local checks before pushing:
  `python3 tests/check_pack.py`" — plain system `python3`.
- Observed in this review: running `python3 tests/check_pack.py` with the
  system interpreter printed `WARNING: tiktoken is not installed — budget
  check SKIPPED` and then `8/8 checks passed`. The tiktoken venv lives at
  `/tmp/tokvenv` (ephemeral; wiped on VM restart), so the documented command
  silently degrades to 7 real checks + 1 pass-by-default whenever the venv
  is gone.

**Problem.** A skipped check counted as passed inflates release confidence:
a release can ship with the budget unverified while the headline says 8/8.
The warning is printed, but the summary line — the part a release note
quotes — erases it. This is the same class of error as the pack's own
"verified" claims that turned out false in the school case: a green headline
over an unchecked claim.

**Fix.** Count honestly: report `"7/8 passed, 1 skipped"` when the budget
check skips, and exit non-zero in a release context (or make the release
checklist require the tiktoken venv explicitly:
`/tmp/tokvenv/bin/python tests/check_pack.py`, recreating the venv first).
Cheapest correct change: track skipped checks separately in `FAILURES`-style
accounting and print the skip in the summary line.

### [M6] MEDIUM — The anchors check ignores bare `.md` path references (694 unguarded pointers)

**Evidence.**

- `tests/check_pack.py` (`check_anchors`): the pattern is
  `([A-Za-z0-9_./-]+\.md)#([A-Za-z0-9_-]+)` — a reference only counts if it
  carries a `#anchor`.
- Measured in this review: **694 bare `.md` path references** across the
  pack (e.g. `` `references/task-atoms.md` `` ×30, `references/fhir-modeling/
  _index.md` ×12), **0 broken today** — all 694 resolve. The pack is
  consistent now; the gap is purely a missing guard.

**Problem.** The single most common cross-reference form in the pack — the
bare dispatch pointer ("load `references/task-atoms.md`, never copy it") —
is the one form no check validates. Rename or move one reference file and
nothing fails; the breakage surfaces later, at runtime, as an agent that
cannot find the vocabulary its router points at. The anchors check already
proves the pattern works for 294 anchored refs; bare refs deserve the same.

**Fix.** Add a 9th check to `tests/check_pack.py` resolving every bare
`references/…md` / `skills/…md` path (relative to the pack root and to the
referencing file's directory), and report the count. The 0-broken baseline
from this review is the expected result.

### [M7] MEDIUM — The tightest router is the gate skill itself; the split-target note is stale

**Evidence.**

- Budget (tiktoken `cl100k_base`, measured in this review): routers —
  `process-expert-review` 4,513 tokens (487 from the 5,000 cap),
  `ihe-landscape-scan` 4,488 (512), `component-building` 4,305,
  `bpmn-modeling` 4,033. References over 5,000: `ips.md` 7,364,
  `clinical-trials.md` 7,204, `care-planning.md` 7,155, `rehabilitation.md`
  6,496, `terminology.md` 6,465, `waits-loops.md` 6,201,
  `standing-continuous.md` 6,051, `diabetes.md` 5,766, `patient-summary.md`
  5,713, `prehospital.md` 5,355, `task-atoms.md` 5,320,
  `ihe-profile-review/clinical-trials.md` 5,287. All under the 8,000 M10
  trigger; HIGH 0.
- `skills/skill-budget-repair/SKILL.md:63`: "Next split target (audit 19
  [CONS A-F7], updated v0.39.0): `references/fhir-modeling/ips.md` — the
  largest `references/` file (7,364 tokens at v0.39.0, 636 from the M10 8,000
  trigger); `references/fhir-modeling/care-planning.md` (7,155 tokens) is now
  second…" — at v0.40.2 `clinical-trials.md` (7,204) has overtaken
  `care-planning.md` (7,155) for second place, so the ranking in the standing
  instruction is stale.

**Problem.** `process-expert-review` is the review gate and the closest
router to its cap, and every audit round adds safety vocabulary to it (the
file already holds ten safety sections). The pack's own rule is to split a
router *before* the next round that adds vocabulary to it; the next round
that touches this skill will breach 5,000 unless the split happens first.
Separately, the split-target note freezes token figures from v0.39.0 in a
standing instruction — the same drift mechanism as the duplicated state.md
rule (L1), in miniature.

**Fix.** Split `process-expert-review` before the next vocabulary-adding
round (move one safety section, e.g. the palliative or surgical block, to
`references/process-expert-review/…md` with a dispatch row — the file
already uses that pattern for transfusion and immunization). Refresh the
split-target note or, better, drop the frozen figures and point at
`scripts/check-skill-budget.py` output as the live ranking.

## LOW

### [L1] LOW — The state.md rule is copied verbatim into 6+ routers; one copy has already drifted

**Evidence.** Identical sentence in `skills/bpmn-modeling/SKILL.md:158`,
`skills/brainstorming-health/SKILL.md:85`,
`skills/component-building/SKILL.md:115`,
`skills/entities-data/SKILL.md:79`, `skills/fhir-modeling/SKILL.md:133`,
`skills/mapping-to-fhir/SKILL.md:75`: "Update `state.md` after each
sub-task, before any long build or validation run, and whenever the work waits
for the user, so an interruption costs at most one sub-task." The copy in
`skills/implementation-guide-sushi/SKILL.md:156` reads "before any long
build, and whenever the work waits for the user" — "or validation run" is
missing.

**Problem.** Seven copies of one rule, one already diverged. The pack
already solved this exact problem for task atoms ("load
`references/task-atoms.md`, never copy it" — present in all 18 routers,
verified) but never applied the same pattern to the checkpoint rule.

**Fix.** Replace the inline sentence in every router with a pointer:
"Update `state.md` per `references/work-structure.md#…`." Keep the full
rule in `work-structure.md` only.

### [L2] LOW — "Announce at the start of your reply" is in 7/18 skills, undocumented

**Evidence.** Present in `bpmn-modeling`, `brainstorming-health`,
`component-building`, `entities-data`, `fhir-modeling`,
`implementation-guide-sushi`, `sequence-diagrams`; absent in the other 11.
`skills/sequence-diagrams/SKILL.md:12` announces "Step 4 — Sequence
diagrams", although the skill also runs in step 5 (carrying diagrams into the
guide).

**Fix.** Document the pattern (step skills announce; review and utility
skills do not) or restrict it to the six step skills; fix the
sequence-diagrams line to "Step 4/5 — Sequence diagrams".

### [L3] LOW — Root `SKILL.md` description is identical to the bootstrap's

**Evidence.** Root `SKILL.md:3` and
`skills/using-health-interop/SKILL.md:3` both read: "Load this skill at the
start of any session about health data interoperability, FHIR, HL7, or
clinical data mapping." The root file is not in the manifest's 18 skills, but
harnesses that index a plugin-root `SKILL.md` see two metadata entries with
the same trigger text and cannot distinguish entry point from workflow.

**Fix.** Differentiate the root description: "Entry point to the
health-interop-superpowers pack — redirects to the `using-health-interop`
bootstrap; load the bootstrap, not this file, for the workflow."

### [L4] LOW — `skill.yaml`'s skills list is unchecked and ordered differently from the manifest

**Evidence.** `skill.yaml` lists 18 skills (set-equal to disk, verified) in
workflow order; `.muse-plugin/plugin.json` lists the same 18 with
`brainstorming-health` first and the rest alphabetical. `tests/check_pack.py`
(`check_manifest`) validates only the Muse manifest; nothing validates
`skill.yaml`'s list. A skill added to disk and to the manifest but not to
`skill.yaml` would pass every check.

**Fix.** Extend `check_manifest` to assert `skill.yaml`'s skills set equals
the disk set, or drop the list from `skill.yaml` (it duplicates the manifest).

### [L5] LOW — The OpenCode V2 plugin half ships untested (documented, but shipped)

**Evidence.** `.opencode/plugins/health-interop-superpowers.js:2` (header)
and `index.js:6-8`: "No 2.x release exists on npm as of 2026-11-17 (latest is
1.19.5), so the V2 half is untested until one ships." `node --check`
validates syntax only; no test exercises the V2 `setup(ctx)` path.

**Fix.** When OpenCode 2.x ships, run the harness acceptance test against it
before claiming V2 support; until then, say "OpenCode 1.x" in the README
harness heading instead of implying both.

### [L6] LOW — The SessionStart hook injects the 2,239-token bootstrap into every session

**Evidence.** `hooks/session-start` reads
`skills/using-health-interop/SKILL.md` in full and emits it as
`additionalContext` on every session start, in every harness that installs
the plugin (Claude, Cursor, Muse branches). The bootstrap router is 2,239
tokens. This is the obra/superpowers pattern, and it is why the workflow
triggers reliably — but it is a ~2.2k-token tax on sessions that have nothing
to do with health interoperability.

**Fix.** Scope the hook (inject only when the first user message matches
health-interop triggers) or document the cost in the README prerequisites so
the trade-off is explicit. Note Anthropic's own boundary rule: always-on
context should hold only what applies broadly.

### [L7] LOW — No live check that the published guide actually responds

**Evidence.** The referral guide's first green CI run did not deploy to
`gh-pages` (never diagnosed; Actions runs are not readable via the pack's
tooling) and the guide 404'd until the user fixed it from the web UI. The
school guide likewise 404'd immediately after its push. The step-5 "Done
when" (`skills/implementation-guide-sushi/SKILL.md:146-152`) has no "fetch
the published URL, confirm 200" item; the router's only live check is for
the menu markup ("Verify on the published page (fetch `index.html`, check
`<nav>`)").

**Fix.** Add to "Done when": "Fetch the published guide URL and confirm it
returns 200; if it 404s after a green run, the deploy did not land — do not
declare the guide published."

## Top 5 fixes, ranked by impact

1. **Encode reviewer independence (H1).** The central gate is self-certifiable
   today, and the school case proved the failure mode. One sentence in two
   files + a presence check.
2. **Generalise the loop-stop rule pack-wide, with escalation and an
   unmatched-error branch (M1).** The SUSHI rule fixed one loop shape in one
   skill; every other build/test loop in the pack is still unguarded.
3. **Fix the bootstrap workflow-filename contradiction (M3).** The file read
   first names the wrong file; the school agent overwrote the shared workflow
   three times because of it.
4. **Rewrite descriptions in third person (M2)** — or A/B test triggering on
   Claude Code first. The pack currently deviates from the official standard
   in all 18 metadata entries.
5. **Add the privacy gate to step 5's "Done when" (M4).** The deploy target
   is the public web; the tick-list used to declare the guide done should
   name the privacy check explicitly.

## What was verified clean (no finding)

- **Progressive disclosure** matches Anthropic's three tiers: metadata
  ~100–400 characters per skill (18 skills ≈ 3.5k characters, well inside
  the ~15.5k discovery budget); all routers ≤ 4,513 tokens, under the 5k
  cap; 201 reference files load on demand only.
- **Frontmatter**: only `name` + `description` in every `SKILL.md`
  (Anthropic: only these two are loaded at startup); names are lowercase
  hyphenated, within 64 characters; descriptions non-empty, no XML tags.
- **Router bodies**: longest is 171 lines (Anthropic: under 500 lines);
  no SKILL.md line over 500 characters (check 8/8).
- **Manifests**: all 7 harness version markers at 0.40.2; the Muse
  manifest lists 18 skills, `brainstorming-health` first, rest alphabetical;
  the other harnesses discover `skills/` from disk, as documented in
  `AGENTS.md` (same as superpowers).
- **Cross-references**: 294 anchored refs resolve; 694 bare `.md` refs
  resolve (0 broken) — the pack is consistent today; M6 is about the missing
  guard, not live breakage.
- **Safety**: synthetic-by-default in the bootstrap, the privacy skill, and
  the git skill ("nothing with real patient data is ever staged"); the
  pre-sharing privacy checklist exists and is referenced by
  `validating-interop`.
- **Budget discipline**: pinned measurement (tiktoken `cl100k_base`),
  recorded history (15 entries), repair skills decoupled from workflow
  gates per the user's correction; `skill-budget-review` reports only,
  `skill-budget-repair` executes — the split is clean.
- **Hard gates**: `<HARD-GATE>` blocks between steps in the step routers;
  "verify live, never from memory" in 7 routers; validation evidence
  required before any claim of correctness (`validating-interop`).
