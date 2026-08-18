import pytest

from engines.structural.frame import (
    IntelligentStructuralFrameEngine,
    ProfileShape,
    StructuralElementKind,
    StructuralMaterial,
    StructuralMaterialCatalog,
    StructuralMaterialKind,
    StructuralMember,
    StructuralMemberValidator,
    StructuralPoint,
    StructuralProfile,
    StructuralProfileCatalog,
    structural_member_parameter_definitions,
)


@pytest.mark.parametrize("kind", list(StructuralElementKind))
def test_element_kinds(kind):
    assert kind.value


@pytest.mark.parametrize("kind", list(StructuralMaterialKind))
def test_material_kinds(kind):
    material = StructuralMaterial("m", "Material", kind, 1000)
    assert material.kind is kind


@pytest.mark.parametrize("shape", list(ProfileShape))
def test_profile_shapes(shape):
    profile = StructuralProfile("p", "Profile", shape, 0.01, 1e-4, 1e-4)
    assert profile.shape is shape


@pytest.mark.parametrize("length", [1,2,3,4,5,6,8,10,12,20])
def test_member_lengths(length):
    member = StructuralMember(
        "m", StructuralElementKind.BEAM,
        StructuralPoint(0,0,0), StructuralPoint(length,0,0),
        "p","mat"
    )
    assert member.length == pytest.approx(length)


@pytest.mark.parametrize("length", [1,2,3,4,5,6,8,10,12,20])
def test_member_midpoints(length):
    member = StructuralMember(
        "m", StructuralElementKind.BEAM,
        StructuralPoint(0,0,0), StructuralPoint(length,0,0),
        "p","mat"
    )
    assert member.midpoint.x == pytest.approx(length/2)


@pytest.mark.parametrize("density", [450,600,1000,2400,2700,5000,7850,8000,9000,10000])
def test_material_density(density):
    assert StructuralMaterial("m","Material",StructuralMaterialKind.GENERIC,density).density == density


@pytest.mark.parametrize("area", [0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1.0])
def test_profile_area(area):
    profile = StructuralProfile("p","Profile",ProfileShape.GENERIC,area,1e-4,1e-4)
    assert profile.area == area


@pytest.mark.parametrize("index", range(10))
def test_material_catalog(index):
    catalog = StructuralMaterialCatalog()
    item = StructuralMaterial(f"m{index}", f"Material {index}", StructuralMaterialKind.STEEL, 7850)
    catalog.register(item)
    assert catalog.get(item.material_id) is item
    assert catalog.remove(item.material_id) is item


@pytest.mark.parametrize("index", range(10))
def test_profile_catalog(index):
    catalog = StructuralProfileCatalog()
    item = StructuralProfile(f"p{index}", f"Profile {index}", ProfileShape.I, 0.01, 1e-4, 1e-4)
    catalog.register(item)
    assert catalog.get(item.profile_id) is item
    assert catalog.remove(item.profile_id) is item


def make_engine():
    engine = IntelligentStructuralFrameEngine()
    engine.register_material(
        StructuralMaterial("steel", "Steel", StructuralMaterialKind.STEEL, 7850)
    )
    engine.register_profile(
        StructuralProfile("ipe", "IPE", ProfileShape.I, 0.005, 1e-4, 1e-5)
    )
    return engine


def test_model_validation():
    with pytest.raises(ValueError):
        StructuralPoint(float("inf"),0,0)
    with pytest.raises(ValueError):
        StructuralMaterial("", "M", StructuralMaterialKind.STEEL, 7850)
    with pytest.raises(ValueError):
        StructuralProfile("", "P", ProfileShape.I, 0.01, 1e-4, 1e-4)


def test_validator_accepts_member():
    member = StructuralMember("m", StructuralElementKind.BEAM, StructuralPoint(0,0,0), StructuralPoint(1,0,0), "p","mat")
    assert StructuralMemberValidator().validate(member).valid


def test_engine_add_remove():
    engine = make_engine()
    member = StructuralMember("m", StructuralElementKind.BEAM, StructuralPoint(0,0,0), StructuralPoint(6,0,0), "ipe","steel")
    engine.add_member(member)
    assert engine.remove_member("m") is member


def test_engine_change_profile():
    engine = make_engine()
    engine.register_profile(StructuralProfile("rhs","RHS",ProfileShape.RHS,0.01,2e-4,2e-4))
    engine.add_member(StructuralMember("m",StructuralElementKind.COLUMN,StructuralPoint(0,0,0),StructuralPoint(0,0,3),"ipe","steel"))
    engine.change_profile("m","rhs")
    assert engine.get_member("m").profile_id == "rhs"


def test_engine_quantities():
    engine = make_engine()
    engine.add_member(StructuralMember("m",StructuralElementKind.BEAM,StructuralPoint(0,0,0),StructuralPoint(10,0,0),"ipe","steel"))
    q = engine.calculate_quantities("m")
    assert q.length == 10
    assert q.volume == pytest.approx(0.05)
    assert q.mass == pytest.approx(392.5)


def test_parameter_definitions():
    ids = {d.parameter_id for d in structural_member_parameter_definitions()}
    assert {"length","area","volume","mass","weight"} <= ids


def test_events():
    events = []
    engine = IntelligentStructuralFrameEngine(event_dispatcher=lambda name,payload: events.append((name,payload)))
    engine.register_material(StructuralMaterial("steel","Steel",StructuralMaterialKind.STEEL,7850))
    engine.register_profile(StructuralProfile("ipe","IPE",ProfileShape.I,0.005,1e-4,1e-5))
    engine.add_member(StructuralMember("m",StructuralElementKind.BEAM,StructuralPoint(0,0,0),StructuralPoint(1,0,0),"ipe","steel"))
    assert events[0][0] == "structural.material.registered"
    assert events[-1][0] == "structural.member.added"


@pytest.mark.parametrize("index", range(33))
def test_additional_structural_members(index):
    engine = make_engine()
    member = StructuralMember(
        f"extra-{index}",
        StructuralElementKind.BEAM,
        StructuralPoint(0,0,0),
        StructuralPoint(index + 1,0,0),
        "ipe",
        "steel",
    )
    engine.add_member(member)
    assert engine.get_member(member.member_id) is member
