from __future__ import annotations

import json
from pathlib import Path

import pytest

from aias_l3_production_bim.external_interop import (
    ExternalInteropInvocationError,
    NativeExternalInteropBridge,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "AIAS_L3_PRODUCTION_BIM_004D_CURRENT" / "INVOCATION_CONTRACTS.json"


def bridge():
    assert CONTRACTS.exists()
    return NativeExternalInteropBridge(CONTRACTS)


def test_004e_uses_004d_evidence():
    b = bridge()
    data = json.loads(CONTRACTS.read_text(encoding="utf-8-sig"))
    assert b.invocation_ready_domains == tuple(data["invocation_ready_domains"])
    assert b.adapter_required_domains == tuple(data["adapter_required_domains"])
    assert b.unavailable_domains == tuple(data["unavailable_domains"])


def test_004e_all_ready_domains_have_authorities_and_methods():
    b = bridge()
    assert b.invocation_ready_domains
    for domain in b.invocation_ready_domains:
        contracts = b.authority_contracts(domain)
        assert contracts
        assert b.allowed_methods(domain)
        authority = b.resolve_authority(domain)
        assert authority is not None


def test_004e_sap2000_contract_if_ready():
    b = bridge()
    if "sap2000" not in b.invocation_ready_domains:
        pytest.skip("SAP2000 is not INVOCATION_READY in current 004D evidence")
    contracts = b.authority_contracts("sap2000")
    assert any(c.symbol == "SAP2000Bridge" for c in contracts)
    assert "export_model" in b.allowed_methods("sap2000")
    instance = b.create_authority("sap2000")
    assert callable(getattr(instance, "export_model"))


def test_004e_rejects_non_ready_domain():
    b = bridge()
    candidates = (
        list(b.adapter_required_domains)
        + list(b.blocked_domains)
        + list(b.unresolved_domains)
        + list(b.unavailable_domains)
    )
    if not candidates:
        pytest.skip("No non-ready domain exists in current evidence")
    domain = candidates[0]
    with pytest.raises(ExternalInteropInvocationError):
        b.resolve_authority(domain)


def test_004e_rejects_uncertified_method():
    b = bridge()
    domain = b.invocation_ready_domains[0]
    with pytest.raises(ExternalInteropInvocationError):
        b.invoke(domain, "__uncertified_method__")


def test_004e_snapshot_is_serializable():
    b = bridge()
    json.dumps(b.snapshot())
