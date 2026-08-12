import pytest
from platform_sdk.documents import *
@pytest.mark.parametrize("i",range(120))
def test_documents(i):
    m=DocumentManager(); d=m.create(PlatformDocument(f"D{i}","Model",DocumentKind.MODEL))
    m.mark_changed(d.document_id); assert d.revision==1 and d.dirty
    m.mark_saved(d.document_id); assert not d.dirty
