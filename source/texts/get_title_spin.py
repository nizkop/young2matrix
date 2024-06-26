from typing import Tuple

from source.function_parts.TextKinds import TextKinds
from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


def get_title_spin(kind: TextKinds) -> Tuple[str, str, str]:
    """
    get introduction text for the spin overlap chapter
    :param kind: choice of formatting (latex/normal text)
    :return: describing text as a tuple of the title, explaining sentences and the example equation
    """
    if get_language() == LanguageChoices.en.name:
        title = "spin functions"
        content = "(only non-vanishing combinations are listed)"
        content += r"\\ " if kind == TextKinds.TEX else "\n"
        content += "overlap of different tableaus is 0 (skipped here); overlap of the same tableaus, also having the same value "
        if kind == TextKinds.TEX:
            content += r"$m_S$-Wert is 1 (skipped here)\\"
        else:
            content += r"mS is 1 (skipped here)\n"
        content += "Here, the following informal representation of the tableaus and its spin functions is used: "
    else:
        title = r"Spinfunktionen"
        content = "(nur nicht verschwindende Kombinationen gezeigt)"
        content += r"\\ " if kind == TextKinds.TEX else "\n"
        content += r"Überlapp zw. versch. Tableaus ist 0 (wird hier ausgelassen), "
        if kind == TextKinds.TEX:
            content += r"Überlapp zwischen gleichen Tableaus mit gleichem $m_S$-Wert ist 1 (wird hier ausgelassen)\\"
        else:
            content += r"Überlapp zwischen gleichen Tableaus mit gleichem mS-Wert ist 1 (wird hier ausgelassen)"+"\n"
        content += r"hier informale Darstellung der Tableaus mit Spinfunktionen nach dem Schema: "

    if kind == TextKinds.TEX:
        equation = r"\bra{\,\text{Tableau 1}\,}\ket{\,\text{Tableau 2}\,} "
        equation += r"= \bra{\, \underbrace{S \quad m_S}_{\text{von Tableau 1}} \,}"
        equation += r" \ket{\, \underbrace{S \quad m_S}_{\text{von Tableau 2}} \,} "
        equation += r"= \underbrace{...}_{\text{Überlapp der Tableaus 1 und 2}}"
    else:
        equation = " "*5
        if get_language() == LanguageChoices.en.name:
            equation += r""" "overlap of the tableaus 1 and 2"  =  < tableau 1 | tableau 2 > """
        else:
            equation += r""" "Überlapp der Tableaus 1 und 2"  =  < Tableau 1 | Tableau 2 > """
        equation += "\n"+" "*5 +"=  < S  m_S | S  m_S >  =  ... "

    return (title, content, equation)
