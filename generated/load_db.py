#!/usr/bin/env python3
"""Load LinkML YAML instances into jtbd.sqlite using schema.sql (composite-key physical model)."""
import sqlite3
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "jtbd.sqlite"

def main():
    schema = (ROOT / "schema.sql").read_text()
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(str(DB))
    conn.executescript(schema)
    conn.execute("PRAGMA foreign_keys = OFF")

    def load(name):
        return yaml.safe_load((ROOT / name).read_text())

    jobs_data = load("jobs-instance.yaml")
    inv_data = load("investments-instance.yaml")
    req_data = load("product-requirements-instance.yaml")
    cur = conn.cursor()
    job_ids, outcome_ids, lane_ids, pout_ids, req_ids = set(), set(), set(), set(), set()

    for j in jobs_data.get("jobs") or []:
        job_ids.add(j["id"])
        cur.execute(
            """INSERT INTO job (id, pref_label, description, status, version, job_level, phase,
               parent_job_id, sequence_order, iterative, last_reviewed,
               job_statement, statement_verb, statement_object, statement_clarifier,
               job_performer, buyer_role, circumstance_situation,
               emotional_job, social_job, end_state,
               job_story_situation, job_story_motivation, job_story_expected_outcome)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (j["id"], j.get("pref_label"), j.get("description"), j.get("status") or "active",
             j.get("version"), j.get("job_level"), j.get("phase"), j.get("parent_job"),
             j.get("sequence_order"),
             1 if j.get("iterative") is True else (0 if j.get("iterative") is False else None),
             str(j["last_reviewed"]) if j.get("last_reviewed") else None,
             j.get("job_statement"), j.get("statement_verb"), j.get("statement_object"),
             j.get("statement_clarifier"), j.get("job_performer"), j.get("buyer_role"),
             j.get("circumstance_situation"), j.get("emotional_job"), j.get("social_job"),
             j.get("end_state"), j.get("job_story_situation"), j.get("job_story_motivation"),
             j.get("job_story_expected_outcome")),
        )
        for ctext in j.get("circumstance_constraints") or []:
            cur.execute(
                "INSERT OR IGNORE INTO job_circumstance_constraint (job_id, constraint_text) VALUES (?,?)",
                (j["id"], ctext),
            )
    for j in jobs_data.get("jobs") or []:
        if j.get("parent_job") in job_ids:
            cur.execute("UPDATE job SET parent_job_id=? WHERE id=?", (j["parent_job"], j["id"]))
        for i, cid in enumerate(j.get("child_jobs") or []):
            if cid in job_ids:
                cur.execute(
                    "INSERT OR IGNORE INTO job_child (parent_job_id, child_job_id, sequence_order) VALUES (?,?,?)",
                    (j["id"], cid, i + 1),
                )
        for rid in j.get("related_jobs") or []:
            if rid in job_ids:
                cur.execute("INSERT OR IGNORE INTO job_related VALUES (?,?)", (j["id"], rid))
        for tag in j.get("sali_tags") or []:
            cur.execute("INSERT OR IGNORE INTO job_sali_tag VALUES (?,?)", (j["id"], tag))

    for o in jobs_data.get("desired_outcomes") or []:
        outcome_ids.add(o["id"])
        cur.execute(
            """INSERT INTO desired_outcome (id, pref_label, description, status, version, statement,
               direction, unit_of_measure, object_of_control, qualifier, importance, satisfaction, opportunity_score, related_job_id)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (o["id"], o.get("pref_label"), o.get("description"), o.get("status") or "active",
             o.get("version"), o.get("statement"), o.get("direction"), o.get("unit_of_measure"),
             o.get("object_of_control"), o.get("qualifier"), o.get("importance"), o.get("satisfaction"),
             o.get("opportunity_score"),
             o.get("related_job") if o.get("related_job") in job_ids else None),
        )
    for j in jobs_data.get("jobs") or []:
        for oid in j.get("desired_outcomes") or []:
            if oid in outcome_ids:
                cur.execute("INSERT OR IGNORE INTO job_desired_outcome VALUES (?,?)", (j["id"], oid))

    for lane in inv_data.get("investment_lanes") or []:
        lane_ids.add(lane["id"])
        cur.execute(
            """INSERT INTO investment_lane (id, pref_label, description, status, version, horizon, strategic_weight, owner)
               VALUES (?,?,?,?,?,?,?,?)""",
            (lane["id"], lane.get("pref_label"), lane.get("description"), lane.get("status") or "active",
             lane.get("version"), lane.get("horizon"), lane.get("strategic_weight"), lane.get("owner")),
        )
    for po in inv_data.get("product_outcomes") or []:
        pout_ids.add(po["id"])
        lane_id = po.get("lane") or po.get("investment_lane")
        if lane_id not in lane_ids:
            lane_id = next(iter(lane_ids), None)
        cur.execute(
            """INSERT INTO product_outcome (id, pref_label, description, status, version,
               target_metric, target_value, current_value, target_date, lane_id)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (po["id"], po.get("pref_label"), po.get("description"), po.get("status") or "active",
             po.get("version"), po.get("metric") or po.get("target_metric"),
             po.get("target") or po.get("target_value"), po.get("current_value"),
             str(po["target_date"]) if po.get("target_date") else None, lane_id),
        )
        for oid in po.get("informed_by_outcomes") or []:
            if oid in outcome_ids:
                cur.execute("INSERT OR IGNORE INTO product_outcome_informed_by VALUES (?,?)", (po["id"], oid))
    for lane in inv_data.get("investment_lanes") or []:
        for pid in lane.get("product_outcomes") or []:
            if pid in pout_ids:
                cur.execute("INSERT OR IGNORE INTO lane_product_outcome VALUES (?,?)", (lane["id"], pid))

    for r in req_data.get("requirements") or []:
        req_ids.add(r["id"])
        cur.execute(
            """INSERT INTO requirement (id, pref_label, description, status, version, requirement_type, priority)
               VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r.get("pref_label"), r.get("description"), r.get("status") or "active",
             r.get("version"), r.get("requirement_type") or "functional", r.get("priority")),
        )
        for i, ac in enumerate(r.get("acceptance_criteria") or []):
            cur.execute(
                "INSERT OR IGNORE INTO requirement_acceptance_criterion VALUES (?,?,?)",
                (r["id"], ac, i),
            )
        for pid in r.get("realizes_product_outcomes") or []:
            if pid in pout_ids:
                cur.execute(
                    "INSERT OR IGNORE INTO requirement_realizes_product_outcome VALUES (?,?)",
                    (r["id"], pid),
                )

    for c in req_data.get("capabilities") or []:
        cur.execute(
            """INSERT INTO capability (id, pref_label, description, status, version, capability_type, implementation_status, owner)
               VALUES (?,?,?,?,?,?,?,?)""",
            (c["id"], c.get("pref_label"), c.get("description"), c.get("status") or "active",
             c.get("version"), c.get("capability_type"), c.get("implementation_status"), c.get("owner")),
        )
        for rid in c.get("satisfies_requirements") or []:
            if rid in req_ids:
                cur.execute("INSERT OR IGNORE INTO capability_satisfies_requirement VALUES (?,?)", (c["id"], rid))
                cur.execute("INSERT OR IGNORE INTO requirement_satisfied_by_capability VALUES (?,?)", (rid, c["id"]))
        for jid in c.get("supports_jobs") or []:
            if jid in job_ids:
                cur.execute("INSERT OR IGNORE INTO capability_supports_job VALUES (?,?)", (c["id"], jid))
        for oid in c.get("supports_desired_outcomes") or []:
            if oid in outcome_ids:
                cur.execute("INSERT OR IGNORE INTO capability_supports_desired_outcome VALUES (?,?)", (c["id"], oid))

    conn.commit()
    for t in ("job", "desired_outcome", "investment_lane", "product_outcome", "requirement", "capability"):
        print(t, cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    conn.close()
    print("Wrote", DB)

if __name__ == "__main__":
    main()
