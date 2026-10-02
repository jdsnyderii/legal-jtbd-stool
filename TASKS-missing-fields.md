# Task list: Kalbach missing fields (additive only)

**Scope:** Plain missing fields on `Job` (and light outcome polish).  
**Out of scope:** Job process / job-map structure (hierarchy remains the process model).

---

## Set A — Job statement grammar

| # | Task | Status |
|---|------|--------|
| A1 | Add slots: `statement_verb`, `statement_object`, `statement_clarifier` | done |
| A2 | Add slot: `job_statement` (optional assembled sentence; may mirror verb+object+clarifier) | done |
| A3 | Document: prefer structured parts; `job_statement` is display/export convenience | done |

## Set B — Job performer (who)

| # | Task | Status |
|---|------|--------|
| B1 | Add slot: `job_performer` (who executes the job) | done |
| B2 | Add slot: `buyer_role` (who buys/authorizes when different from performer) | done |

## Set C — Circumstances (when / where)

| # | Task | Status |
|---|------|--------|
| C1 | Add slot: `circumstance_situation` (triggering context) | done |
| C2 | Add slot: `circumstance_constraints` (multivalued string: time, budget, risk, etc.) | done |
| C3 | Keep existing `phase` as domain facet (not replaced) | done |

## Set D — Emotional / social dimensions

| # | Task | Status |
|---|------|--------|
| D1 | Add slot: `emotional_job` | done |
| D2 | Add slot: `social_job` | done |

## Set E — Completion & job story (optional narrative)

| # | Task | Status |
|---|------|--------|
| E1 | Add slot: `end_state` (what “done” looks like) | done |
| E2 | Add slots: `job_story_situation`, `job_story_motivation`, `job_story_expected_outcome` | done |

## Set F — Desired outcome polish (small)

| # | Task | Status |
|---|------|--------|
| F1 | Add slot on DesiredOutcome: `object_of_control` (ODI fourth element, explicit) | done |

## Set G — Propagate to physical layer & tooling

| # | Task | Status |
|---|------|--------|
| G1 | Update `jobs.yaml` (LinkML) with all new slots + Job/DesiredOutcome slot lists | done |
| G2 | Update `schema.sql` (`job` + `desired_outcome` columns, all nullable except existing required) | done |
| G3 | Update `load_db.py` INSERT columns for new fields | done |
| G4 | Backfill a few top-level jobs in `jobs-instance.yaml` with statement + performer + end_state as examples | done |
| G5 | Reload `jtbd.sqlite` | done |
| G6 | Refresh `sample-data.json` | done |
| G7 | Extend `jtbd-editor.html` job detail form with new fields | done |
| G8 | Mark this task list statuses complete; note in AGENT.md briefly | done |

---

## Acceptance

- [x] LinkML validates conceptually (new slots on Job / DesiredOutcome)
- [x] SQLite loads without error; new columns present and nullable
- [x] Example T1–T6 rows show non-empty `job_statement` / `job_performer` where backfilled
- [x] Editor can view/edit new fields for a selected job
- [x] Process hierarchy unchanged (`parent_job`, `child_jobs`, `sequence_order`, `iterative`)
