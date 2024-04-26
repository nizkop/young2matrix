from source.ui_parts.settings.idea_config import get_language


def get_title_permutation_to_tableaus(permutation_group:int):
    if get_language() == "en":
        return f"All possible (standard) young tableaus for the group {permutation_group} are:"
    return f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {permutation_group} lauten:"