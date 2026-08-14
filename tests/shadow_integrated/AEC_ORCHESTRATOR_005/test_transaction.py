from aec_orchestrator_transaction.plan import TransactionPlan,TransactionStep,TransactionState
from aec_orchestrator_transaction.engine import TransactionEngine


def test_reversible_transaction_commits():
    calls=[]
    plan=TransactionPlan(
        "T1",
        (
            TransactionStep("S1","prepare",True),
            TransactionStep("S2","apply",True),
        ),
    )
    result=TransactionEngine().execute(
        plan,
        {
            "prepare":lambda:calls.append("prepare"),
            "apply":lambda:calls.append("apply"),
        },
    )

    assert result.state==TransactionState.COMMITTED
    assert result.completed_steps==("S1","S2")
    assert calls==["prepare","apply"]


def test_nonreversible_step_is_rejected_fail_closed():
    plan=TransactionPlan(
        "T2",
        (
            TransactionStep("S1","publish",False),
        ),
        require_all_reversible=True,
    )

    result=TransactionEngine().execute(plan,{"publish":lambda:None})
    assert result.state==TransactionState.FAILED
    assert result.completed_steps==()


def test_failure_after_completed_step_reports_rollback_state():
    def boom():
        raise RuntimeError("fail")

    plan=TransactionPlan(
        "T3",
        (
            TransactionStep("S1","prepare",True),
            TransactionStep("S2","apply",True),
        ),
    )

    result=TransactionEngine().execute(
        plan,
        {
            "prepare":lambda:None,
            "apply":boom,
        },
    )

    assert result.state==TransactionState.ROLLED_BACK
    assert result.completed_steps==("S1",)
