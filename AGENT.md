# AGENT.md — Legal JTBD Three-Legged Stool

Guidance for humans and agents working on this package. It records **design choices**, **modeling conventions**, and **how to regenerate** artifacts without re-litigating settled decisions.

---

## 1. Purpose

This package models **Jobs to Be Done (JTBD)** for **US civil litigation** as a maintainable, storage-independent semantic model with three linked legs:

| Leg | LinkML schema | Instance data | Role |
|-----|---------------|---------------|------|
| **Jobs & outcomes** | `jobs.yaml` (+ `graph_foundation.yaml`) | `jobs-instance.yaml` | Kalbach Main Jobs → mid → micro; desired outcomes |
| **Investment lanes** | `investments.yaml` | `investments-instance.yaml` | Where product value is cataloged (lanes + product outcomes) |
| **Requirements & capabilities** | `product_requirements.yaml` | `product-requirements-instance.yaml` | Requirements → capabilities that support jobs/outcomes |

Together they form a **three-legged stool**: product work should be traceable from **job/outcome → product outcome → requirement → capability**.

---

## 2. Domain framing (settled)

### 2.1 Litigation phases (coarse-grained)

Used as `phase` on jobs (orientation, not a strict state machine):

0. `pre_litigation`  
1. `pleadings`  
2. `case_management`  
3. `discovery`  
4. `pretrial`  
5. `trial`  
6. `post_trial`  
7. `resolution` (cross-cutting in practice; kept as a phase bucket)  

Also used: `cross_cutting` for related/reusable jobs.

**Anchors:** SALI LMSS 2.0–style phase/service thinking; standard US FRCP-oriented Civ Pro arc (Yale/Stanford/Harvard/Columbia/UT teaching patterns). Class/MDL treated as **overlays**, not separate top-level phases.

### 2.2 Top-level Main Jobs (T1–T6)

| ID | Main Job |
|----|----------|
| **T1** | Resolve the dispute on favorable terms |
| **T2** | Establish and protect a viable legal position |
| **T3** | Develop the evidentiary and factual record |
| **T4** | Narrow or dispose of issues before trial |
| **T5** | Obtain a reasoned decision on the merits (or preserve error for review) |
| **T6** | Manage cost, risk, and process discipline across the matter |

Performer is primarily the **party/client**; counsel is hired to help. Counsel-delivery jobs are **related** (R1–R8), not additional Main Jobs.

### 2.3 Hierarchy (Kalbach)

- **top_level** — Main Job (stable, solution-agnostic)  
- **mid_level** — Job-map stage / major step (often phase-aligned)  
- **micro** — Smallest actionable objective inside a stage  

**Iterative** mids (`iterative: true`) may legitimately repeat (discovery waves, negotiation rounds, successive motions, continuous governance).

### 2.4 Related / reusable jobs (R1–R8)

Mid-level only (no micro expansion required): counsel engagement, insurance, vendors, research, knowledge/SALI tagging, privilege governance, stakeholder/PR track, enforcement/collection.

### 2.5 Desired outcomes (Kalbach form)

Attached primarily at **top** and **mid** levels:

- `direction` ∈ {minimize, maximize, maintain}  
- `unit_of_measure` + `qualifier`  
- Optional `importance`, `satisfaction`, `opportunity_score`  

Micros usually do **not** each carry outcomes.

---

## 3. Semantic identity (storage-independent)

### 3.1 Rule

**Primary keys are SemanticIds (CURIE/IRI strings), never database surrogate integers for domain entities.**

Examples:

- `jtbd:JOB-T3-EVIDENCE`  
- `jtbd:OUT-T3-MIN-DISCOVERY-COST`  
- `inv:LANE-EFFICIENCY`  
- `inv:POUT-LOWER-DISCOVERY-COST`  
- `req:REQ-EDISC-COST-CONTROL`  
- `req:CAP-DISCOVERY-WORKFLOW`  

### 3.2 CURIE patterns

| Kind | Pattern |
|------|---------|
| Job | `jtbd:JOB-T{n}-…` top; `…-M{n}-…` mid; `…-MICRO-…` micro; `jtbd:JOB-R{n}-…` related |
| Outcome | `jtbd:OUT-T{n}-…` or `jtbd:OUT-T{n}-M{n}-…` |
| Lane | `inv:LANE-…` |
| Product outcome | `inv:POUT-…` |
| Requirement | `req:REQ-…` |
| Capability | `req:CAP-…` |

### 3.3 Graph role

LinkML classes/slots may carry `graph_role: node` or `graph_role: edge` (annotation). This is **projection guidance** for graph or relational stores—not a storage technology.

- **Nodes:** Job, DesiredOutcome, InvestmentLane, ProductOutcome, Requirement, Capability  
- **Edges:** multivalued associations (child_jobs, desired_outcomes, supports_jobs, …)

---

## 4. LinkML design

### 4.1 Files

| File | Contents |
|------|----------|
| `graph_foundation.yaml` | `SemanticId`, abstract `Identifiable` / `GraphNode` / `GraphEdge`, lifecycle status |
| `jobs.yaml` | Job, DesiredOutcome, levels, phases, iterative |
| `investments.yaml` | InvestmentLane, ProductOutcome, horizon |
| `product_requirements.yaml` | Requirement, Capability |
| `unified_inline.yaml` | Merged schema for SQL generation (imports stripped, annotations stripped for loader compatibility) |

### 4.2 Class-typed edges (important)

Cross-references that must become **SQL foreign keys** use **class ranges**, not bare `uriorcurie`:

| Slot | Range |
|------|--------|
| `parent_job`, `child_jobs`, `related_jobs` | `Job` |
| `desired_outcomes`, `related_job` | `DesiredOutcome` / `Job` |
| `product_outcomes`, `lane` | `ProductOutcome` / `InvestmentLane` |
| `informed_by_outcomes` | `DesiredOutcome` |
| `realizes_product_outcomes` | `ProductOutcome` |
| `supports_jobs` | `Job` |
| `supports_desired_outcomes` | `DesiredOutcome` |
| `satisfies_requirements` / `satisfied_by_capabilities` | `Requirement` / `Capability` |

**Exception:** `sali_tags` remains `uriorcurie` (external SALI LMSS concepts, not in-schema classes) → stored as TEXT.

### 4.3 Why not rely on raw `gen-sqltables` alone?

Official pipeline:

`SchemaView` → `RelationalModelTransformer` → `SQLTableGenerator`

Gaps relative to production needs:

| Issue | Generator behavior | Our physical choice |
|-------|--------------------|---------------------|
| Join PKs | Surrogate `INTEGER id` | **Composite natural keys** |
| FK names | Often `child_jobs_id_id` | **Clean** `child_job_id` |
| Table names | PascalCase (`Job`) | **snake_case** (`job`) |
| Abstract bases | Optional tables | **Omit** (`Identifiable`, etc.) |
| Views | None | Hierarchy + traceability views |

**Canonical physical DDL is `schema.sql`**, derived from LinkML *plus* these physical conventions—not a competing hand model of the domain.

Raw generator output is kept as `generated_schema.sql` for regression comparison. Intermediate relational LinkML: `unified_relmodel.yaml`.

---

## 5. Database conventions (`schema.sql` / `jtbd.sqlite`)

### 5.1 Node tables

`job`, `desired_outcome`, `investment_lane`, `product_outcome`, `requirement`, `capability`

- PK: `id TEXT` (SemanticId)  
- Shared columns where applicable: `pref_label`, `description`, `status`, `version`  
- `job.parent_job_id` → `job(id)`  
- `desired_outcome.related_job_id` → `job(id)`  
- `product_outcome.lane_id` → `investment_lane(id)`  

### 5.2 Edge tables (composite PKs)

| Table | PK | Notes |
|-------|-----|--------|
| `job_child` | `(parent_job_id, child_job_id)` | optional `sequence_order` |
| `job_related` | `(job_id, related_job_id)` | |
| `job_desired_outcome` | `(job_id, desired_outcome_id)` | |
| `job_sali_tag` | `(job_id, sali_tag)` | tag is TEXT |
| `lane_product_outcome` | `(lane_id, product_outcome_id)` | |
| `product_outcome_informed_by` | `(product_outcome_id, desired_outcome_id)` | |
| `requirement_realizes_product_outcome` | `(requirement_id, product_outcome_id)` | |
| `requirement_satisfied_by_capability` | `(requirement_id, capability_id)` | |
| `requirement_acceptance_criterion` | `(requirement_id, criterion)` | + `position` |
| `capability_satisfies_requirement` | `(capability_id, requirement_id)` | |
| `capability_supports_job` | `(capability_id, job_id)` | |
| `capability_supports_desired_outcome` | `(capability_id, desired_outcome_id)` | |

FKs use `ON DELETE CASCADE` on edge endpoints where appropriate.

### 5.3 Views

- `v_job_hierarchy` — top → mid → micro  
- `v_node_catalog` — union of all node types  
- `v_traceability` — job → outcome → product outcome → requirement → capability  

### 5.4 Load path

```text
jobs-instance.yaml
investments-instance.yaml
product-requirements-instance.yaml
        │
        ▼
   load_db.py  +  schema.sql
        │
        ▼
   jtbd.sqlite
```

Instance CURIEs **must** resolve to IDs present in `jobs-instance.yaml` (T1–T6 era). Legacy IDs such as `jtbd:JOB-PROTECT-RIGHTS` or `jtbd:OUT-MIN-COST-DISCOVERY` are obsolete.

---

## 6. UI (`jtbd-editor.html`)

**JTBD Workbench** — single-page editor for navigation and light editing.

### 6.1 Layout

- **Left:** search, level filters, collapsible job tree (or list for other collections)  
- **Center:** detail form / list / trace table  
- **Right:** path-length-1 connections for the selection  

### 6.2 Data

- Embedded sample from `sample-data.json` (built from YAML instances)  
- **Reload sample** resets from embed (works on `file://`)  
- **Export YAML / JSON** downloads current in-memory model  

### 6.3 Conventions in the UI

- Level badges on every job: `[top]` `[mid]` `[micro]`  
- Iterative mids marked with ↻  
- Related jobs (R*) under a separate tree section  

The editor is a **catalog/maintenance UI**, not a multi-user server. Persistence is export → YAML → `load_db.py` (or future WASM SQLite).

---

## 7. Architecture notes (future storage)

Discussed target shape (not fully implemented in this zip beyond static files):

```text
Static site (HTML/JS)  ← served from object storage / any static host
        │
        ▼
Browser + optional SQLite WASM
        │
        ▼
jtbd.sqlite  (same bucket or separate object; single-writer limitations)
```

- WASM does **not** serve the UI; the UI is static HTML.  
- Putting `jtbd.sqlite` in the **same S3 bucket** as the site is fine if fetch/CORS/presigned access is configured.  
- **Not multi-user safe** as a single shared SQLite file without a coordination layer.

---

## 8. File inventory

| Path | Role |
|------|------|
| `AGENT.md` | This document |
| `graph_foundation.yaml` | Shared identity & abstract graph types |
| `jobs.yaml` / `investments.yaml` / `product_requirements.yaml` | LinkML schemas v0.4.0 |
| `jobs-instance.yaml` | Full job hierarchy + outcomes |
| `investments-instance.yaml` | Lanes + product outcomes (CURIEs aligned) |
| `product-requirements-instance.yaml` | Requirements + capabilities (CURIEs aligned) |
| `unified_inline.yaml` | Merged schema for tooling |
| `unified_relmodel.yaml` | LinkML relational transform output |
| `generated_schema.sql` | Raw `gen-sqltables`-style DDL (reference) |
| `schema.sql` | **Canonical physical DDL** |
| `jtbd.sqlite` | Loaded database |
| `load_db.py` | YAML → SQLite loader |
| `example_queries.sql` | Sample queries |
| `jtbd-editor.html` | Workbench UI |
| `sample-data.json` | Compact sample for the editor |
| `jobs-hierarchy.xlsx` | Spreadsheet export of job tree + outcomes |

---

## 9. Agent / contributor checklist

When changing this system:

1. **Prefer SemanticId CURIEs** for all domain identity.  
2. **Preserve three levels** (top / mid / micro) and `iterative` on mids that loop.  
3. **Class-range** multivalued slots that must FK in SQL; keep external refs as `uriorcurie` only when intentionally out-of-schema.  
4. After schema edits: refresh `unified_inline.yaml` → optional `generated_schema.sql` → update **`schema.sql`** physical conventions → `load_db.py` → `jtbd.sqlite`.  
5. After instance edits: realign inv/req CURIEs to job/outcome IDs → reload DB → regenerate `sample-data.json` and refresh editor embed if needed.  
6. Do **not** reintroduce obsolete job IDs (`JOB-PROTECT-RIGHTS`, `JOB-DISCOVERY-MANAGE`, etc.).  
7. Do **not** treat raw generator DDL as production without composite keys and clean names.  

---

## 10. Quick start

```bash
# Inspect DB (if sqlite3 available)
sqlite3 jtbd.sqlite "SELECT top_label, mid_label, micro_label FROM v_job_hierarchy LIMIT 10;"

# Reload DB from YAML
python3 load_db.py

# Open UI
open jtbd-editor.html   # or double-click / serve statically
```

---

*Package version aligns with LinkML schemas **0.4.0** and the T1–T6 litigation JTBD breakdown agreed in design sessions.*


## 11. Kalbach descriptive fields (v0.5.0)

Additive Job fields (process still = hierarchy only):

- Statement: `job_statement`, `statement_verb`, `statement_object`, `statement_clarifier`
- Who: `job_performer`, `buyer_role`
- Circumstances: `circumstance_situation`, `circumstance_constraints` (table `job_circumstance_constraint`)
- Emotional / social: `emotional_job`, `social_job`
- Done + story: `end_state`, `job_story_*`
- Outcome: `object_of_control`

See `TASKS-missing-fields.md`. T1–T6 tops are backfilled.

## 12. schema.sql is always generated

**Rule:** `schema.sql` is a **generated** artifact. Do not hand-edit it.

Pipeline:

1. Edit LinkML YAML (`graph_foundation.yaml`, `jobs.yaml`, `investments.yaml`, `product_requirements.yaml`)
2. Run `python3 generate_schema.py` (builds `unified_inline.yaml` + physical `schema.sql`)
3. Run `python3 load_db.py` → `jtbd.sqlite`

Brute-force edits to `schema.sql` require explicit human permission.
Physical conventions (snake_case, composite edge PKs, views) live in `generate_schema.py`, not in one-off SQL patches.

## 13. Editor vs database (known gap)

| Path | Status |
|------|--------|
| YAML instances → `load_db.py` → `jtbd.sqlite` | **Works** |
| YAML/`sample-data.json` embedded → `jtbd-editor.html` | **Works** |
| Editor reads/writes `jtbd.sqlite` | **Gap** — editor does not use SQLite/WASM |

Today the editor is a **catalog UI over embedded JSON** (exported from YAML). The database is a **separate queryable store** loaded from the same YAML. They stay aligned when you:

1. Edit YAML (or export from editor → replace YAML)
2. `python3 load_db.py`
3. Refresh `sample-data.json` into the editor embed (or re-export pipeline)

Future option: SQLite WASM in the browser loading `jtbd.sqlite` (discussed architecture; not implemented).
