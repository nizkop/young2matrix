from source.function_parts.text_kinds import text_kinds
from source.settings.language_choices import language_choices
from source.settings import get_language


def get_info_spin_possibilities(permutation_group:int, kind:text_kinds) -> str:
    """
    get introduction sentence fot the spin function chapter
    :param permutation_group: number of the permuation group
    :param kind: choice of formatting (latex/normal text)
    :return: introduction sentence
    """
    if get_language() == language_choices.en.name:
        s = r"Possible combinations "
        s += r"$\ket{S \; M_S}$" if kind == text_kinds.TEX else "| S M_S >"
        s += " for the tableaus of permutation group "
        return s + f"{permutation_group} are:"
    else:
        s = r"Die möglichen Kombinationen "
        s += "$\ket{S \; M_S}$" if kind == text_kinds.TEX else "| S M_S >"
        s+= " für die Tableaus der "
        return s + fr"Permutationsgruppe {permutation_group} lauten:"