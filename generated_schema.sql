-- # Abstract Class: Identifiable Description: Any element that has a stable semantic identity.
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Abstract Class: GraphNode Description: Domain entity that should be treated as a graph node.
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Abstract Class: GraphEdge Description: First-class relationship that itself carries identity and attributes. Use when the edge needs its own metadata.
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Class: Job Description: A job to be done at one of three Kalbach-aligned levels: top_level (Main Job), mid_level (stage in the job map), or micro (micro-job inside a stage).
--     * Slot: job_level Description: top_level = Main Job; mid_level = stage / major step in the job map; micro = micro-job (finest grain inside a stage).
--     * Slot: phase Description: Coarse-grained litigation phase this job primarily belongs to.
--     * Slot: last_reviewed
--     * Slot: sequence_order Description: Optional ordering within a parent (especially useful for micro-jobs that form a sequence inside a mid_level stage).
--     * Slot: iterative Description: True when this mid-level job can legitimately repeat / loop during a matter (e.g. discovery waves, successive motions, negotiation rounds).
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
--     * Slot: parent_job_id Description: Hierarchical parent. A mid_level job points to a top_level job. A micro job points to a mid_level (or occasionally top_level) job.
-- # Class: DesiredOutcome Description: Kalbach-formulated desired outcome statement.
--     * Slot: statement Description: Full Kalbach statement.
--     * Slot: direction
--     * Slot: unit_of_measure
--     * Slot: qualifier
--     * Slot: importance
--     * Slot: satisfaction
--     * Slot: opportunity_score
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
--     * Slot: related_job_id
-- # Class: InvestmentLane
--     * Slot: horizon Description: Now / next / later / explore planning horizon.
--     * Slot: strategic_weight Description: Relative strategic importance of the lane (e.g. 0.0–1.0).
--     * Slot: owner
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Class: ProductOutcome
--     * Slot: target_metric
--     * Slot: target_value
--     * Slot: current_value
--     * Slot: target_date
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
--     * Slot: lane_id
-- # Class: Requirement
--     * Slot: requirement_type
--     * Slot: priority
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Class: Capability
--     * Slot: capability_type
--     * Slot: implementation_status
--     * Slot: owner
--     * Slot: id Description: Canonical, storage-independent identifier.
--     * Slot: pref_label Description: Human-readable preferred label.
--     * Slot: description
--     * Slot: status
--     * Slot: version
-- # Class: Job_sali_tags
--     * Slot: id
--     * Slot: Job_id Description: Autocreated FK slot
--     * Slot: sali_tags Description: External SALI LMSS concept CURIEs (not in-schema classes). Stored as TEXT in SQL.
-- # Class: Job_desired_outcomes
--     * Slot: id
--     * Slot: Job_id Description: Autocreated FK slot
--     * Slot: desired_outcomes_id_id
-- # Class: Job_child_jobs
--     * Slot: id
--     * Slot: Job_id Description: Autocreated FK slot
--     * Slot: child_jobs_id_id Description: Convenience inverse of parent_job. Especially useful for listing the micro-jobs that belong to a mid_level stage.
-- # Class: Job_related_jobs
--     * Slot: id
--     * Slot: Job_id Description: Autocreated FK slot
--     * Slot: related_jobs_id_id Description: Lateral (non-hierarchical) relationships between jobs.
-- # Class: InvestmentLane_product_outcomes
--     * Slot: id
--     * Slot: InvestmentLane_id Description: Autocreated FK slot
--     * Slot: product_outcomes_id_id
-- # Class: ProductOutcome_informed_by_outcomes
--     * Slot: id
--     * Slot: ProductOutcome_id Description: Autocreated FK slot
--     * Slot: informed_by_outcomes_id_id Description: Kalbach desired outcomes this product outcome is designed to improve.
-- # Class: Requirement_realizes_product_outcomes
--     * Slot: id
--     * Slot: Requirement_id Description: Autocreated FK slot
--     * Slot: realizes_product_outcomes_id_id Description: Product outcomes this requirement helps realize.
-- # Class: Requirement_satisfied_by_capabilities
--     * Slot: id
--     * Slot: Requirement_id Description: Autocreated FK slot
--     * Slot: satisfied_by_capabilities_id_id
-- # Class: Requirement_acceptance_criteria
--     * Slot: id
--     * Slot: Requirement_id Description: Autocreated FK slot
--     * Slot: acceptance_criteria
-- # Class: Capability_satisfies_requirements
--     * Slot: id
--     * Slot: Capability_id Description: Autocreated FK slot
--     * Slot: satisfies_requirements_id_id Description: Requirements this capability satisfies.
-- # Class: Capability_supports_jobs
--     * Slot: id
--     * Slot: Capability_id Description: Autocreated FK slot
--     * Slot: supports_jobs_id_id Description: Jobs (any level) this capability supports.
-- # Class: Capability_supports_desired_outcomes
--     * Slot: id
--     * Slot: Capability_id Description: Autocreated FK slot
--     * Slot: supports_desired_outcomes_id_id Description: Desired outcomes this capability supports.

CREATE TABLE "Job" (
	job_level VARCHAR(9) NOT NULL,
	phase VARCHAR(14),
	last_reviewed DATE,
	sequence_order INTEGER,
	iterative BOOLEAN,
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	parent_job_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_job_id) REFERENCES "Job" (id)
);
CREATE INDEX "ix_Job_id" ON "Job" (id);

CREATE TABLE "InvestmentLane" (
	horizon VARCHAR(7),
	strategic_weight FLOAT,
	owner TEXT,
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_InvestmentLane_id" ON "InvestmentLane" (id);

CREATE TABLE "Requirement" (
	requirement_type VARCHAR(14) NOT NULL,
	priority VARCHAR(6),
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Requirement_id" ON "Requirement" (id);

CREATE TABLE "Capability" (
	capability_type VARCHAR(10),
	implementation_status VARCHAR(11),
	owner TEXT,
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_Capability_id" ON "Capability" (id);

CREATE TABLE "DesiredOutcome" (
	statement TEXT NOT NULL,
	direction VARCHAR(8) NOT NULL,
	unit_of_measure TEXT NOT NULL,
	qualifier TEXT,
	importance INTEGER,
	satisfaction INTEGER,
	opportunity_score FLOAT,
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	related_job_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(related_job_id) REFERENCES "Job" (id)
);
CREATE INDEX "ix_DesiredOutcome_id" ON "DesiredOutcome" (id);

CREATE TABLE "ProductOutcome" (
	target_metric TEXT,
	target_value TEXT,
	current_value TEXT,
	target_date DATE,
	id TEXT NOT NULL,
	pref_label TEXT,
	description TEXT,
	status VARCHAR(10) NOT NULL,
	version TEXT,
	lane_id TEXT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(lane_id) REFERENCES "InvestmentLane" (id)
);
CREATE INDEX "ix_ProductOutcome_id" ON "ProductOutcome" (id);

CREATE TABLE "Job_sali_tags" (
	id INTEGER NOT NULL,
	"Job_id" TEXT,
	sali_tags TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Job_id") REFERENCES "Job" (id)
);
CREATE INDEX "ix_Job_sali_tags_id" ON "Job_sali_tags" (id);

CREATE TABLE "Job_child_jobs" (
	id INTEGER NOT NULL,
	"Job_id" TEXT,
	child_jobs_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Job_id") REFERENCES "Job" (id),
	FOREIGN KEY(child_jobs_id_id) REFERENCES "Job" (id)
);
CREATE INDEX "ix_Job_child_jobs_id" ON "Job_child_jobs" (id);

CREATE TABLE "Job_related_jobs" (
	id INTEGER NOT NULL,
	"Job_id" TEXT,
	related_jobs_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Job_id") REFERENCES "Job" (id),
	FOREIGN KEY(related_jobs_id_id) REFERENCES "Job" (id)
);
CREATE INDEX "ix_Job_related_jobs_id" ON "Job_related_jobs" (id);

CREATE TABLE "Requirement_satisfied_by_capabilities" (
	id INTEGER NOT NULL,
	"Requirement_id" TEXT,
	satisfied_by_capabilities_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Requirement_id") REFERENCES "Requirement" (id),
	FOREIGN KEY(satisfied_by_capabilities_id_id) REFERENCES "Capability" (id)
);
CREATE INDEX "ix_Requirement_satisfied_by_capabilities_id" ON "Requirement_satisfied_by_capabilities" (id);

CREATE TABLE "Requirement_acceptance_criteria" (
	id INTEGER NOT NULL,
	"Requirement_id" TEXT,
	acceptance_criteria TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Requirement_id") REFERENCES "Requirement" (id)
);
CREATE INDEX "ix_Requirement_acceptance_criteria_id" ON "Requirement_acceptance_criteria" (id);

CREATE TABLE "Capability_satisfies_requirements" (
	id INTEGER NOT NULL,
	"Capability_id" TEXT,
	satisfies_requirements_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Capability_id") REFERENCES "Capability" (id),
	FOREIGN KEY(satisfies_requirements_id_id) REFERENCES "Requirement" (id)
);
CREATE INDEX "ix_Capability_satisfies_requirements_id" ON "Capability_satisfies_requirements" (id);

CREATE TABLE "Capability_supports_jobs" (
	id INTEGER NOT NULL,
	"Capability_id" TEXT,
	supports_jobs_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Capability_id") REFERENCES "Capability" (id),
	FOREIGN KEY(supports_jobs_id_id) REFERENCES "Job" (id)
);
CREATE INDEX "ix_Capability_supports_jobs_id" ON "Capability_supports_jobs" (id);

CREATE TABLE "Job_desired_outcomes" (
	id INTEGER NOT NULL,
	"Job_id" TEXT,
	desired_outcomes_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Job_id") REFERENCES "Job" (id),
	FOREIGN KEY(desired_outcomes_id_id) REFERENCES "DesiredOutcome" (id)
);
CREATE INDEX "ix_Job_desired_outcomes_id" ON "Job_desired_outcomes" (id);

CREATE TABLE "InvestmentLane_product_outcomes" (
	id INTEGER NOT NULL,
	"InvestmentLane_id" TEXT,
	product_outcomes_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("InvestmentLane_id") REFERENCES "InvestmentLane" (id),
	FOREIGN KEY(product_outcomes_id_id) REFERENCES "ProductOutcome" (id)
);
CREATE INDEX "ix_InvestmentLane_product_outcomes_id" ON "InvestmentLane_product_outcomes" (id);

CREATE TABLE "ProductOutcome_informed_by_outcomes" (
	id INTEGER NOT NULL,
	"ProductOutcome_id" TEXT,
	informed_by_outcomes_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("ProductOutcome_id") REFERENCES "ProductOutcome" (id),
	FOREIGN KEY(informed_by_outcomes_id_id) REFERENCES "DesiredOutcome" (id)
);
CREATE INDEX "ix_ProductOutcome_informed_by_outcomes_id" ON "ProductOutcome_informed_by_outcomes" (id);

CREATE TABLE "Requirement_realizes_product_outcomes" (
	id INTEGER NOT NULL,
	"Requirement_id" TEXT,
	realizes_product_outcomes_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Requirement_id") REFERENCES "Requirement" (id),
	FOREIGN KEY(realizes_product_outcomes_id_id) REFERENCES "ProductOutcome" (id)
);
CREATE INDEX "ix_Requirement_realizes_product_outcomes_id" ON "Requirement_realizes_product_outcomes" (id);

CREATE TABLE "Capability_supports_desired_outcomes" (
	id INTEGER NOT NULL,
	"Capability_id" TEXT,
	supports_desired_outcomes_id_id TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("Capability_id") REFERENCES "Capability" (id),
	FOREIGN KEY(supports_desired_outcomes_id_id) REFERENCES "DesiredOutcome" (id)
);
CREATE INDEX "ix_Capability_supports_desired_outcomes_id" ON "Capability_supports_desired_outcomes" (id);
