import pytest

from gui.workspace2 import Availability, CommandDescriptor, CommandRegistry, ProfessionalStatus, core_command_catalog


def test_search_is_ranked_multilingual_and_capability_visible():
    registry = core_command_catalog()
    assert registry.search("muro")[0].command_id == "WALL"
    assert registry.search("structural", discipline="Structure")[0].discipline == "Structure"
    assert registry.resolve("L").capability_id == "CAD-LINE"


def test_duplicate_identity_and_aliases_fail_closed():
    registry = CommandRegistry(); registry.register(CommandDescriptor("ONE", "One", ("O",), "CAD", "CAP-ONE"))
    with pytest.raises(KeyError, match="alias_conflict"):
        registry.register(CommandDescriptor("TWO", "Two", ("O",), "CAD", "CAP-TWO"))
    with pytest.raises(ValueError, match="duplicate_command_alias"):
        CommandDescriptor("BAD", "Bad", ("B", "B"), "CAD", "CAP-BAD")


def test_execution_respects_truthful_availability():
    called=[]; registry=core_command_catalog({"LINE":lambda value:called.append(value) or value})
    assert registry.execute("L", 4)==4 and called==[4]
    with pytest.raises(RuntimeError, match="reference_only"):
        registry.execute("STRUCTURAL-DESIGN")
    with pytest.raises(RuntimeError, match="unavailable"):
        registry.execute("REVIT")


def test_professional_release_requires_all_authorities():
    status=ProfessionalStatus(); assert not status.snapshot()["engineering_release_authorized"]
    status.normative_pack="COVENIN-ACQUIRED"; status.normative_status="VALIDATED"; status.review_status="APPROVED"; status.professional_reviewer="Licensed Engineer"
    assert status.snapshot()["engineering_release_authorized"]


def test_catalog_exposes_distinct_capability_states():
    states={item.availability for item in core_command_catalog().all()}
    assert states=={Availability.AVAILABLE, Availability.REFERENCE_ONLY, Availability.UNAVAILABLE}
