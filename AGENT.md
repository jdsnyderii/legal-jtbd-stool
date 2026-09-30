# AGENT.md — Legal JTBD Three-Legged Stool

Full design conventions for this package. See also GENERATE.md.

## Purpose

Three legs: Jobs & outcomes | Investment lanes | Requirements & capabilities.

## Semantic identity

Primary keys are SemanticIds (CURIE/IRI), never domain surrogate integers.

## schema.sql is always generated

Edit LinkML YAML, run `python3 generate_schema.py`, then `python3 load_db.py`.
Do not hand-edit schema.sql.

## Process = hierarchy

parent_job / child_jobs / sequence_order / iterative — not process field bags on Main Jobs.

## Kalbach descriptive fields (v0.5.0)

job_statement, statement_verb/object/clarifier, job_performer, buyer_role,
circumstance_situation, circumstance_constraints, emotional_job, social_job,
end_state, job_story_*.

## Editor vs database

Editor uses embedded JSON from YAML. SQLite is separate (load_db.py).
Editor does not read jtbd.sqlite (known gap).

See repository history and local zip for complete narrative AGENT if this summary is abbreviated.
