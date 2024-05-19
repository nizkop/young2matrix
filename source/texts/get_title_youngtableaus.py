from source.function_parts.text_kinds import text_kinds
from source.ui_parts.settings.idea_config import get_language


def get_title_multiplied_youngtableaus(kind:text_kinds):
    if get_language() == "en":
        header = "young tableaus in their multiplied out form"
        content = "a, b, c, ... " if kind == text_kinds.TXT else r"$a, b, c, \hdots \quad $ "
        content += "= general functions, that could e.g. represent p orbitals"
    else:
        header = "Ausmultiplizierte Young-Tableaus"
        if kind == text_kinds.TXT:
            content = "a, b, c, ... "
        else:
            content = r"$a, b, c, \hdots \quad $ "
        content += "= allgemeine Funktionen, die beispielsweise p-Orbitale repräsentieren könnten"

    return (header, content)