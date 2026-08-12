import pytest
from platform_sdk.context import PlatformContext
from design.steel.vertical_slice import SteelBeamVerticalSlice
@pytest.mark.parametrize('i',range(120))
def test_slice(i):
 r=SteelBeamVerticalSlice(PlatformContext.create_default()).run(f'B{i}','W14X38','ASTM_A992',6,2,50e3,30e3,60e3);assert r.design_result.unity_ratio>=0 and '# Steel Beam Design' in r.report.markdown
