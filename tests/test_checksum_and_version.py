from src.storage.checksum import calculate_checksum,verify_checksum
from src.storage.file_version import FileVersion
def test_checksum_is_stable():
    c=calculate_checksum({'b':2,'a':1}); assert c==calculate_checksum({'a':1,'b':2}) and verify_checksum({'a':1,'b':2},c)
def test_version_compatibility():
    s=FileVersion.parse('1.2.0'); assert FileVersion.parse('1.0.0').is_compatible_with(s) and not FileVersion.parse('2.0.0').is_compatible_with(s)
