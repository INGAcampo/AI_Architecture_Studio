from aias_next047_validation import ContinuityValidation
def test_validation_holds_missing(tmp_path): assert ContinuityValidation(tmp_path).run()['status']=='HOLD'
