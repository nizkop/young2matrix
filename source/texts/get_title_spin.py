
from typing import Tuple

from source.function_parts.text_kinds import text_kinds
from source.ui_parts.settings.idea_config import get_language
from source.ui_parts.settings.language_choices import language_choices


def get_title_spin(kind: text_kinds) -> Tuple[str, str, str]:
    if get_language() == language_choices.en.name:
        title = "spin functions"
        content = "(only non-vanishing combinations are listed)"
        content += r"\\ " if kind == text_kinds.TEX else "\n"
        content += "overlap of different tableaus is 0 (skipped here); overlap of the same tableaus, also having the same value "
        if kind == text_kinds.TEX:
            content += r"$m_S$-Wert is 1 (skipped here)\\"
        else:
            content += r"mS is 1 (skipped here)\n"
        content += "Here, the following informal representation of the tableaus and its spin functions is used: "
    else:
        title = r"Spinfunktionen"
        content = "(nur nicht verschwindende Kombinationen gezeigt)"
        content += r"\\ " if kind == text_kinds.TEX else "\n"
        content += r"Überlapp zw. versch. Tableaus ist 0 (wird hier ausgelassen), "
        if kind == text_kinds.TEX:
            content += r"Überlapp zwischen gleichen Tableaus mit gleichem $m_S$-Wert ist 1 (wird hier ausgelassen)\\"
        else:
            content += r"Überlapp zwischen gleichen Tableaus mit gleichem mS-Wert ist 1 (wird hier ausgelassen)"+"\n"
        content += r"hier informale Darstellung der Tableaus mit Spinfunktionen nach dem Schema: "


    # if kind == text_kinds.TEX:
    equation = r"\bra{\,\text{Tableau 1}\,}\ket{\,\text{Tableau 2}\,} "
    equation += r"= \bra{\, \underbrace{S \quad m_S}_{\text{von Tableau 1}} \,}"
    equation += r" \ket{\, \underbrace{S \quad m_S}_{\text{von Tableau 2}} \,} "
    equation += r"= \underbrace{...}_{\text{Überlapp der Tableaus 1 und 2}}"
    # else: TODO ?

    return (title, content, equation)
