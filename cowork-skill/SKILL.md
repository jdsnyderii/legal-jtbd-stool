---
name: jtbd-hypothesis-canvas
description: Create a JTBD (Jobs to Be Done) Hypothesis Canvas, the official Kalbach/Matthias JTBD Toolkit V3 layout, as an editable canvas page plus a YAML file and a PDF. Make sure to use this skill whenever the user mentions a JTBD canvas, hypothesis canvas, jobs-to-be-done framing, focus job, job performer, job map or job steps, or wants to scope who to interview and what to ask before JTBD research, even if they do not say "canvas". Also use it to turn rough notes into a canvas, or to load and edit an existing canvas YAML.
---

# JTBD Hypothesis Canvas

Produce a complete JTBD Hypothesis Canvas (Toolkit V3) for the user's domain. The deliverable is a self-contained HTML tool that looks like the V3 canvas, is prefilled with draft hypotheses, and lets the user edit in place, save YAML, load YAML, and save a PDF. Everything runs locally in the browser. No Python or install is needed.

This is for the **Frame** phase: scoping who to talk to and what to talk about before deep research. The contents are hypotheses to validate in interviews, not findings.

## Workflow (form first, minimal conversation)

The user prefers a form-based flow over a long narrative Q&A. Do this:

1. **Collect only what you cannot infer.** Ask at most one short round of questions, and skip anything the user already said. You need:
   - the domain / playing field
   - the one job performer (the canvas allows exactly one)
   - the focus job, or enough to propose one
2. **Settle the focus job.** It is the unit of analysis, so spend effort here. If the user's phrasing is too broad (spans a whole lifecycle) or too narrow (a micro-task), propose 2-3 alternatives at different altitudes with one-line trade-offs and let them pick. Use the why/how test: "why?" moves toward aspirations, "how?" moves toward job steps.
3. **Draft everything else yourself** as starter hypotheses: aspirations, related jobs, job steps, success criteria, emotions, circumstances. Do not interview the user for each section. Drafts are cheaper to edit than blanks.
4. **Build the prefilled tool** (see below) and give it to the user.
5. **Iterate from their edits.** If they paste back YAML or tell you changes, apply them and re-check against the formulation rules.

## Building the prefilled tool

1. Copy `assets/jtbd_canvas_tool.html` to the outputs folder (e.g. `jtbd_canvas_<topic>.html`).
2. Replace the `const DEF={...};` block near the top of the `<script>` with the drafted values. Keep the shape exactly:

```js
const DEF={title:"Litigation partner: respond to a filed complaint",
playing_field:"...",
job_performer:"...",
focus_job:"...",
aspirations:["...","..."],
related_jobs:["..."],
beginning:["step","step"],
middle:["step","step"],
end:["step","step"],
success_criteria:["..."],
emotions:["..."],
circumstances:["..."]};
```

   Job steps are arrays: one string per step, in chronological order. Do not change anything else in the file. Edit it with a targeted replacement, not a rewrite.
3. Present the file. Tell the user how to use it in 3 short lines: open it in a browser, click any text to edit (Enter adds a bullet), then **Save YAML** / **Save as PDF** (print dialog, choose Save as PDF, margins None).

A worked example of the expected content is in `examples/litigation_partner_respond_to_complaint.yaml`.

## Formulation rules (enforce on every draft)

| Element | Rules |
|---|---|
| Playing field | Plain-language "We're in the business of ...", not a broad industry label |
| Job performer | One primary performer only |
| Focus job | Action verb first, solution- and technology-agnostic, singular (no AND/OR), clear beginning/middle/end, stable over time |
| Aspirations | 2-3 "Be ..." identity-level goals |
| Related jobs | Functional jobs at the same altitude as the focus job, not the current focus |
| Job steps | Action verb, chronological, no tools or methods, no AND/OR |
| Success criteria | minimize / maximize / reduce / increase + unit of measure + qualifier |
| Emotions | "Feel ..." or "Avoid feeling ..." |
| Circumstances | Prefer "Whether ..." |

If the performer is ambiguous (for example "partner or associate"), explain briefly that they are different performers with different aspirations and emotions, and ask which one to use. Offer a second canvas for the other.

## YAML output

The tool's **Save YAML** writes this shape (matches `references/jtbd_hypothesis_canvas.linkml.yaml`). If the user wants YAML directly in chat or as a file, produce the same shape:

```yaml
playing_field: "..."
job_performer: "..."
focus_job: "..."
aspirations:
  - "..."
related_jobs:
  - "..."
job_steps:
  stages: [PLAN, PREPARE, EXECUTE, MONITOR, MODIFY, CONCLUDE]   # one per line in saved files
  beginning: "step → step → step"
  middle: "step → step"
  end: "step → step"
success_criteria:
  - "..."
emotions:
  - "..."
circumstances:
  - "..."
meta:
  title: "..."
  version: "1.0"
  source: "Official JTBD Hypothesis Canvas structure (jtbd.tk/canvas)"
```

Job-step phases are single strings with " → " between steps. The tool's loader also accepts newline-separated or folded (`>`) text.

## Editing an existing canvas

- If the user gives a YAML file, read it, apply their changes, then rebuild the tool with the updated values in `DEF`. Or tell them they can open the tool and use **Load YAML**.
- Load YAML supports plain maps, lists, quoted and plain scalars, and `>` / `|` blocks. It is not a full YAML parser (no anchors or flow-style lists in values).

## What not to do

- Do not invent canvas sections beyond those in the table above.
- Do not put solutions, product names, or features into job statements.
- Do not present the canvas as research output.
- Do not force one "correct" focus job; the right altitude depends on the user's strategic intent.
- Do not skip the focus-job decision. Everything else depends on it.
- Do not rewrite the HTML tool's layout or logic unless the user asks for a change.

## Reference files

- `assets/jtbd_canvas_tool.html`: the V3-layout editable canvas (blank). Copy and prefill per request.
- `references/jtbd_hypothesis_canvas.linkml.yaml`: formal schema for the YAML.
- `examples/litigation_partner_respond_to_complaint.yaml`: filled example instance.
- Official visual and guidance: jtbd.tk/canvas (JTBD Toolkit, Jim Kalbach & Elaine Matthias, CC BY-NC-ND 4.0).
