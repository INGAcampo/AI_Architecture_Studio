import pytest
from design.steel.column_reports import SteelColumnReportEngine
from design.steel.column_domain import *
from design.steel.catalog import seed_default_catalog
from design.steel.repositories import SteelProfileRepository,SteelMaterialRepository
from design.steel.column_design_engine import SteelColumnDesignEngine

@pytest.mark.parametrize("i", range(120))
def test_column_report(i):
    pr=SteelProfileRepository();mr=SteelMaterialRepository();seed_default_catalog(pr,mr)
    c=SteelColumn(f"C{i}","W14X38","ASTM_A992",3.5,ColumnEndCondition.PINNED_PINNED,ColumnEndCondition.PINNED_PINNED,SteelColumnDemand(300e3))
    r=SteelColumnDesignEngine().design(c,pr.get("W14X38"),mr.get("ASTM_A992"))
    report=SteelColumnReportEngine().build(c,pr.get("W14X38"),mr.get("ASTM_A992"),r)
    assert f"Steel Column Design — C{i}" in report.markdown
