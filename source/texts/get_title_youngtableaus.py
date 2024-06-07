from typing import Tuple

from source.function_parts.TextKinds import TextKinds
from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


def get_title_multiplied_youngtableaus(kind:TextKinds) -> Tuple[str,str]:
    """ get title for page with multiplied out tableaus
    :param kind: choice between not-particular or latex formatted
    :return: title name
    """
    if get_language() == LanguageChoices.en.name:
        header = "young tableaus in their multiplied out form"
        content = "a, b, c, ... " if kind == TextKinds.TXT else r"$a, b, c, \hdots \quad $ "
        content += "= general functions, that could e.g. represent p orbitals"
    else:
        header = "Ausmultiplizierte Young-Tableaus"
        if kind == TextKinds.TXT:
            content = "a, b, c, ... "
        else:
            content = r"$a, b, c, \hdots \quad $ "
        content += "= allgemeine Funktionen, die beispielsweise p-Orbitale repräsentieren könnten"

    return (header, content)