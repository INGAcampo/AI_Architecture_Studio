from pathlib import Path
import pytest
from aias_design_system import audit_python_ui,design_tokens,render_qss,validate_tokens

ROOT=Path(__file__).resolve().parents[1]

def test_tokens_are_complete_semantic_and_accessibility_governed():
 tokens=design_tokens();assert validate_tokens(tokens)==[];assert tokens["status"]=="FOUNDATION_CANDIDATE_FOR_RENDERED_REVIEW";assert tokens["accessibility"]["minimum_contrast_normal"]>=4.5;assert tokens["iconography"]["random_external_icons_prohibited"] is True

def test_qss_is_generated_for_dark_and_light_without_legacy_palette_literals():
 dark=render_qss("dark");light=render_qss("light");assert "AIAS Design System 0.1.0" in dark;assert '#0B111A' in dark and '#F3F6FA' in light;assert 'role="primary"' in dark;assert 'font-family: "Segoe UI"' in dark;assert dark!=light

def test_unsupported_theme_fails_closed():
 with pytest.raises(ValueError,match="unsupported_theme"):render_qss("neon")

def test_current_gui_audit_truthfully_identifies_migration_work():
 result=audit_python_ui(ROOT/"src/gui");assert result["files_scanned"]>0;assert result["migration_required"] is True;assert "main_window.py" in result["inline_stylesheet_files"]
