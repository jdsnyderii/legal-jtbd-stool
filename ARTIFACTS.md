# Artifacts on this branch

## In git (source of truth for structure)

- LinkML: `graph_foundation.yaml`, `jobs.yaml` (v0.5.0)
- Docs: `README.md`, `AGENT.md`, `GENERATE.md`
- `restore_large_artifacts.py`

## Large binaries / full instances

Full `jobs-instance.yaml`, `sample-data.json`, `jtbd-editor.html`, and `jtbd.sqlite` may exceed single-commit tooling limits from the agent.

**Authoritative local package:** `jtbd-models-complete.zip` produced in the modeling session.

After cloning this branch, place those files in the repo root (or re-export from your local working copy), then:

```bash
python3 generate_schema.py   # when generator is present
python3 load_db.py           # when loader + instances present
```

## Design rules

See `README.md` on `main` and `AGENT.md` on this branch.
