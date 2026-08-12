"""Registro de perfiles normativos.

Los nombres son plantillas configurables. La edición oficial aplicable debe
ser confirmada por el profesional responsable y por la autoridad local.
"""

from core.standards.standard_profile import StandardProfile


class StandardRegistry:

    @staticmethod
    def built_in_profiles():
        return {
            "metric_custom": StandardProfile(
                profile_id="metric_custom",
                name="Métrico personalizado",
                country="Personalizado",
                jurisdiction="Definida por el proyecto",
                structural_basis="Definir",
                concrete_code="Definir",
                steel_code="Definir",
                load_code="Definir",
                seismic_code="Definir",
                wind_code="Definir",
                geotechnical_code="Definir",
                fire_code="Definir",
                accessibility_code="Definir",
                quality_code="Definir",
                verified=False,
                notes=(
                    "Perfil editable para proyectos sin plantilla nacional "
                    "preconfigurada."
                ),
            ),
            "venezuela": StandardProfile(
                profile_id="venezuela",
                name="Venezuela — Perfil configurable",
                country="Venezuela",
                jurisdiction="Nacional / municipal",
                structural_basis="COVENIN / criterios del proyecto",
                concrete_code="COVENIN / ACI, edición por confirmar",
                steel_code="COVENIN / AISC, edición por confirmar",
                load_code="COVENIN, edición por confirmar",
                seismic_code="COVENIN sísmica, edición por confirmar",
                wind_code="COVENIN viento, edición por confirmar",
                geotechnical_code="Norma y estudio geotécnico del proyecto",
                fire_code="Normativa nacional y municipal aplicable",
                accessibility_code="Normativa nacional y municipal aplicable",
                quality_code="COVENIN / plan de calidad del proyecto",
                verified=False,
                notes=(
                    "Las ediciones deben verificarse para la ubicación, "
                    "tipo de obra y autoridad competente."
                ),
            ),
            "international": StandardProfile(
                profile_id="international",
                name="Internacional — ISO/IEC/IFC",
                country="Internacional",
                jurisdiction="Definida por contrato",
                structural_basis="Norma estructural definida por contrato",
                concrete_code="Código de concreto definido por contrato",
                steel_code="Código de acero definido por contrato",
                load_code="Código de cargas definido por contrato",
                seismic_code="Código sísmico definido por contrato",
                wind_code="Código de viento definido por contrato",
                geotechnical_code="ISO / código geotécnico del contrato",
                fire_code="Código de incendio del contrato",
                accessibility_code="Código de accesibilidad del contrato",
                quality_code="ISO 9001 / plan de calidad",
                bim_standard="IFC / ISO 19650",
                verified=False,
            ),
            "usa": StandardProfile(
                profile_id="usa",
                name="Estados Unidos — Perfil configurable",
                country="Estados Unidos",
                jurisdiction="Estado / ciudad / autoridad competente",
                structural_basis="IBC, edición local por confirmar",
                concrete_code="ACI 318, edición por confirmar",
                steel_code="AISC 360, edición por confirmar",
                load_code="ASCE 7, edición por confirmar",
                seismic_code="ASCE 7 / IBC, edición por confirmar",
                wind_code="ASCE 7, edición por confirmar",
                geotechnical_code="IBC / informe geotécnico",
                fire_code="IBC / NFPA, edición local por confirmar",
                accessibility_code="ADA / código local",
                quality_code="Especificaciones del proyecto / ASTM",
                verified=False,
            ),
            "europe": StandardProfile(
                profile_id="europe",
                name="Europa — Eurocódigos",
                country="Unión Europea",
                jurisdiction="País y anexo nacional",
                structural_basis="Eurocódigos + Anexo Nacional",
                concrete_code="EN 1992, edición por confirmar",
                steel_code="EN 1993, edición por confirmar",
                load_code="EN 1991, edición por confirmar",
                seismic_code="EN 1998, edición por confirmar",
                wind_code="EN 1991-1-4, edición por confirmar",
                geotechnical_code="EN 1997, edición por confirmar",
                fire_code="Eurocódigos de fuego + norma nacional",
                accessibility_code="Normativa nacional aplicable",
                quality_code="EN / ISO / plan de calidad",
                verified=False,
            ),
            "spain": StandardProfile(
                profile_id="spain",
                name="España — Perfil configurable",
                country="España",
                jurisdiction="Nacional / autonómica / municipal",
                structural_basis="CTE / Código Estructural",
                concrete_code="Código Estructural, edición por confirmar",
                steel_code="Código Estructural, edición por confirmar",
                load_code="CTE DB-SE-AE, edición por confirmar",
                seismic_code="Normativa sísmica vigente por confirmar",
                wind_code="CTE DB-SE-AE, edición por confirmar",
                geotechnical_code="CTE DB-SE-C / estudio geotécnico",
                fire_code="CTE DB-SI",
                accessibility_code="CTE DB-SUA + normativa local",
                quality_code="Código Estructural / plan de control",
                verified=False,
            ),
            "colombia": StandardProfile(
                profile_id="colombia",
                name="Colombia — Perfil configurable",
                country="Colombia",
                jurisdiction="Nacional / municipal",
                structural_basis="NSR, edición por confirmar",
                concrete_code="NSR / ACI, edición por confirmar",
                steel_code="NSR / AISC, edición por confirmar",
                load_code="NSR, edición por confirmar",
                seismic_code="NSR, edición por confirmar",
                wind_code="NSR, edición por confirmar",
                geotechnical_code="NSR / estudio geotécnico",
                fire_code="NSR / normativa local",
                accessibility_code="Normativa nacional y local",
                quality_code="NSR / plan de calidad",
                verified=False,
            ),
        }

    @classmethod
    def get(cls, profile_id):
        return cls.built_in_profiles().get(profile_id)

    @classmethod
    def names(cls):
        return {
            profile_id: profile.name
            for profile_id, profile in cls.built_in_profiles().items()
        }
