from __future__ import annotations
from dataclasses import dataclass
import hashlib
from pathlib import Path
@dataclass(frozen=True, slots=True)
class BaselineManifest:
    baseline_id: str
    files: tuple[tuple[str,str], ...]
    frozen: bool = False
    def digest(self) -> str:
        canonical="\n".join(f"{path}:{digest}" for path,digest in self.files).encode()
        return hashlib.sha256(canonical).hexdigest()
class ReleasePromotion:
    def build(self, root: Path, relative_paths: tuple[str, ...], *, frozen: bool = False) -> BaselineManifest:
        entries=[]
        for relative in sorted(relative_paths):
            path=root/relative
            if not path.is_file(): raise FileNotFoundError(relative)
            entries.append((relative,hashlib.sha256(path.read_bytes()).hexdigest()))
        return BaselineManifest("AIAS-BASELINE-CANDIDATE",tuple(entries),frozen)
    def promote(self, manifest: BaselineManifest, *, clean_tree: bool, external_gates_closed: bool) -> dict:
        eligible=manifest.frozen and clean_tree and external_gates_closed
        return {"promoted":eligible,"baseline_id":manifest.baseline_id,"reason":"all promotion gates passed" if eligible else "baseline freeze, clean tree and external gates are required"}
