# JTBD Hypothesis Canvas Tool

Automatable pipeline for the official **JTBD Hypothesis Canvas** (V3) defined by Jim Kalbach & Elaine Matthias (JTBD Toolkit).

## Contents

| File | Purpose |
|------|---------|
| `jtbd_hypothesis_canvas.linkml.yaml` | LinkML schema defining the canvas structure |
| `generate_canvas_pdf.py` | YAML → official-layout PDF generator |
| `examples/defendant_post_pleading.yaml` | Filled example (defendant post-pleading stage) |

## Schema (LinkML)

The schema captures every section of the official visual canvas:

**Top-down (Scope)**  
- `playing_field`  
- `job_performer`  
- `focus_job` (unit of analysis)  
- `aspirations` (multivalued)  
- `related_jobs` (multivalued)  

**Bottom-up (Hypothesize)**  
- `job_steps` (structured: beginning / middle / end + optional stages)  
- `success_criteria` (multivalued)  
- `emotions` (multivalued)  
- `circumstances` (multivalued)  

Optional `meta` block for title, author, version, etc.

## Usage

```bash
# Generate PDF from any conforming YAML
python generate_canvas_pdf.py examples/defendant_post_pleading.yaml \
    -o ../JTBD_Defendant_Post_Pleading_Canvas.pdf
```

Requirements: `pyyaml`, `reportlab`

```bash
pip install pyyaml reportlab
```

## Design Notes

- The generator reproduces the official V3 layout (arch for Focus Job, stage labels, vertical title, footer).
- Aspirations sit in the center-top box; the Focus Job arch is drawn so its content lives inside the semicircle and does not overlap the Aspirations text.
- All formulation guidance (action-verb jobs, minimize/maximize success criteria, “feel / avoid feeling”, “whether …” circumstances) is documented in the schema descriptions and remains the responsibility of the YAML author.
- The pipeline is intentionally generic: any domain can be expressed as a YAML instance and rendered with the same visual language.
