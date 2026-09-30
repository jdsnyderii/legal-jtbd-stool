# legal-jtbd-stool

**Legal litigation Jobs to Be Done (JTBD)** — three-legged stool for product strategy:

| Leg | Contents |
|-----|----------|
| **Jobs & outcomes** | Kalbach hierarchy (top / mid / micro) + desired outcomes |
| **Investment lanes** | Product outcomes cataloged by strategic lane |
| **Requirements & capabilities** | Traceability from outcomes to buildable capabilities |

## Status

- **Domain model (LinkML jobs):** `v0.5.0` (Kalbach descriptive fields + hierarchy)
- **Canonical branch for full work:** `domain/jobs-v0.5.0` (models, instances, generated schema, loader, UI)
- **`main`:** project orientation and contribution rules (this README)

## Design rules (non-negotiable)

1. **Semantic identity** — CURIEs/IRIs as primary keys (`jtbd:JOB-…`, `inv:…`, `req:…`), not DB surrogate IDs for domain entities.
2. **`schema.sql` is always generated** — edit LinkML, then run `python3 generate_schema.py`. Do not hand-edit DDL.
3. **Process = hierarchy** — job map is `parent_job` / `child_jobs` / `sequence_order` / `iterative`, not a bag of process fields on the main job.
4. **Editor ≠ database (today)** — Workbench uses embedded JSON from YAML; SQLite is loaded separately via `load_db.py`.

## Quick start (on the domain branch)

```bash
git checkout domain/jobs-v0.5.0
python3 generate_schema.py   # LinkML → schema.sql
python3 load_db.py           # YAML instances → jtbd.sqlite
open jtbd-editor.html        # or serve statically
```

## Documentation on the domain branch

- `AGENT.md` — full design choices and conventions
- `GENERATE.md` — schema generation
- `TASKS-missing-fields.md` — Kalbach field extension checklist

## License / privacy

Private repository. Intended for internal product/strategy modeling.
