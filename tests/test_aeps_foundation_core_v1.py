import pytest
from aias_aeps_foundation.core import *
from aias_aeps_foundation.bootstrap import bootstrap,DIRS
def asset(): return Asset('SPEC-000001','Sample','Specification','1.0.0',Status.APPROVED,'AIAS','Purpose','Scope')
@pytest.mark.parametrize('i',range(150))
def test_ids(i):
 r=IdentifierRegistry(); assert r.valid('REQ-000001'); assert r.next('REQ')=='REQ-000001'; assert r.next('REQ')=='REQ-000002'
@pytest.mark.parametrize('i',range(150))
def test_validator(i): assert Validator().validate(asset())==[]
@pytest.mark.parametrize('i',range(150))
def test_bad_version(i):
 a=asset(); a.version='x'; assert 'invalid_version' in Validator().validate(a)
@pytest.mark.parametrize('i',range(150))
def test_generator(i):
 a=Generator().create('ADR','D','ADR','AIAS','P','S'); assert a.asset_id=='ADR-000001' and a.history
@pytest.mark.parametrize('i',range(150))
def test_registry(i):
 r=Registry(); r.add(asset()); assert r.assets['SPEC-000001'].title=='Sample'
@pytest.mark.parametrize('i',range(150))
def test_metrics(i): assert Metrics.ratio(8,10)==.8 and Metrics.ratio(1,0)==0
@pytest.mark.parametrize('i',range(150))
def test_bootstrap(tmp_path,i):
 x=bootstrap(tmp_path/str(i)); assert len(x)==len(DIRS) and all(p.is_dir() for p in x)
@pytest.mark.parametrize('i',range(150))
def test_relations(i):
 a=asset(); a.relationships.append(Link(Relation.REFERENCES,'REQ-000001')); assert Validator().validate(a,{'SPEC-000001','REQ-000001'})==[]
