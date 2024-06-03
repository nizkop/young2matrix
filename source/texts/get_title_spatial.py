from typing import Tuple

from source.function_parts.text_kinds import text_kinds
from source.settings.language_choices import language_choices
from source.settings.settings_config import get_language


def get_title_spatial(kind: text_kinds) -> Tuple[str, str]:
    if get_language() == language_choices.en.name:
        title = "spatial functions"
        content = " (only non-vanishing combinations are listed)"
        content += r"\\" if kind == text_kinds.TEX else "\n"
        content += "(because of the normed functions in them) identical tableaus fall back to an overlap of 1. This is why those tableaus are not shown here."
    else:
        title = "Raumfunktionen"
        content = r" (nur nicht verschwindende Kombinationen gezeigt)"
        content += r"\\" if kind == text_kinds.TEX else "\n"
        content += r"Identische Tableaus ergeben (aufgrund der normierten Funktionen darin) automatisch 1 und werden daher hier nicht aufgelistet."

    return (title, content)