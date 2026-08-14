from dataclasses import replace

from standards_engine_ext.provenance import (
    RulePack,
    RulePackProvenance,
    compute_rule_pack_sha256,
    verify_rule_pack,
)
from standards_engine_ext.registry import RulePackRegistry


def make_pack():
    provisional=RulePack(
        pack_id="DEMO",
        version="1.0",
        provenance=RulePackProvenance(
            source_name="DEMO-NOT-A-CODE",
            source_version="1",
            jurisdiction="TEST",
            effective_date="2026-01-01",
        ),
        rule_ids=("R1","R2"),
        content_sha256="0"*64,
    )
    return replace(
        provisional,
        content_sha256=compute_rule_pack_sha256(provisional),
    )


def test_rule_pack_hash_and_provenance_validate():
    pack=make_pack()
    assert verify_rule_pack(pack) is True


def test_tampered_pack_fails_closed():
    pack=make_pack()
    tampered=replace(pack,rule_ids=("R1","R3"))
    assert verify_rule_pack(tampered) is False


def test_registry_rejects_duplicate_version():
    registry=RulePackRegistry()
    pack=make_pack()
    registry.register(pack)

    failed=False
    try:
        registry.register(pack)
    except ValueError:
        failed=True

    assert failed is True


def test_registry_returns_exact_version():
    registry=RulePackRegistry()
    pack=make_pack()
    registry.register(pack)
    assert registry.get("DEMO","1.0")==pack
    assert registry.count==1
