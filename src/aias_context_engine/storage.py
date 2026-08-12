"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ContextStore:
    """Execute the public ContextStore operation for the AIAS continuity and context system using explicit caller inputs."""
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "snapshots").mkdir(exist_ok=True)

    def write(self, context: dict[str, Any]) -> dict[str, str]:
        """Persist write for the AIAS continuity and context system in its stable external representation."""
        master = self.root / "MASTER_CONTEXT.json"
        master.write_text(json.dumps(context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        snapshot = self.root / "snapshots" / f"MASTER_CONTEXT_{stamp}.json"
        shutil.copy2(master, snapshot)
        prompt = self.root / "CONTINUE_PROMPT.md"
        prompt.write_text(
            "# AIAS Continuity Prompt\n\n"
            "Read `MASTER_CONTEXT.json` as the current project authority. "
            "Verify it against the repository before modifying code. Preserve completed decisions, "
            "continue the active program and update ACE after every validated macro-delivery.\n",
            encoding="utf-8",
        )
        next_task = self.root / "NEXT_TASK.yaml"
        next_task.write_text(
            f"program: {context['roadmap']['current']}\nnext: {context['roadmap']['next']}\nstatus: ACTIVE\n",
            encoding="utf-8",
        )
        project_state = self.root / "PROJECT_STATE.json"
        project_state.write_text(
            json.dumps({"generated_at": context["generated_at"], "current_state": context["current_state"], "roadmap": context["roadmap"], "integrity": context["integrity"]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        human = self.root / "MASTER_CONTEXT.md"
        human.write_text(
            "# AIAS Master Context\n\n"
            f"Generated: `{context['generated_at']}`\n\n"
            f"Active program: **{context['roadmap']['current']}**\n\n"
            f"Next program: **{context['roadmap']['next']}**\n\n"
            f"Components inventoried: **{len(context['components'])}**  \n"
            f"Source packages: **{len(context['installed_packages'])}**  \n"
            f"Integrity: `{context['integrity']['canonical_payload_sha256']}`\n\n"
            "Machine-readable authority: `MASTER_CONTEXT.json`.\n",
            encoding="utf-8",
        )
        orders = self.root / "EXECUTIVE_ORDERS.md"
        orders.write_text(
            "# AIAS Executive Orders\n\n"
            "- **OE-000031:** tangible implementation has priority over conceptual expansion.\n"
            "- **OE-000050:** communicate material opportunities, risks and acceleration recommendations immediately with evidence, tradeoffs and a concrete action; suppress non-actionable noise.\n"
            "- **OE-000051:** before replacing the primary AIAS conversation, generate and validate the AEC-000051 continuity handoff package.\n"
            "- **ACE-DEC-0001:** regenerate and validate ACE after every macro-delivery.\n",
            encoding="utf-8",
        )
        university = self.root / "AIAS_UNIVERSITY_STATE.md"
        university.write_text(
            "# AIAS University State\n\nStatus: **PLANNED_STRATEGIC_SUBSYSTEM**\n\n"
            "Planned capabilities: tutorials, books, manuals, guides, courses, exams and certificates.\n",
            encoding="utf-8",
        )
        conversation = self.root / "CONVERSATION_LOG.md"
        conversation.write_text(
            "# AIAS Conversation Continuity Log\n\n"
            f"- {context['generated_at']}: ACE generated a repository-derived context snapshot.\n",
            encoding="utf-8",
        )
        return {"master": str(master), "snapshot": str(snapshot), "prompt": str(prompt), "next_task": str(next_task), "project_state": str(project_state), "human_context": str(human)}
