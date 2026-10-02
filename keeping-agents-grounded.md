# Keeping Agents Grounded

A plain-language guide to how this project turns **ideas about legal work** into **structured data** that people and software (including AI agents) can share, check, and query.

---

## Why this matters

When teams and AI assistants talk about “jobs to be done,” investments, or product requirements, it is easy to drift: names change, levels get mixed up, and nobody is sure what is official.

This project uses a **chain of controlled steps** so that:

1. The **rules** for what a “job” is are written down once.
2. The **catalog** of real jobs (and related items) follows those rules.
3. A **database** is built from those same rules—not invented ad hoc.
4. The **data** is loaded into that database in a repeatable way.

That chain is what “keeping agents grounded” means here: answers and edits should stay tied to the same models and the same loaded facts.

---

## The big picture (four steps)

Think of it like a filing system for a law firm’s playbook:

| Step | Everyday analogy | In this project |
|------|------------------|-----------------|
| **1. Define the forms** | Design the blank forms (what fields exist, what is required) | **LinkML models** (YAML “schemas”) |
| **2. Combine the forms** | Put all form types in one binder so nothing is missing | **Unified model** (all legs of the stool together) |
| **3. Build the filing cabinets** | Build drawers and folders that match the forms | **Database schema** (`schema.sql` → SQLite) |
| **4. File the real papers** | Fill out forms and put them in the right drawers | **Instance data** (YAML) → **load into the database** |

```
LinkML models  →  Unified model  →  Database structure  →  Loaded catalog
   (rules)         (one binder)      (empty cabinets)      (filled cabinets)
```

Nothing in step 4 should invent new field types that step 1 did not define. The database structure should come from the models, not from one-off hand edits.

---

## Step 1 — LinkML models (“the rules”)

**LinkML** is a way to write **definitions** in simple structured text files (YAML): what kinds of things exist, what labels they have, and how they connect.

In this project the “three-legged stool” is split into separate rule books so each leg can evolve clearly:

| File (conceptually) | What it defines |
|---------------------|-----------------|
| Graph foundation | Shared idea of identity (stable IDs like names, not “row number 47”) and whether something is a main thing or a relationship |
| Jobs | Jobs at top / mid / micro levels, desired outcomes, phases, Kalbach-style description fields |
| Investments | Investment lanes and product outcomes |
| Product requirements | Requirements and capabilities |

**For a non-technical reader:** these files are the **dictionary and grammar**. They do not list every litigation job yet; they say what a “job” *is allowed to look like*.

Important design choices baked into the rules:

- **Stable names (semantic IDs)** — e.g. `jtbd:JOB-T1-RESOLVE` — so the same job means the same thing in documents, the UI, and the database.
- **Hierarchy is the process** — how work unfolds is modeled by parent/child jobs and order, not by inventing a second parallel process language.
- **Descriptive Kalbach fields** — who does the job, in what situation, what “done” looks like, etc., sit on the job as attributes.

---

## Step 2 — Combined (unified) model (“one binder”)

Each leg is useful alone, but the product story needs **traceability** across legs, for example:

> Job → desired outcome → product outcome → requirement → capability

So the separate rule books are **merged into one unified model**. That merge is a technical step, but the idea is simple: **one consistent set of rules** before building storage.

Agents (and humans) should treat the unified rules as the contract: if something is not in the model, it is not part of the official catalog shape.

---

## Step 3 — Database schema (“empty cabinets”)

From the unified rules, a **database structure** is **generated**—tables, columns, and relationship tables.

In this project:

- A generator script reads the LinkML rules.
- It writes **`schema.sql`** (the blueprint for SQLite).
- **`schema.sql` is always generated.** It should not be hand-edited as the source of truth. If the cabinets need a new drawer, change the **rules** (LinkML), then regenerate.

What you get in practice:

- One table per major kind of thing (jobs, outcomes, lanes, requirements, capabilities, …).
- Extra tables for many-to-many links (e.g. a job related to several outcomes).
- Views that make common questions easier (hierarchy, end-to-end trace).

**Analogy:** the schema is the labeled empty drawers. Generating it from LinkML keeps the drawers aligned with the dictionary.

---

## Step 4 — Instance data and loading (“filing the papers”)

**Instance data** means the **actual catalog**: the real jobs in litigation, their outcomes, sample investment lanes, and so on—written in YAML files that follow the rules.

Examples of instance files:

- Jobs and desired outcomes  
- Investment lanes and product outcomes  
- Requirements and capabilities  

**Loading** means a script reads those files and inserts them into the database that was created from `schema.sql`.

Order of operations that stays safe:

1. Update or regenerate **`schema.sql`** from LinkML (if rules changed).  
2. Create or refresh the empty database from that schema.  
3. Run the **loader** on the instance YAML files.  
4. Query or browse the result (SQL tools, or a UI that uses an export of the same data).

If the loader fails, that is often a **good** signal: the papers do not match the forms, and the system refused to file them incorrectly.

---

## How this keeps agents grounded

| Risk without this flow | How the flow helps |
|------------------------|--------------------|
| Agent invents new job levels or fields | Levels and fields are fixed in LinkML |
| Same job described three different ways | One semantic ID in instances and database |
| Database columns drift from documentation | Schema is generated from the same LinkML |
| UI shows one story, database another | Both should be fed from the same instance YAML (or a deliberate export of it) |
| “Process” gets reinvented as free text only | Process is the job hierarchy plus shared attributes |

**Grounding rule of thumb:**  
*Change the rules in LinkML → regenerate the schema → update instances → reload the database.*  
Do not start by inventing columns in the database or one-off fields only in a chat.

---

## What is *not* automatic (honest limits)

- The **web editor** in this project primarily works on an **embedded snapshot** of the catalog (for easy local browsing). It is not the same thing as “the database is always live in the browser” unless that is built later.
- **Regenerating** schema and **reloading** data are deliberate steps (scripts), not magic continuous sync.
- **GitHub** holds the source files; a full load still depends on running the generator and loader where the database file is built.

Those limits do not break the mental model; they mean humans (and agents) should still respect the four steps above.

---

## One-page checklist

When someone—or an agent—proposes a change, ask:

1. **Rules** — Does LinkML already allow this field or relationship? If not, update the model first.  
2. **Instances** — Is the real-world catalog updated in the YAML instances?  
3. **Schema** — Was `schema.sql` regenerated from LinkML (not hand-patched)?  
4. **Load** — Was the database reloaded so queries see the new facts?  
5. **Consumers** — Do UI exports or documents still point at the same IDs?

If all five are yes, the system stays grounded.

---

## Glossary (short)

| Term | Meaning in plain language |
|------|---------------------------|
| **LinkML** | Written rules for what our data is allowed to look like |
| **Schema** | Structure of the database (tables and columns) |
| **Instance** | Actual filled-in records (the catalog entries) |
| **Semantic ID** | Stable official name for a record (not “whatever the database numbered it”) |
| **JTBD** | Jobs to be Done—the work someone is trying to get done |
| **Three-legged stool** | Jobs/outcomes + investment lanes + requirements/capabilities |

---

*This note describes the intended metadata flow for the legal JTBD stool project. For implementation detail, see `AGENT.md` and `GENERATE.md` on the domain branch.*
