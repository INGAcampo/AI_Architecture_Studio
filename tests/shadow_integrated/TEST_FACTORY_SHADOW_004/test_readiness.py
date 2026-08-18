from shadow_test_factory_reconcile.readiness import audit_queue_entries


def test_readiness_accepts_valid_manifest(tmp_path):
    manifest=tmp_path/"m.json"
    manifest.write_text("{}",encoding="ascii")

    result=audit_queue_entries(
        (
            {
                "megablock":"A",
                "state":"READY_FOR_RECONCILIATION",
                "package_manifest":str(manifest),
                "integration_authorized":False,
            },
        )
    )

    assert result.passed is True
    assert result.ready_count==1


def test_readiness_rejects_missing_manifest():
    result=audit_queue_entries(
        (
            {
                "megablock":"A",
                "state":"READY_FOR_RECONCILIATION",
                "package_manifest":"Z:/does/not/exist.json",
                "integration_authorized":False,
            },
        )
    )

    assert result.passed is False
    assert result.manifest_missing==("A",)


def test_readiness_rejects_authority_leak(tmp_path):
    manifest=tmp_path/"m.json"
    manifest.write_text("{}",encoding="ascii")

    result=audit_queue_entries(
        (
            {
                "megablock":"A",
                "state":"READY_FOR_RECONCILIATION",
                "package_manifest":str(manifest),
                "integration_authorized":True,
            },
        )
    )

    assert result.passed is False
    assert result.authority_violations==("A",)


def test_readiness_rejects_duplicate_megablock(tmp_path):
    manifest=tmp_path/"m.json"
    manifest.write_text("{}",encoding="ascii")

    entries=(
        {
            "megablock":"A",
            "state":"READY_FOR_RECONCILIATION",
            "package_manifest":str(manifest),
            "integration_authorized":False,
        },
        {
            "megablock":"A",
            "state":"READY_FOR_RECONCILIATION",
            "package_manifest":str(manifest),
            "integration_authorized":False,
        },
    )

    result=audit_queue_entries(entries)
    assert result.passed is False
    assert result.duplicate_megablocks==("A",)
