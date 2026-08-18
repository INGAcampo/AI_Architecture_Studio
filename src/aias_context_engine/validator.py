"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "schema_version", "engine_version", "generated_at", "project_root", "identity",
    "constitution", "current_state", "roadmap", "components", "installed_packages",
    "permanent_rules", "decisions", "capabilities", "integrity",
}


class ContextValidator:
    """Execute the public ContextValidator operation for the AIAS continuity and context system using explicit caller inputs."""
    def validate(self, context: dict[str, Any]) -> dict[str, Any]:
        """Validate validate for the AIAS continuity and context system and report explicit issues."""
        errors: list[str] = []
        missing = sorted(REQUIRED_KEYS - set(context))
        if missing:
            errors.append(f"missing keys: {', '.join(missing)}")
        if context.get("schema_version") != "1.0.0":
            errors.append("unsupported schema_version")
        if not context.get("identity", {}).get("project_id") == "AIAS":
            errors.append("identity.project_id must be AIAS")
        if len(context.get("permanent_rules", [])) < 5:
            errors.append("permanent_rules is incomplete")
        expected = context.get("integrity", {}).get("canonical_payload_sha256")
        payload = dict(context)
        payload["integrity"] = {}
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        actual = hashlib.sha256(canonical).hexdigest()
        if expected != actual:
            errors.append("integrity checksum mismatch")
        return {"valid": not errors, "errors": errors, "component_count": len(context.get("components", [])), "package_count": len(context.get("installed_packages", []))}

    def validate_file(self, path: Path) -> dict[str, Any]:
        """Validate file for the AIAS continuity and context system and report explicit issues."""
        return self.validate(json.loads(path.read_text(encoding="utf-8")))
