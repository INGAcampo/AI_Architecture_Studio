from pathlib import Path

from core.standards.standard_manager import StandardManager
from core.standards.standard_registry import StandardRegistry
from core.standards.standard_validator import StandardValidator


def test_builtin_standard_profiles_are_available():
    profiles = StandardRegistry.built_in_profiles()
    assert "venezuela" in profiles
    assert profiles["venezuela"].name


def test_standard_manager_persists_selected_profile(tmp_path):
    path = tmp_path / "standard_settings.json"
    manager = StandardManager(config_path=path)
    assert manager.set_profile_by_id("venezuela") is True
    assert path.exists()

    restored = StandardManager(config_path=path)
    assert restored.active_profile.name == manager.active_profile.name


def test_active_profile_validation_has_stable_shape(tmp_path):
    manager = StandardManager(config_path=tmp_path / "standards.json")
    result = StandardValidator.validate(manager.active_profile)

    assert set(result) == {"valid", "warnings", "errors"}
    assert isinstance(result["warnings"], list)
    assert isinstance(result["errors"], list)


def test_main_window_standard_command_modules_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "src/commands/core/standards_command.py").exists()
    assert (root / "src/commands/core/standards_report_command.py").exists()
    assert (root / "src/commands/core/__init__.py").exists()
