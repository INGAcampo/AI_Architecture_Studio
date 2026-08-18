from aias_next054_continuation import ContinuationPackage
def test_package_incomplete(tmp_path):assert ContinuationPackage(tmp_path/'x').build()['status']=='INCOMPLETE'
