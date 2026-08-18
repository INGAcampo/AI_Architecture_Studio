"""AEKS reference ingestion, graph validation and checksum release orchestration."""
from __future__ import annotations
from pathlib import Path
import json, hashlib, zipfile
from .importers import JSONKnowledgeImporter
from .repository import KnowledgeRepository
from .registry import StandardsRegistry
from .graph import KnowledgeGraphBuilder
from .traceability import KnowledgeTraceabilityEngine
from .exporters import KnowledgeExporter

class AEKSOrchestrator:
    """Execute the knowledge lifecycle and package searchable traceable evidence."""
    def import_unit(self, source: Path, workspace: Path) -> dict:
        """Validate, persist, index, export and package an imported knowledge unit."""
        unit = JSONKnowledgeImporter().load(source)
        repo = KnowledgeRepository(workspace / "repository")
        saved = repo.save(unit)

        registry = StandardsRegistry(workspace / "registry" / "standards_registry.json")
        registry.register(unit, saved)
        registry.save()

        graph = KnowledgeGraphBuilder().build([unit])
        graph_path = workspace / "graph" / "knowledge_graph.json"
        graph_path.parent.mkdir(parents=True, exist_ok=True)
        graph_path.write_text(json.dumps(sorted(graph.triples), indent=2), encoding="utf-8")

        trace_path = workspace / "traceability" / f"{unit.eku_id}.json"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        trace_path.write_text(json.dumps(KnowledgeTraceabilityEngine().matrix(unit), indent=2), encoding="utf-8")

        md_path = KnowledgeExporter().to_markdown(unit, workspace / "docs" / f"{unit.eku_id}.md")

        release = workspace / "release"
        release.mkdir(parents=True, exist_ok=True)
        archive = release / f"{unit.eku_id}_{unit.version}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for path in workspace.rglob("*"):
                if path.is_file() and release not in path.parents:
                    z.write(path, path.relative_to(workspace))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()

        return {
            "eku_id": unit.eku_id,
            "stored": str(saved),
            "registry": str(registry.path),
            "graph": str(graph_path),
            "traceability": str(trace_path),
            "documentation": str(md_path),
            "archive": str(archive),
            "sha256": digest,
            "validated": True,
            "human_review_required": unit.human_review_required,
        }
