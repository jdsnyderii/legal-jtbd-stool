-- ============================================================================
-- JTBD production schema (GENERATED — do not hand-edit)
-- Source: LinkML unified v0.5.0
-- Generator: generate_schema.py
-- Conventions: snake_case tables, SemanticId TEXT PKs, composite edge PKs
-- ============================================================================
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS job (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  job_level TEXT NOT NULL,
  parent_job_id TEXT,
  phase TEXT,
  last_reviewed TEXT,
  sequence_order INTEGER,
  iterative INTEGER,
  job_statement TEXT,
  statement_verb TEXT,
  statement_object TEXT,
  statement_clarifier TEXT,
  job_performer TEXT,
  buyer_role TEXT,
  circumstance_situation TEXT,
  emotional_job TEXT,
  social_job TEXT,
  end_state TEXT,
  job_story_situation TEXT,
  job_story_motivation TEXT,
  job_story_expected_outcome TEXT,
  PRIMARY KEY (id),
  FOREIGN KEY (parent_job_id) REFERENCES job(id)
);
CREATE INDEX IF NOT EXISTS ix_job_id ON job(id);

CREATE TABLE IF NOT EXISTS desired_outcome (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  statement TEXT,
  direction TEXT,
  unit_of_measure TEXT,
  qualifier TEXT,
  importance INTEGER,
  satisfaction INTEGER,
  opportunity_score REAL,
  related_job_id TEXT,
  object_of_control TEXT,
  PRIMARY KEY (id),
  FOREIGN KEY (related_job_id) REFERENCES job(id)
);
CREATE INDEX IF NOT EXISTS ix_desired_outcome_id ON desired_outcome(id);

CREATE TABLE IF NOT EXISTS investment_lane (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  horizon TEXT,
  strategic_weight REAL,
  owner TEXT,
  PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_investment_lane_id ON investment_lane(id);

CREATE TABLE IF NOT EXISTS product_outcome (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  lane_id TEXT,
  target_metric TEXT,
  target_value TEXT,
  current_value TEXT,
  target_date TEXT,
  PRIMARY KEY (id),
  FOREIGN KEY (lane_id) REFERENCES investment_lane(id)
);
CREATE INDEX IF NOT EXISTS ix_product_outcome_id ON product_outcome(id);

CREATE TABLE IF NOT EXISTS requirement (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  requirement_type TEXT,
  priority TEXT,
  PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_requirement_id ON requirement(id);

CREATE TABLE IF NOT EXISTS capability (
  id TEXT NOT NULL,
  pref_label TEXT,
  description TEXT,
  status TEXT NOT NULL,
  version TEXT,
  capability_type TEXT,
  implementation_status TEXT,
  owner TEXT,
  PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_capability_id ON capability(id);

CREATE TABLE IF NOT EXISTS job_child (
  parent_job_id TEXT NOT NULL,
  child_job_id TEXT NOT NULL,
  sequence_order INTEGER,
  PRIMARY KEY (parent_job_id, child_job_id),
  FOREIGN KEY (parent_job_id) REFERENCES job(id) ON DELETE CASCADE,
  FOREIGN KEY (child_job_id) REFERENCES job(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_job_child_parent_job_id ON job_child(parent_job_id);
CREATE INDEX IF NOT EXISTS ix_job_child_child_job_id ON job_child(child_job_id);

CREATE TABLE IF NOT EXISTS job_related (
  job_id TEXT NOT NULL,
  related_job_id TEXT NOT NULL,
  PRIMARY KEY (job_id, related_job_id),
  FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE,
  FOREIGN KEY (related_job_id) REFERENCES job(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_job_related_job_id ON job_related(job_id);
CREATE INDEX IF NOT EXISTS ix_job_related_related_job_id ON job_related(related_job_id);

CREATE TABLE IF NOT EXISTS job_desired_outcome (
  job_id TEXT NOT NULL,
  desired_outcome_id TEXT NOT NULL,
  PRIMARY KEY (job_id, desired_outcome_id),
  FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE,
  FOREIGN KEY (desired_outcome_id) REFERENCES desired_outcome(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_job_desired_outcome_job_id ON job_desired_outcome(job_id);
CREATE INDEX IF NOT EXISTS ix_job_desired_outcome_desired_outcome_id ON job_desired_outcome(desired_outcome_id);

CREATE TABLE IF NOT EXISTS job_sali_tag (
  job_id TEXT NOT NULL,
  sali_tag TEXT NOT NULL,
  PRIMARY KEY (job_id, sali_tag),
  FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_job_sali_tag_job_id ON job_sali_tag(job_id);

CREATE TABLE IF NOT EXISTS job_circumstance_constraint (
  job_id TEXT NOT NULL,
  constraint_text TEXT NOT NULL,
  PRIMARY KEY (job_id, constraint_text),
  FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_job_circumstance_constraint_job_id ON job_circumstance_constraint(job_id);

CREATE TABLE IF NOT EXISTS lane_product_outcome (
  lane_id TEXT NOT NULL,
  product_outcome_id TEXT NOT NULL,
  PRIMARY KEY (lane_id, product_outcome_id),
  FOREIGN KEY (lane_id) REFERENCES investment_lane(id) ON DELETE CASCADE,
  FOREIGN KEY (product_outcome_id) REFERENCES product_outcome(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_lane_product_outcome_lane_id ON lane_product_outcome(lane_id);
CREATE INDEX IF NOT EXISTS ix_lane_product_outcome_product_outcome_id ON lane_product_outcome(product_outcome_id);

CREATE TABLE IF NOT EXISTS product_outcome_informed_by (
  product_outcome_id TEXT NOT NULL,
  desired_outcome_id TEXT NOT NULL,
  PRIMARY KEY (product_outcome_id, desired_outcome_id),
  FOREIGN KEY (product_outcome_id) REFERENCES product_outcome(id) ON DELETE CASCADE,
  FOREIGN KEY (desired_outcome_id) REFERENCES desired_outcome(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_product_outcome_informed_by_product_outcome_id ON product_outcome_informed_by(product_outcome_id);
CREATE INDEX IF NOT EXISTS ix_product_outcome_informed_by_desired_outcome_id ON product_outcome_informed_by(desired_outcome_id);

CREATE TABLE IF NOT EXISTS requirement_realizes_product_outcome (
  requirement_id TEXT NOT NULL,
  product_outcome_id TEXT NOT NULL,
  PRIMARY KEY (requirement_id, product_outcome_id),
  FOREIGN KEY (requirement_id) REFERENCES requirement(id) ON DELETE CASCADE,
  FOREIGN KEY (product_outcome_id) REFERENCES product_outcome(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_requirement_realizes_product_outcome_requirement_id ON requirement_realizes_product_outcome(requirement_id);
CREATE INDEX IF NOT EXISTS ix_requirement_realizes_product_outcome_product_outcome_id ON requirement_realizes_product_outcome(product_outcome_id);

CREATE TABLE IF NOT EXISTS requirement_satisfied_by_capability (
  requirement_id TEXT NOT NULL,
  capability_id TEXT NOT NULL,
  PRIMARY KEY (requirement_id, capability_id),
  FOREIGN KEY (requirement_id) REFERENCES requirement(id) ON DELETE CASCADE,
  FOREIGN KEY (capability_id) REFERENCES capability(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_requirement_satisfied_by_capability_requirement_id ON requirement_satisfied_by_capability(requirement_id);
CREATE INDEX IF NOT EXISTS ix_requirement_satisfied_by_capability_capability_id ON requirement_satisfied_by_capability(capability_id);

CREATE TABLE IF NOT EXISTS requirement_acceptance_criterion (
  requirement_id TEXT NOT NULL,
  criterion TEXT NOT NULL,
  position INTEGER,
  PRIMARY KEY (requirement_id, criterion),
  FOREIGN KEY (requirement_id) REFERENCES requirement(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_requirement_acceptance_criterion_requirement_id ON requirement_acceptance_criterion(requirement_id);

CREATE TABLE IF NOT EXISTS capability_satisfies_requirement (
  capability_id TEXT NOT NULL,
  requirement_id TEXT NOT NULL,
  PRIMARY KEY (capability_id, requirement_id),
  FOREIGN KEY (capability_id) REFERENCES capability(id) ON DELETE CASCADE,
  FOREIGN KEY (requirement_id) REFERENCES requirement(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_capability_satisfies_requirement_capability_id ON capability_satisfies_requirement(capability_id);
CREATE INDEX IF NOT EXISTS ix_capability_satisfies_requirement_requirement_id ON capability_satisfies_requirement(requirement_id);

CREATE TABLE IF NOT EXISTS capability_supports_job (
  capability_id TEXT NOT NULL,
  job_id TEXT NOT NULL,
  PRIMARY KEY (capability_id, job_id),
  FOREIGN KEY (capability_id) REFERENCES capability(id) ON DELETE CASCADE,
  FOREIGN KEY (job_id) REFERENCES job(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_capability_supports_job_capability_id ON capability_supports_job(capability_id);
CREATE INDEX IF NOT EXISTS ix_capability_supports_job_job_id ON capability_supports_job(job_id);

CREATE TABLE IF NOT EXISTS capability_supports_desired_outcome (
  capability_id TEXT NOT NULL,
  desired_outcome_id TEXT NOT NULL,
  PRIMARY KEY (capability_id, desired_outcome_id),
  FOREIGN KEY (capability_id) REFERENCES capability(id) ON DELETE CASCADE,
  FOREIGN KEY (desired_outcome_id) REFERENCES desired_outcome(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_capability_supports_desired_outcome_capability_id ON capability_supports_desired_outcome(capability_id);
CREATE INDEX IF NOT EXISTS ix_capability_supports_desired_outcome_desired_outcome_id ON capability_supports_desired_outcome(desired_outcome_id);

CREATE VIEW IF NOT EXISTS v_job_hierarchy AS
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

CREATE VIEW IF NOT EXISTS v_node_catalog AS
SELECT 'job' AS node_type, id, pref_label, status FROM job
UNION ALL SELECT 'desired_outcome', id, pref_label, status FROM desired_outcome
UNION ALL SELECT 'investment_lane', id, pref_label, status FROM investment_lane
UNION ALL SELECT 'product_outcome', id, pref_label, status FROM product_outcome
UNION ALL SELECT 'requirement', id, pref_label, status FROM requirement
UNION ALL SELECT 'capability', id, pref_label, status FROM capability;

CREATE VIEW IF NOT EXISTS v_traceability AS
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
