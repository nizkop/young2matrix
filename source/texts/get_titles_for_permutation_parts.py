
from source.settings.language_choices import language_choices
from source.settings.settings_config import get_language


def get_title_permutation_to_tableaus(permutation_group:int):
    """
    todo
    :param permutation_group:
    :return:
    """
    if get_language() == language_choices.en.name:
        return f"All possible (standard) young tableaus for the group {permutation_group} are:"
    return f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {permutation_group} lauten:"