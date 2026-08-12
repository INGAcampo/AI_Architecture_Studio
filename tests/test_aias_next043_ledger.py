from aias_next043_ledger import ExecutionLedger
def test_ledger_appends(tmp_path): assert ExecutionLedger(tmp_path/'x').append('M','VALIDATED')['status']=='VALIDATED'
