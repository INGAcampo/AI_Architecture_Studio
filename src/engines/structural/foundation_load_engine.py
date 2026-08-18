from models.structural.foundation_load_case import (
    FoundationLoadCase,
)


class FoundationLoadEngine:

    DEFAULT_CASES = [

        FoundationLoadCase(
            "Servicio",
            1.0,
            1.0,
        ),

        FoundationLoadCase(
            "Mayorada",
            1.2,
            1.6,
        ),
    ]
