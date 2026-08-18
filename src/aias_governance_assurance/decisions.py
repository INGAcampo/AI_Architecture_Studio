"""Canonical recovered decisions from the final historical-chat segment."""
from __future__ import annotations

DECISIONS=(
 ("HIST-001","1700-1740","BINDING","Specification is the official source of truth; no module starts from code.","engineering/aeps/05_SDD/ASDD-000002-formal-sdd.yaml"),
 ("HIST-002","1725","BINDING","Trace Constitution to SDD, architecture, specification, code, tests and benchmarks.","src/aias_aeps_governance_sdd/traceability.py"),
 ("HIST-003","1730","BINDING","Admit changes only with measurable productivity, quality or maintainability benefit.","src/aias_aeps_governance_sdd/kpi.py"),
 ("HIST-004","1760","BINDING","Target Level 5 and at least 45 percent sustainable manual-effort reduction without quality loss.","engineering/aeps/metrics/KPI-000004-time-reduction.md"),
 ("HIST-005","1780","BINDING","Knowledge is structured, traceable, versioned, reusable and verifiable.","engineering/aeps/03_ONTOLOGY"),
 ("HIST-006","1820","BINDING","Reusable cross-program capability belongs to the development platform first.","engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml"),
 ("HIST-007","1840","BINDING","Version knowledge and assign exactly one official lifecycle state.","src/aias_governance_assurance/assets.py"),
 ("HIST-008","1860","BINDING","Engineering assets use stable identifiers and growth is measured as assets, not lines of code.","src/aias_governance_assurance/assets.py"),
 ("HIST-009","1870-1880","BINDING","Generators and validators produce structure, code, tests and documentation.","src/aias_aeps_governance_sdd/generators.py"),
 ("HIST-010","1920-1940","BINDING","All modules are designed, specified, generated, validated, documented and certified inside AEPS.","src/aias_governance_assurance/sdd.py"),
 ("HIST-011","1970","BINDING","AEC-000024 anti-bureaucracy: simplify or remove governance without measurable benefit.","engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml"),
 ("HIST-012","1980","BINDING","Automate documentation, QA, releases, traceability, generation and certification.","src/aias_governance_assurance/orchestrator.py"),
 ("HIST-013","2000","BINDING","Maintain intelligent backups and total recoverability.","src/aias_context_engine/storage.py"),
 ("HIST-014","2060","BINDING","AEC-000049 materializes safe value at the earliest maturity level.","engineering/aeps/02_CONSTITUTION/AEC-000002-executable-constitution.yaml"),
 ("HIST-015","2290-2300","BINDING","Build more, discuss enough; every conversation produces a tangible asset.","ACKC/EXECUTIVE_ORDERS.md"),
 ("HIST-016","2310","BINDING","New rules apply immediately; existing validated components align through controlled plans.","src/aias_governance_assurance/orchestrator.py"),
 ("HIST-017","2320-2330","BINDING","Every delivery increases reusable, verifiable and traceable technological capital.","src/aias_governance_assurance/orchestrator.py"),
 ("HIST-018","2340","BINDING","Maintain an AIAS Master Development Plan with programs, assets, rules, priorities, dependencies, metrics and state.","engineering/aias/master/AIAS_MASTER_DEVELOPMENT_PLAN.json"),
 ("HIST-019","2350-2370","BINDING","Every implementation block includes code, tests, CLI, documentation, installer and integrated release evidence.","src/aias_governance_assurance/dod.py"),
 ("HIST-020","2390-2410","BINDING","Knowledge units record origin, license, version, date, traceability and human-review need.","src/aias_aeks"),
 ("HIST-021","2470-2500","BINDING","Engineering capabilities are primary; infrastructure exists only to enable them; progress is capability-based.","ACKC/EXECUTIVE_ORDERS.md"),
 ("HIST-022","2500","BINDING","Definition of Done is executable and completion cannot be declared early.","src/aias_governance_assurance/dod.py"),
 ("HIST-023","2530","BINDING","Macrodeliveries include reference cases, receipt, manifest, release ZIP and validation evidence.","src/aias_governance_assurance/dod.py"),
 ("HIST-024","1920-2490","ROADMAP","Knowledge Graph, intelligence core, autonomous cloud, operating system and full-project production remain staged programs.","ACKC/MASTER_CONTEXT.json"),
 ("HIST-025","2380","ROADMAP","Knowledge, calculation, drawing, technical-file and engineering-agent programs are sequenced capabilities.","ACKC/MASTER_CONTEXT.json"),
)

def registry():
 """Return recovered decisions as serialization-ready records."""
 return [{"decision_id":i,"captures":c,"classification":k,"decision":d,"evidence":e} for i,c,k,d,e in DECISIONS]
