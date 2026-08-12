import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_venezuela_is_formally_selected_but_normative_pack_remains_gated():
    program = json.loads(
        (ROOT / "engineering/aias/structural_codes/STRUCTURAL_CODES_PROGRAM.json").read_text(encoding="utf-8")
    )
    profile = json.loads(
        (ROOT / "engineering/aias/structural_codes/VE-001_VENEZUELA_JURISDICTION_PROFILE.json").read_text(encoding="utf-8")
    )
    assert program["initial_jurisdiction"] == "Venezuela"
    assert program["initial_jurisdiction_code"] == "VE"
    assert profile["decision"]["status"] == "FORMALLY_APPROVED_BY_PROJECT_DIRECTOR"
    assert profile["implementation_status"] == "OFFICIAL_QUOTATION_AND_ACQUISITION_DOSSIER_AUTHORIZED"
    assert profile["authorization"]["payment_status"] == "PENDING_FINAL_PRICE_LICENSE_AND_BILLING_APPROVAL"
    assert profile["construction_approved"] is False
    assert profile["normative_compliance_claimed"] is False


def test_venezuela_profile_covers_first_structural_and_bim_families_safely():
    profile = json.loads(
        (ROOT / "engineering/aias/structural_codes/VE-001_VENEZUELA_JURISDICTION_PROFILE.json").read_text(encoding="utf-8")
    )
    families = {item["family"] for item in profile["candidate_structural_inventory"]}
    assert {"LOADS_AND_ACTIONS", "SEISMIC_DESIGN", "STRUCTURAL_CONCRETE", "STRUCTURAL_STEEL", "BIM_DELIVERABLES"} <= families
    assert all(item["status"] != "AUTHORIZED_FOR_CALCULATION" for item in profile["candidate_structural_inventory"])
    assert len(profile["mandatory_activation_gates"]) >= 7
    assert profile["official_ecosystem"]["catalog_entry_point"].startswith("https://fondonorma.org.ve/")


def test_acquisition_dossier_authorizes_inquiry_but_not_blind_payment():
    dossier = json.loads(
        (ROOT / "engineering/aias/structural_codes/VE-002_NORMATIVE_ACQUISITION_DOSSIER.json").read_text(encoding="utf-8")
    )
    assert dossier["authorization"]["quotation_authorized"] is True
    assert dossier["authorization"]["payment_authorized"] is False
    assert dossier["authorization"]["purchase_authorized_up_to_amount"] is None
    assert len(dossier["requested_candidates"]) >= 5
    assert len(dossier["acceptance_criteria"]) >= 5
    assert dossier["applicant"]["legal_or_personal_name"] == "ALFREDO CAMPO"
    assert dossier["applicant"]["role"] == "PRESIDENTE"
    assert dossier["applicant"]["email"] == "CAMPOALFREDO7@GMAIL.COM"
    assert dossier["outbound_communication"]["status"] == "PREPARED_NOT_SENT"
    assert dossier["outbound_communication"]["payment_or_contract_created"] is False
    message = ROOT / dossier["outbound_communication"]["artifact"]
    assert message.is_file()
    text = message.read_text(encoding="utf-8")
    assert "To: atencionalcliente@fondonorma.org.ve" in text
    assert "From: campoalfredo7@gmail.com" in text
