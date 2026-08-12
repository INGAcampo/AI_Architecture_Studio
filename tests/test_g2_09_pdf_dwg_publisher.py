import pytest
from documentation_kernel.professional_publisher import *

@pytest.mark.parametrize("i", range(120))
def test_publish(i):
    job = PublishJob(f"J{i}", ("A-101", "A-201"), PublishFormat.PDF, "out")
    manifest = ProfessionalPublisher().publish(job)
    assert manifest.success
    assert manifest.files == ("out/A-101.pdf", "out/A-201.pdf")
