from aias_next046_sync import DashboardSync
def test_sync_holds_missing(tmp_path): assert DashboardSync(tmp_path/'p',tmp_path/'d').run()['status']=='HOLD'
