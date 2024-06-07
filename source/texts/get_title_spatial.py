from typing import Tuple

from source.function_parts.TextKinds import TextKinds
from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


def get_title_spatial(kind: TextKinds) -> Tuple[str, str]:
    """
    get the title for the page of spatial functions (before integral building)
    :param kind: choice between not-particular or latex formatted
    :return: title of spatial chapter
    """
    if get_language() == LanguageChoices.en.name:
        title = "spatial functions"
        content = " (only non-vanishing combinations are listed)"
        content += r"\\" if kind == TextKinds.TEX else "\n"
        content += "(because of the normed functions in them) identical tableaus fall back to an overlap of 1. This is why those tableaus are not shown here."
    else:
        title = "Raumfunktionen"
        content = r" (nur nicht verschwindende Kombinationen gezeigt)"
        content += r"\\" if kind == TextKinds.TEX else "\n"
        content += r"Identische Tableaus ergeben (aufgrund der normierten Funktionen darin) automatisch 1 und werden daher hier nicht aufgelistet."

    return (title, content)