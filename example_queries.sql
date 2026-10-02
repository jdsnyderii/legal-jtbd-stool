-- Example queries against jtbd.sqlite

-- 1. All top-level jobs
SELECT id, pref_label, phase FROM job WHERE job_level = 'top_level' ORDER BY id;

-- 2. Full hierarchy under T3 (Evidence)
SELECT mid_label, micro_label, micro_seq
FROM v_job_hierarchy
WHERE top_id = 'jtbd:JOB-T3-EVIDENCE'
ORDER BY mid_label, micro_seq;

-- 3. Iterative mid-level jobs
SELECT id, pref_label, phase
FROM job
WHERE job_level = 'mid_level' AND iterative = 1
ORDER BY id;

-- 4. Highest opportunity outcomes
SELECT id, pref_label, opportunity_score, related_job_id
FROM desired_outcome
ORDER BY opportunity_score DESC
LIMIT 15;

-- 5. Outcomes for a job
SELECT o.id, o.pref_label, o.direction, o.unit_of_measure, o.opportunity_score
FROM job_desired_outcome jdo
JOIN desired_outcome o ON o.id = jdo.desired_outcome_id
WHERE jdo.job_id = 'jtbd:JOB-T3-EVIDENCE';

-- 6. Node catalog
SELECT node_type, COUNT(*) FROM v_node_edge_catalog GROUP BY node_type;

-- 7. Path-ish: job -> outcomes (for Connections-style neighborhood)
SELECT j.pref_label AS job, o.pref_label AS outcome
FROM job j
JOIN job_desired_outcome jdo ON jdo.job_id = j.id
JOIN desired_outcome o ON o.id = jdo.desired_outcome_id
WHERE j.job_level = 'top_level';
