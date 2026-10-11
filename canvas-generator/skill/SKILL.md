---
name: jtbd-hypothesis-canvas
description: Guide a user through creating a filled JTBD Hypothesis Canvas YAML instance (official Kalbach/Toolkit V3 structure) and optionally generate the matching PDF. Use when the user wants to fill out a JTBD canvas, create a jobs-to-be-done hypothesis canvas, scope a focus job, or produce a canvas YAML/PDF for any domain.
---

# JTBD Hypothesis Canvas Filler

Help the user produce a complete, well-formed **JTBD Hypothesis Canvas** instance in YAML that conforms to the official Toolkit structure (V3). Then optionally render it to the official-layout PDF.

This skill is for the **Frame** phase — scoping who to talk to and what to talk about before deep research. It does not replace interviews.

## When to Use

- User asks to “fill out a JTBD canvas”, “create a hypothesis canvas”, “scope a focus job”, or similar.
- User is starting JTBD work on a new domain and needs a structured starting point.
- User already has rough notes and wants them turned into a proper canvas instance.

## Official Canvas Structure (do not invent sections)

**Top-down (Scope)**
- `playing_field` — domain / value-creation context in plain language
- `job_performer` — who executes the job (one primary performer per canvas)
- `focus_job` — the unit of analysis (functional, solution-agnostic, singular, action-verb first)
- `aspirations` — 2–3 higher-order “be” goals
- `related_jobs` — other jobs at similar altitude (not the current focus)

**Bottom-up (Hypothesize)**
- `job_steps` — chronological process (`beginning`, `middle`, `end` + optional `stages`)
- `success_criteria` — how success is measured (prefer minimize/maximize + unit + qualifier)
- `emotions` — feel / avoid feeling statements
- `circumstances` — contextual factors (prefer “whether …”)

Optional: `meta` (title, author, version, description, source).

## Conversation Flow

Follow this sequence. Do not skip ahead to writing the full YAML until the core scoping decisions are clear.

### Step 1 — Playing Field
Ask:
> What area or domain are we in? Describe it in plain language (avoid broad industry labels).  
> Example prompt: “We’re in the business of __________.”

Record a concise `playing_field`.

### Step 2 — Job Performer
Ask:
> Who is the primary job performer we want to create value for?  
> List possible actors first if helpful, then choose **one**.

Record `job_performer`. One performer per canvas.

### Step 3 — Focus Job
This is the most important decision. Guide the user to a statement that:
- Starts with an action verb
- Is solution- and technology-agnostic
- Is singular (no AND/OR)
- Has a clear beginning, middle, and end
- Sits at a useful altitude (not so high it is an aspiration, not so low it is a micro-task)

Use the hierarchy test:
- Ask “why?” → moves up toward aspirations
- Ask “how?” → moves down toward job steps

Propose 1–3 candidate focus-job phrasings and let the user choose or refine. Record `focus_job`.

### Step 4 — Aspirations & Related Jobs
- Aspirations: 2–3 “be” goals the performer is pursuing by doing the focus job.
- Related Jobs: other functional jobs at roughly the same level that the performer also tries to get done in this playing field. These are explicitly *not* the current focus.

### Step 5 — Bottom-up Hypotheses
Treat these as initial hypotheses to be validated later:

**Job Steps**  
Prefer the three-phase structure:
- `beginning`
- `middle`
- `end`  
Optionally include `stages: [PLAN, PREPARE, EXECUTE, MONITOR, MODIFY, CONCLUDE]`.

Phrase steps with action verbs, no tools/solutions, no AND/OR.

**Success Criteria**  
Use the pattern: directional verb (minimize/maximize/reduce/increase) + unit of measure + qualifier.  
Example: “Minimize the time to reach clarity on the nature and magnitude of exposure”

**Emotions**  
Start with “Feel …” or “Avoid feeling …”

**Circumstances**  
Prefer “Whether …” statements that capture meaningful variation in how the job is done.

### Step 6 — Emit the YAML
Once the above are agreed, write a complete YAML file that matches this shape:

```yaml
playing_field: >
  ...
job_performer: >
  ...
focus_job: >
  ...
aspirations:
  - ...
related_jobs:
  - ...
job_steps:
  stages:
    - PLAN
    - PREPARE
    - EXECUTE
    - MONITOR
    - MODIFY
    - CONCLUDE
  beginning: >
    ...
  middle: >
    ...
  end: >
    ...
success_criteria:
  - ...
emotions:
  - ...
circumstances:
  - ...
meta:
  title: ...
  version: "1.0"
  description: ...
  source: Official JTBD Hypothesis Canvas structure (jtbd.tk/canvas)
```

Save it (e.g. `canvas.yaml` or a domain-specific name).

### Step 7 — Optional PDF Generation
If the user wants the official-layout PDF and the generator is available:

```bash
python generate_canvas_pdf.py path/to/canvas.yaml -o canvas.pdf
```

The generator lives alongside this skill (`../generate_canvas_pdf.py`) and expects only `pyyaml` + `reportlab`.

## Formulation Rules (enforce these)

| Element            | Rules |
|--------------------|-------|
| Focus Job          | Action verb first, no solutions/tech, singular, stable over time |
| Job Steps          | Action verb, no tools/methods, no AND/OR, chronological |
| Success Criteria   | minimize/maximize/reduce/increase + unit + qualifier |
| Emotions           | “Feel …” or “Avoid feeling …” |
| Circumstances      | Prefer “Whether …” |
| Aspirations        | “Be …” identity-level outcomes |
| Related Jobs       | Same altitude as Focus Job, separate beginning/middle/end |

## What Not to Do

- Do not invent extra canvas sections.
- Do not put solutions, product names, or features into job statements.
- Do not treat the canvas as research output — it is a hypothesis for the Frame phase.
- Do not force a single “correct” focus job; help the user choose a useful altitude for *their* strategic intent.
- Do not skip the Focus Job conversation; it is the unit of analysis everything else depends on.

## Reference Files

- Schema: `../jtbd_hypothesis_canvas.linkml.yaml`
- Example instance: `../examples/defendant_post_pleading.yaml`
- Generator: `../generate_canvas_pdf.py`
- Official visual: jtbd.tk/canvas

When in doubt, prefer the official Toolkit language and structure over improvisation.
