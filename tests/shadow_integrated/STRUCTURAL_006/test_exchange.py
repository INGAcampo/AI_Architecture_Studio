from structural_platform_exchange.contracts import StructuralExchangeEnvelope,StructuralResultRecord
from structural_platform_exchange.codec import encode_exchange_json,decode_exchange_json,exchange_sha256


def make_envelope():
    return StructuralExchangeEnvelope(
        schema_version="1.0",
        source_engine="AIAS_SHADOW",
        model_id="MODEL-1",
        results=(
            StructuralResultRecord("B1","M3",120.0,"N*m","ULS-1"),
            StructuralResultRecord("B1","V2",30.0,"N","ULS-1"),
        ),
    )


def test_exchange_roundtrip_is_lossless():
    original=make_envelope()
    decoded=decode_exchange_json(encode_exchange_json(original))
    assert decoded==original


def test_exchange_hash_is_deterministic():
    envelope=make_envelope()
    assert exchange_sha256(envelope)==exchange_sha256(envelope)
    assert len(exchange_sha256(envelope))==64


def test_invalid_result_record_fails_closed():
    failed=False
    try:
        StructuralResultRecord("","M3",1.0,"N*m","CASE").validate()
    except ValueError:
        failed=True
    assert failed is True
