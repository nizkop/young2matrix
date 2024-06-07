
from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


def get_title_permutation_to_tableaus(permutation_group:int) -> str:
    """
    getting the title for the chapter showing all possible young tableaus
    :param permutation_group: size of the permutation group (actual selection)
    :return: title for first calculated chapter
    """
    if get_language() == LanguageChoices.en.name:
        return f"All possible (standard) young tableaus for the group {permutation_group} are:"
    return f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {permutation_group} lauten:"