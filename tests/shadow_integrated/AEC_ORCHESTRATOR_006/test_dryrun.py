from aec_orchestrator_dryrun.dryrun import DryRunStep,evaluate_dry_run


def test_read_only_dry_run_is_accepted():
    report=evaluate_dry_run(
        (
            DryRunStep("S1","query",False,True),
            DryRunStep("S2","inspect",False,True),
        )
    )
    assert report.accepted is True
    assert report.blocked_steps==()


def test_external_write_is_blocked_by_default():
    report=evaluate_dry_run(
        (
            DryRunStep("S1","save",True,True),
        )
    )
    assert report.accepted is False
    assert report.blocked_steps==("S1",)


def test_explicit_external_write_flag_changes_only_dryrun_decision():
    report=evaluate_dry_run(
        (
            DryRunStep("S1","save",True,True),
        ),
        allow_external_writes=True,
    )
    assert report.accepted is True
    assert report.reversible_steps==("S1",)
