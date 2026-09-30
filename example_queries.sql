-- Example queries for jtbd.sqlite
SELECT top_label, mid_label, micro_label FROM v_job_hierarchy LIMIT 20;
SELECT COUNT(*) AS jobs FROM job;
SELECT id, job_statement, job_performer FROM job WHERE job_level = 'top_level';
