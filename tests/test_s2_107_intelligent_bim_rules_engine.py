from dataclasses import dataclass
import pytest

from engines.ai.rules import (
    DoorWidthRule,
    DuplicateGuidRule,
    EmptyPropertyRule,
    InvalidLevelRule,
    Issue,
    IssueSeverity,
    MissingMaterialRule,
    Rule,
    RuleContext,
    RuleEngine,
    RuleRegistry,
)


@dataclass
class Element:
    element_id: str
    kind: str = "wall"
    width: float = 1.0
    material_id: str | None = "mat-1"
    guid: str | None = None
    level_id: str | None = None
    name: str | None = "Element"


class AlwaysIssueRule(Rule):
    rule_id = "test.always"
    name = "Always Issue"

    def evaluate(self, element, context):
        return (
            Issue(
                rule_id=self.rule_id,
                rule_name=self.name,
                severity=IssueSeverity.INFO,
                element_id=element.element_id,
                message="Issue",
            ),
        )


@pytest.mark.parametrize("index", range(20))
def test_issue_model(index):
    issue = Issue(
        rule_id="r",
        rule_name="Rule",
        severity=IssueSeverity.WARNING,
        element_id=f"E{index}",
        message="Message",
    )
    data = issue.to_dict()
    assert data["element_id"] == f"E{index}"
    assert data["severity"] == "WARNING"


@pytest.mark.parametrize("index", range(20))
def test_registry(index):
    registry = RuleRegistry()
    rule = AlwaysIssueRule()
    registry.register(rule)
    assert len(registry) == 1
    assert registry.get(rule.rule_id) is rule
    assert registry.enabled() == (rule,)
    removed = registry.unregister(rule.rule_id)
    assert removed is rule


@pytest.mark.parametrize("index", range(20))
def test_door_width_rule(index):
    registry = RuleRegistry()
    registry.register(DoorWidthRule(0.80))
    engine = RuleEngine(registry)
    door = Element(f"D{index}", kind="door", width=0.70)
    issues = engine.run_element(door)
    assert len(issues) == 1
    assert issues[0].severity is IssueSeverity.ERROR


@pytest.mark.parametrize("index", range(20))
def test_material_level_and_property_rules(index):
    registry = RuleRegistry()
    registry.register(MissingMaterialRule())
    registry.register(InvalidLevelRule())
    registry.register(EmptyPropertyRule(("name",)))
    engine = RuleEngine(registry)
    element = Element(
        f"E{index}",
        material_id=None,
        level_id="L9",
        name="",
    )
    issues = engine.run_element(
        element,
        metadata={"valid_level_ids": {"L1", "L2"}},
    )
    assert len(issues) == 3
    assert {issue.rule_id for issue in issues} == {
        "bim.element.missing_material",
        "bim.element.invalid_level",
        "bim.element.empty_required_property",
    }


@pytest.mark.parametrize("index", range(20))
def test_duplicate_guid_rule(index):
    registry = RuleRegistry()
    registry.register(DuplicateGuidRule())
    engine = RuleEngine(registry)
    project = {
        "elements": [
            Element("A", guid=f"G{index}"),
            Element("B", guid=f"G{index}"),
        ]
    }
    issues = engine.run(project)
    assert len(issues) == 2
    assert all(issue.severity is IssueSeverity.CRITICAL for issue in issues)


@pytest.mark.parametrize("index", range(20))
def test_engine_statistics_and_clear(index):
    registry = RuleRegistry()
    registry.register(AlwaysIssueRule())
    engine = RuleEngine(registry)
    project = {"elements": [Element(f"E{index}")]}
    issues = engine.run(project)
    assert len(issues) == 1
    stats = engine.statistics()
    assert stats.runs == 1
    assert stats.issue_count == 1
    assert stats.by_severity["INFO"] == 1
    engine.clear()
    cleared = engine.statistics()
    assert cleared.runs == 0
    assert cleared.issue_count == 0
