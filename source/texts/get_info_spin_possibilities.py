from source.function_parts.text_kinds import text_kinds
from source.ui_parts.settings.idea_config import get_language


def get_info_spin_possibilities(permutation_group:int, kind:text_kinds) -> str:
    if get_language() == "en":
        s = r"Possible combinations "
        s += r"$\ket{S \; M_S}$" if kind == text_kinds.TEX else "| S Ms >"
        s += "for the tableaus of permutation group "
        return s + f"{permutation_group} are:"
    else:
        s = r"Die möglichen Kombinationen "
        s += "$\ket{S \; M_S}$" if kind == text_kinds.TEX else "| S Ms >"
        s+= " für die Tableaus der "
        return s + fr"Permutationsgruppe {permutation_group} lauten:"