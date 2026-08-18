import pytest
from datetime import date
from documentation_kernel.titleblock_revision import *

@pytest.mark.parametrize("i", range(120))
def test_revision(i):
    manager = TitleBlockRevisionManager()
    block = TitleBlock(f"TB{i}", "Project", "A-101", "Floor Plan")
    block = manager.add_revision(block, Revision("R1", "Issued", date(2026, 1, 1), "A"))
    block = manager.add_revision(block, Revision("R2", "Updated", date(2026, 2, 1), "B"))
    assert manager.latest_revision(block).revision_id == "R2"
    assert len(block.revisions) == 2
