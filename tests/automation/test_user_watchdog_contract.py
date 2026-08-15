from pathlib import Path
def test_user_watchdog_has_idle_and_bounded_restart_contract():
    text=Path('tools/automation/Start-AIASUserWatchdog.ps1').read_text(encoding='utf-8')
    assert 'TARGET_REACHED' in text and 'HUMAN_INPUT_REQUIRED' in text and '$restarts -ge 3' in text
