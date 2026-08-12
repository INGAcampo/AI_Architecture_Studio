"""Validación preventiva de perfiles normativos."""


class StandardValidator:

    REQUIRED_FIELDS = (
        "structural_basis",
        "concrete_code",
        "steel_code",
        "load_code",
        "seismic_code",
        "geotechnical_code",
        "quality_code",
    )

    @classmethod
    def validate(cls, profile):
        errors = []
        warnings = []

        if profile is None:
            return {
                "valid": False,
                "errors": ["No existe un perfil normativo activo."],
                "warnings": [],
            }

        for field_name in cls.REQUIRED_FIELDS:
            value = str(getattr(profile, field_name, "") or "").strip()
            if not value:
                errors.append(
                    f"Falta definir: {field_name.replace('_', ' ')}."
                )
            elif "confirmar" in value.lower() or value.lower() == "definir":
                warnings.append(
                    f"Debe confirmarse oficialmente: "
                    f"{field_name.replace('_', ' ')}."
                )

        if not profile.verified:
            warnings.append(
                "El perfil aún no está marcado como verificado por el "
                "profesional responsable."
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
