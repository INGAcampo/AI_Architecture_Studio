from geometry_bim_bridge_diff.diff import SceneItemSignature,diff_scene_signatures


A="a"*64
B="b"*64
C="c"*64
D="d"*64


def sig(instance,mesh=A,meta=B):
    return SceneItemSignature(instance,instance,mesh,meta)


def test_scene_diff_detects_all_change_classes():
    before=(sig("same"),sig("geom"),sig("meta"),sig("gone"))
    after=(
        sig("same"),
        sig("geom",mesh=C),
        sig("meta",meta=D),
        sig("new"),
    )

    result=diff_scene_signatures(before,after)

    assert result.added==("new",)
    assert result.removed==("gone",)
    assert result.geometry_changed==("geom",)
    assert result.metadata_changed==("meta",)
    assert result.unchanged==("same",)


def test_duplicate_instance_id_fails_closed():
    failed=False
    try:
        diff_scene_signatures((sig("x"),sig("x")),())
    except ValueError:
        failed=True
    assert failed is True


def test_invalid_hash_fails_closed():
    failed=False
    try:
        diff_scene_signatures(
            (SceneItemSignature("x","G","bad",B),),
            (),
        )
    except ValueError:
        failed=True
    assert failed is True
