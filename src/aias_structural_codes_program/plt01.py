"""PLT-01 governed optimization, document automation and distributed execution."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json,math

@dataclass(frozen=True,slots=True)
class OptimizationCandidate:
    candidate_id:str;objectives:tuple[tuple[str,float],...];constraints:tuple[tuple[str,float],...];evidence_sha256:str
@dataclass(frozen=True,slots=True)
class OptimizationPolicy:
    policy_id:str;objective_weights:tuple[tuple[str,float],...];constraint_maxima:tuple[tuple[str,float],...];human_approval_required:bool=True
@dataclass(frozen=True,slots=True)
class OptimizationDecision:
    selected_id:str;ranked_ids:tuple[str,...];rejected:tuple[tuple[str,str],...];status:str;human_approval_required:bool=True;global_optimum_claimed:bool=False
class GovernedOptimizer:
    def select(self,candidates:tuple[OptimizationCandidate,...],policy:OptimizationPolicy)->OptimizationDecision:
        if not policy.policy_id or not policy.objective_weights or not policy.constraint_maxima:raise ValueError("optimization_policy_incomplete")
        weights=dict(policy.objective_weights);limits=dict(policy.constraint_maxima);ranked=[];rejected=[];ids=[]
        for row in candidates:
            ids.append(row.candidate_id);objectives=dict(row.objectives);constraints=dict(row.constraints)
            if not row.candidate_id or len(row.evidence_sha256)!=64 or any(not math.isfinite(x) for x in (*objectives.values(),*constraints.values())):rejected.append((row.candidate_id,"invalid_candidate"));continue
            missing=set(weights)-set(objectives)
            violations=[key for key,limit in limits.items() if key not in constraints or constraints[key]>limit]
            if missing or violations:rejected.append((row.candidate_id,"missing_objective" if missing else f"constraint_violation:{sorted(violations)}"));continue
            ranked.append((sum(objectives[key]*weight for key,weight in weights.items()),row.candidate_id))
        if len(ids)!=len(set(ids)):raise ValueError("duplicate_candidate_id")
        ranked.sort();ordered=tuple(x[1] for x in ranked)
        return OptimizationDecision(ordered[0] if ordered else "",ordered,tuple(rejected),"PROPOSED_FOR_HUMAN_APPROVAL" if ordered else "NO_FEASIBLE_CANDIDATE")

REQUIRED_DOCUMENTS={"MODEL","CALCULATION_REPORT","DRAWINGS","SPECIFICATIONS","REVISION_REGISTER"}
@dataclass(frozen=True,slots=True)
class DocumentEvidence:
    document_id:str;kind:str;revision:str;source_locator:str;sha256:str
@dataclass(frozen=True,slots=True)
class AutomatedDocumentPackage:
    package_id:str;documents:tuple[DocumentEvidence,...];manifest_sha256:str;status:str;issues:tuple[str,...];professional_review_required:bool=True
class DocumentAutomationEngine:
    def assemble(self,package_id:str,documents:tuple[DocumentEvidence,...])->AutomatedDocumentPackage:
        issues=[];kinds=[x.kind for x in documents];ids=[x.document_id for x in documents]
        missing=sorted(REQUIRED_DOCUMENTS-set(kinds))
        if not package_id:issues.append("document_package_id_required")
        if missing:issues.append(f"missing_documents:{missing}")
        if len(ids)!=len(set(ids)):issues.append("duplicate_document_id")
        for row in documents:
            if not all((row.document_id,row.kind,row.revision,row.source_locator)) or len(row.sha256)!=64:issues.append(f"{row.document_id}:invalid_document_evidence")
        digest=hashlib.sha256(json.dumps([asdict(x) for x in documents],sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return AutomatedDocumentPackage(package_id,documents,digest,"READY_FOR_PROFESSIONAL_REVIEW" if not issues else "BLOCKED",tuple(issues))

@dataclass(frozen=True,slots=True)
class ComputeJob:
    job_id:str;capability:str;payload_sha256:str;dependencies:tuple[str,...]=()
@dataclass(frozen=True,slots=True)
class DistributedPlan:
    plan_id:str;batches:tuple[tuple[str,...],...];status:str;issues:tuple[str,...];plan_sha256:str
class DistributedComputePlanner:
    def plan(self,plan_id:str,jobs:tuple[ComputeJob,...],allowed_capabilities:set[str])->DistributedPlan:
        issues=[];ids=[x.job_id for x in jobs]
        if not plan_id:issues.append("plan_id_required")
        if len(ids)!=len(set(ids)):issues.append("duplicate_job_id")
        known=set(ids)
        for job in jobs:
            if not job.job_id or job.capability not in allowed_capabilities or len(job.payload_sha256)!=64:issues.append(f"{job.job_id}:invalid_job")
            if set(job.dependencies)-known:issues.append(f"{job.job_id}:unknown_dependency")
        pending={x.job_id:set(x.dependencies) for x in jobs};batches=[];done=set()
        while pending:
            ready=tuple(sorted(key for key,value in pending.items() if value<=done))
            if not ready:issues.append("dependency_cycle");break
            batches.append(ready);done.update(ready)
            for key in ready:pending.pop(key)
        digest=hashlib.sha256(json.dumps([asdict(x) for x in jobs],sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return DistributedPlan(plan_id,tuple(batches),"READY" if not issues else "BLOCKED",tuple(issues),digest)
