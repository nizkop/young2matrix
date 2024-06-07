from source.function_parts.TextKinds import TextKinds
from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


def get_info_spin_possibilities(permutation_group:int, kind:TextKinds) -> str:
    """
    get introduction sentence fot the spin function chapter
    :param permutation_group: number of the permutation group
    :param kind: choice of formatting (latex/normal text)
    :return: introduction sentence
    """
    if get_language() == LanguageChoices.en.name:
        s = r"Possible combinations "
        s += r"$\ket{S \; M_S}$" if kind == TextKinds.TEX else "| S M_S >"
        s += " for the tableaus of permutation group "
        return s + f"{permutation_group} are:"
    else:
        s = r"Die möglichen Kombinationen "
        s += "$\ket{S \; M_S}$" if kind == TextKinds.TEX else "| S M_S >"
        s+= " für die Tableaus der "
        return s + fr"Permutationsgruppe {permutation_group} lauten:"