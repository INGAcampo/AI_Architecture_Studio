"""Evidence-gated external interoperability bridge for AIAS L3 004E."""
from __future__ import annotations

import importlib
import inspect
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExternalAuthorityContract:
    """Represent ExternalAuthorityContract within the AIAS production BIM interoperability layer."""
    domain: str
    module: str
    symbol: str
    kind: str | None
    constructor_signature: str | None
    methods: tuple[str, ...]


class ExternalInteropInvocationError(RuntimeError):
    """Raised when an external interoperability invocation is not allowed."""


class NativeExternalInteropBridge:
    """Invoke only authorities explicitly certified INVOCATION_READY by 004D."""

    def __init__(self, contracts_path: str | Path) -> None:
        self._contracts_path = Path(contracts_path)
        data = json.loads(self._contracts_path.read_text(encoding="utf-8-sig"))
        self._ready = tuple(data.get("invocation_ready_domains", ()))
        self._adapter_required = tuple(data.get("adapter_required_domains", ()))
        self._blocked = tuple(data.get("blocked_domains", ()))
        self._unresolved = tuple(data.get("unresolved_domains", ()))
        self._unavailable = tuple(data.get("unavailable_domains", ()))
        self._audited = dict(data.get("audited_domains", {}))

    @property
    def invocation_ready_domains(self) -> tuple[str, ...]:
        """Execute the invocation ready domains operation for this interoperability component."""
        return self._ready

    @property
    def adapter_required_domains(self) -> tuple[str, ...]:
        """Execute the adapter required domains operation for this interoperability component."""
        return self._adapter_required

    @property
    def blocked_domains(self) -> tuple[str, ...]:
        """Execute the blocked domains operation for this interoperability component."""
        return self._blocked

    @property
    def unresolved_domains(self) -> tuple[str, ...]:
        """Execute the unresolved domains operation for this interoperability component."""
        return self._unresolved

    @property
    def unavailable_domains(self) -> tuple[str, ...]:
        """Execute the unavailable domains operation for this interoperability component."""
        return self._unavailable

    def is_invocation_ready(self, domain: str) -> bool:
        """Execute the is invocation ready operation for this interoperability component."""
        return domain in self._ready

    def authority_contracts(self, domain: str) -> tuple[ExternalAuthorityContract, ...]:
        """Execute the authority contracts operation for this interoperability component."""
        item = self._audited.get(domain)
        if not item:
            return ()
        out: list[ExternalAuthorityContract] = []
        for authority in item.get("authorities", ()):
            out.append(
                ExternalAuthorityContract(
                    domain=domain,
                    module=authority["module"],
                    symbol=authority["symbol"],
                    kind=authority.get("kind"),
                    constructor_signature=authority.get("constructor_signature"),
                    methods=tuple(
                        method["name"]
                        for method in authority.get("methods", ())
                    ),
                )
            )
        return tuple(out)

    def allowed_methods(self, domain: str) -> tuple[str, ...]:
        """Execute the allowed methods operation for this interoperability component."""
        methods: list[str] = []
        for contract in self.authority_contracts(domain):
            for method in contract.methods:
                if method not in methods:
                    methods.append(method)
        return tuple(methods)

    def resolve_authority(self, domain: str, authority_index: int = 0) -> Any:
        """Execute the resolve authority operation for this interoperability component."""
        if domain not in self._ready:
            raise ExternalInteropInvocationError(
                f"Domain {domain!r} is not INVOCATION_READY."
            )
        contracts = self.authority_contracts(domain)
        if not contracts:
            raise ExternalInteropInvocationError(
                f"No certified authority contract for domain {domain!r}."
            )
        try:
            contract = contracts[authority_index]
        except IndexError as exc:
            raise ExternalInteropInvocationError(
                f"Authority index {authority_index} is invalid for {domain!r}."
            ) from exc

        module = importlib.import_module(contract.module)
        return getattr(module, contract.symbol)

    def create_authority(self, domain: str, authority_index: int = 0) -> Any:
        """Execute the create authority operation for this interoperability component."""
        authority = self.resolve_authority(domain, authority_index)
        if inspect.isclass(authority):
            sig = inspect.signature(authority)
            required = [
                p
                for p in sig.parameters.values()
                if p.name not in ("self", "cls")
                and p.default is inspect._empty
                and p.kind not in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                )
            ]
            if required:
                raise ExternalInteropInvocationError(
                    f"Certified authority for {domain!r} unexpectedly requires "
                    f"constructor dependencies: {[p.name for p in required]}"
                )
            return authority()
        return authority

    def invoke(
        self,
        domain: str,
        method: str,
        *args: Any,
        authority_index: int = 0,
        **kwargs: Any,
    ) -> Any:
        """Execute the invoke operation for this interoperability component."""
        if method not in self.allowed_methods(domain):
            raise ExternalInteropInvocationError(
                f"Method {method!r} is not certified for domain {domain!r}."
            )
        target = self.create_authority(domain, authority_index)
        callable_obj = getattr(target, method, None)
        if not callable(callable_obj):
            raise ExternalInteropInvocationError(
                f"Certified method {method!r} is not callable for {domain!r}."
            )
        return callable_obj(*args, **kwargs)

    def snapshot(self) -> dict[str, Any]:
        """Execute the snapshot operation for this interoperability component."""
        return {
            "invocation_ready_domains": list(self._ready),
            "adapter_required_domains": list(self._adapter_required),
            "blocked_domains": list(self._blocked),
            "unresolved_domains": list(self._unresolved),
            "unavailable_domains": list(self._unavailable),
            "authorities": {
                domain: [
                    {
                        "module": c.module,
                        "symbol": c.symbol,
                        "methods": list(c.methods),
                    }
                    for c in self.authority_contracts(domain)
                ]
                for domain in self._ready
            },
        }
