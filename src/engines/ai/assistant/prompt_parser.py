from __future__ import annotations
import re

from .intent import AssistantIntent, IntentType


class PromptParser:
    _count_pattern = re.compile(r"cu[aá]nt(?:os|as)", re.IGNORECASE)
    _modify_pattern = re.compile(
        r"(aumenta|reduce|cambia|modifica)\s+(?:la\s+)?(?P<property>\w+)"
        r"(?:\s+(?:a|en)\s+(?P<value>[0-9]+(?:[.,][0-9]+)?))?",
        re.IGNORECASE,
    )

    def parse(self, prompt: str) -> AssistantIntent:
        text = prompt.strip()
        if not text:
            return AssistantIntent(IntentType.UNKNOWN, 0.0, raw_prompt=prompt)

        lower = text.lower()

        if "seleccion" in lower or "seleccionado" in lower:
            return AssistantIntent(
                IntentType.QUERY_SELECTION,
                0.95,
                raw_prompt=prompt,
            )

        if "incidencia" in lower or "problema" in lower or "error" in lower:
            return AssistantIntent(
                IntentType.QUERY_ISSUES,
                0.92,
                raw_prompt=prompt,
            )

        if "contexto" in lower or "nivel activo" in lower or "disciplina" in lower:
            return AssistantIntent(
                IntentType.QUERY_CONTEXT,
                0.88,
                raw_prompt=prompt,
            )

        if self._count_pattern.search(lower):
            entity = "elements"
            for candidate in ("columnas", "puertas", "muros", "vigas", "losas"):
                if candidate in lower:
                    entity = candidate
                    break
            return AssistantIntent(
                IntentType.QUERY_COUNTS,
                0.90,
                entities={"entity": entity},
                raw_prompt=prompt,
            )

        if "ejecuta reglas" in lower or "revisa el proyecto" in lower:
            return AssistantIntent(
                IntentType.RUN_RULES,
                0.93,
                raw_prompt=prompt,
            )

        match = self._modify_pattern.search(text)
        if match:
            raw_value = match.group("value")
            value = None
            if raw_value is not None:
                value = float(raw_value.replace(",", "."))
            return AssistantIntent(
                IntentType.MODIFY_PROPERTY,
                0.85,
                entities={
                    "property": match.group("property").lower(),
                    "value": value,
                },
                raw_prompt=prompt,
            )

        return AssistantIntent(
            IntentType.UNKNOWN,
            0.20,
            raw_prompt=prompt,
        )
