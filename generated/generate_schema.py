#!/usr/bin/env python3
"""Generate schema.sql from LinkML schemas (physical conventions applied in code)."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent

NODE_CLASS_MAP = {
    "Job": "job",
    "DesiredOutcome": "desired_outcome",
    "InvestmentLane": "investment_lane",
    "ProductOutcome": "product_outcome",
    "Requirement": "requirement",
    "Capability": "capability",
}

# Multivalued slots → edge tables (composite PK). Value-only edges have ctable None.
# (slot_name, parent_class, edge_table, parent_col, child_col, child_table_or_None, extra_cols)
EDGE_SPECS = [
    ("child_jobs", "Job", "job_child", "parent_job_id", "child_job_id", "job", [("sequence_order", "INTEGER")]),
    ("related_jobs", "Job", "job_related", "job_id", "related_job_id", "job", []),
    ("desired_outcomes", "Job", "job_desired_outcome", "job_id", "desired_outcome_id", "desired_outcome", []),
    ("sali_tags", "Job", "job_sali_tag", "job_id", "sali_tag", None, []),
    ("circumstance_constraints", "Job", "job_circumstance_constraint", "job_id", "constraint_text", None, []),
    ("product_outcomes", "InvestmentLane", "lane_product_outcome", "lane_id", "product_outcome_id", "product_outcome", []),
    ("informed_by_outcomes", "ProductOutcome", "product_outcome_informed_by", "product_outcome_id", "desired_outcome_id", "desired_outcome", []),
    ("realizes_product_outcomes", "Requirement", "requirement_realizes_product_outcome", "requirement_id", "product_outcome_id", "product_outcome", []),
    ("satisfied_by_capabilities", "Requirement", "requirement_satisfied_by_capability", "requirement_id", "capability_id", "capability", []),
    ("acceptance_criteria", "Requirement", "requirement_acceptance_criterion", "requirement_id", "criterion", None, [("position", "INTEGER")]),
    ("satisfies_requirements", "Capability", "capability_satisfies_requirement", "capability_id", "requirement_id", "requirement", []),
    ("supports_jobs", "Capability", "capability_supports_job", "capability_id", "job_id", "job", []),
    ("supports_desired_outcomes", "Capability", "capability_supports_desired_outcome", "capability_id", "desired_outcome_id", "desired_outcome", []),
]

def snake(name: str) -> str:
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.replace("__", "_").lower().strip("_")

def load_yaml(p):
    return yaml.safe_load(Path(p).read_text())

def strip_annotations(obj):
    if isinstance(obj, dict):
        obj.pop("annotations", None)
        for v in list(obj.values()):
            strip_annotations(v)
    elif isinstance(obj, list):
        for v in obj:
            strip_annotations(v)

def build_unified():
    parts = []
    for f in ["graph_foundation.yaml", "jobs.yaml", "investments.yaml", "product_requirements.yaml"]:
        d = load_yaml(ROOT / f)
        strip_annotations(d)
        d.pop("imports", None)
        parts.append(d)
    unified = {
        "id": "https://example.org/legal-jtbd/unified",
        "name": "LegalJTBDUnified",
        "version": "0.5.0",
        "prefixes": {"linkml": "https://w3id.org/linkml/", "jtbd": "https://example.org/legal-jtbd/jobs/"},
        "default_prefix": "jtbd",
        "imports": ["linkml:types"],
        "types": {}, "enums": {}, "slots": {}, "classes": {},
    }
    for d in parts:
        for section in ("prefixes", "types", "enums", "slots", "classes"):
            for k, v in (d.get(section) or {}).items():
                unified[section][k] = v
    if "SemanticId" in unified["types"]:
        unified["types"]["SemanticId"] = {"typeof": "string", "description": "CURIE/IRI semantic id"}
    for abs_name in ("Identifiable", "GraphNode", "GraphEdge"):
        if abs_name in unified["classes"]:
            unified["classes"][abs_name]["abstract"] = True
    (ROOT / "unified_inline.yaml").write_text(
        yaml.dump(unified, sort_keys=False, allow_unicode=True, width=100)
    )
    return unified

def induced_slots(unified, class_name):
    """Walk is_a chain and collect slot names + definitions."""
    classes = unified["classes"]
    slots_meta = unified.get("slots") or {}
    ordered = []
    seen = set()

    def walk(cn):
        c = classes.get(cn) or {}
        parent = c.get("is_a")
        if parent:
            walk(parent)
        for sn in c.get("slots") or []:
            if sn in seen:
                continue
            seen.add(sn)
            ordered.append(sn)
        # attributes inline
        for sn, sd in (c.get("attributes") or {}).items():
            if sn not in seen:
                seen.add(sn)
                ordered.append(sn)
                slots_meta[sn] = sd

    walk(class_name)
    return ordered, slots_meta

def sql_type(range_name, unified):
    if range_name in ("integer", "boolean"):
        return "INTEGER"
    if range_name in ("float", "double"):
        return "REAL"
    return "TEXT"

def col_name_for_slot(sn, range_name):
    col = snake(sn)
    # singular class-valued FK
    if range_name in NODE_CLASS_MAP and not col.endswith("_id"):
        # parent_job → parent_job_id
        col = col + "_id"
    return col

def generate_ddl(unified):
    lines = []
    lines.append("-- ============================================================================")
    lines.append("-- JTBD production schema (GENERATED — do not hand-edit)")
    lines.append("-- Source: LinkML unified v" + str(unified.get("version", "?")))
    lines.append("-- Generator: generate_schema.py")
    lines.append("-- Conventions: snake_case tables, SemanticId TEXT PKs, composite edge PKs")
    lines.append("-- ============================================================================")
    lines.append("PRAGMA foreign_keys = ON;")
    lines.append("")

    # Multivalued slot names to skip on node tables
    multi_slots = {e[0] for e in EDGE_SPECS}

    for cls, table in NODE_CLASS_MAP.items():
        slot_names, slots_meta = induced_slots(unified, cls)
        lines.append(f"CREATE TABLE IF NOT EXISTS {table} (")
        col_defs = []
        pk = None
        fks = []
        for sn in slot_names:
            if sn in multi_slots:
                continue
            sm = slots_meta.get(sn) or {}
            rng = sm.get("range") or "string"
            # skip if range is a class and multivalued was missed
            if sm.get("multivalued"):
                continue
            col = col_name_for_slot(sn, rng)
            # normalize known names
            if col == "parent_job":
                col = "parent_job_id"
            if col == "related_job":
                col = "related_job_id"
            if col == "lane" and table == "product_outcome":
                col = "lane_id"
            st = sql_type(rng, unified)
            is_id = sn == "id" or sm.get("identifier")
            required = bool(sm.get("required") or is_id)
            # class range → FK text
            if rng in NODE_CLASS_MAP:
                st = "TEXT"
                if not col.endswith("_id"):
                    col = col + "_id"
                if not is_id:
                    fks.append((col, NODE_CLASS_MAP[rng]))
            nullsql = " NOT NULL" if required else ""
            col_defs.append(f"  {col} {st}{nullsql}")
            if is_id:
                pk = col
        if pk:
            col_defs.append(f"  PRIMARY KEY ({pk})")
        for col, ref in fks:
            col_defs.append(f"  FOREIGN KEY ({col}) REFERENCES {ref}(id)")
        lines.append(",\n".join(col_defs))
        lines.append(");")
        lines.append(f"CREATE INDEX IF NOT EXISTS ix_{table}_id ON {table}(id);")
        lines.append("")

    for slot, parent_cls, edge_table, pcol, ccol, ctable, extras in EDGE_SPECS:
        ptable = NODE_CLASS_MAP[parent_cls]
        lines.append(f"CREATE TABLE IF NOT EXISTS {edge_table} (")
        defs = [f"  {pcol} TEXT NOT NULL", f"  {ccol} TEXT NOT NULL"]
        for ecol, etype in extras:
            defs.append(f"  {ecol} {etype}")
        defs.append(f"  PRIMARY KEY ({pcol}, {ccol})")
        defs.append(f"  FOREIGN KEY ({pcol}) REFERENCES {ptable}(id) ON DELETE CASCADE")
        if ctable:
            defs.append(f"  FOREIGN KEY ({ccol}) REFERENCES {ctable}(id) ON DELETE CASCADE")
        lines.append(",\n".join(defs))
        lines.append(");")
        lines.append(f"CREATE INDEX IF NOT EXISTS ix_{edge_table}_{pcol} ON {edge_table}({pcol});")
        if ctable:
            lines.append(f"CREATE INDEX IF NOT EXISTS ix_{edge_table}_{ccol} ON {edge_table}({ccol});")
        lines.append("")

    lines.append("""CREATE VIEW IF NOT EXISTS v_job_hierarchy AS
SELECT
  t.id AS top_id, t.pref_label AS top_label,
  m.id AS mid_id, m.pref_label AS mid_label, m.iterative AS mid_iterative,
  mi.id AS micro_id, mi.pref_label AS micro_label, mi.sequence_order AS micro_seq,
  COALESCE(mi.phase, m.phase, t.phase) AS phase
FROM job t
LEFT JOIN job m ON m.parent_job_id = t.id AND m.job_level = 'mid_level'
LEFT JOIN job mi ON mi.parent_job_id = m.id AND mi.job_level = 'micro'
WHERE t.job_level = 'top_level'
ORDER BY t.id, m.sequence_order, mi.sequence_order;
""")
    lines.append("""CREATE VIEW IF NOT EXISTS v_node_catalog AS
SELECT 'job' AS node_type, id, pref_label, status FROM job
UNION ALL SELECT 'desired_outcome', id, pref_label, status FROM desired_outcome
UNION ALL SELECT 'investment_lane', id, pref_label, status FROM investment_lane
UNION ALL SELECT 'product_outcome', id, pref_label, status FROM product_outcome
UNION ALL SELECT 'requirement', id, pref_label, status FROM requirement
UNION ALL SELECT 'capability', id, pref_label, status FROM capability;
""")
    lines.append("""CREATE VIEW IF NOT EXISTS v_traceability AS
SELECT
  j.id AS job_id, j.pref_label AS job_label, j.job_level,
  o.id AS outcome_id, o.pref_label AS outcome_label, o.opportunity_score,
  po.id AS product_outcome_id, po.pref_label AS product_outcome_label,
  r.id AS requirement_id, r.pref_label AS requirement_label, r.priority,
  c.id AS capability_id, c.pref_label AS capability_label, c.implementation_status
FROM job j
LEFT JOIN job_desired_outcome jdo ON jdo.job_id = j.id
LEFT JOIN desired_outcome o ON o.id = jdo.desired_outcome_id
LEFT JOIN product_outcome_informed_by poib ON poib.desired_outcome_id = o.id
LEFT JOIN product_outcome po ON po.id = poib.product_outcome_id
LEFT JOIN requirement_realizes_product_outcome rrpo ON rrpo.product_outcome_id = po.id
LEFT JOIN requirement r ON r.id = rrpo.requirement_id
LEFT JOIN requirement_satisfied_by_capability rsc ON rsc.requirement_id = r.id
LEFT JOIN capability c ON c.id = rsc.capability_id;
""")
    return "\n".join(lines)

def main():
    unified = build_unified()
    ddl = generate_ddl(unified)
    out = ROOT / "schema.sql"
    out.write_text(ddl)
    print(f"Wrote {out} ({len(ddl.splitlines())} lines)")
    # sanity: Kalbach fields present
    for col in ("job_statement", "job_performer", "end_state", "object_of_control"):
        assert col in ddl, f"missing generated column {col}"
    assert "job_circumstance_constraint" in ddl
    print("OK: Kalbach fields present in generated DDL")

if __name__ == "__main__":
    main()
