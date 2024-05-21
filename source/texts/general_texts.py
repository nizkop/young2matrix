from source.ui_parts.settings.language_config import get_language
from source.ui_parts.settings.language_choices import language_choices


def get_general_text(key:str) -> str:
    """
    getting text phrases;
    function combines multiple text parts, that can be addressed via a key;
    allowes for change in language
    :param key: indication, which text is needed
    :return: fully expressed text in choosen language
    """

    if get_language() == language_choices.en.name:
        general_texts = {
            "overlap_header": "overlap integrals of ",
            "spatial_header": "spatial functions",
            "spin_header": "spin functions",
            "tableau_header": "young tableaus",
            "spin_2rows": "(Because there are only two spin functions α, β, more than two anti symmetric spin functions are impossible.)",
            "spin_2rows_tex": r"\textit{(Because there are only two spin functions $\alpha, \beta$, more than two anti symmetric spin functions are impossible.)}",
            "spatial_2columns": "(Bacause spatial tableaus have to be adjoint to the spin tableaus" +
                                " (and for them only two functions can be anti symmetric at most), " +
                                "more than two columns are impossible.)",
            "too_small_for_overlap": "This permutation group is too small to lead to non-trivial combinations of basis functions.",
            "h_info_spin": "Attention: The Hamiltonian does not depend on the spin. Thereby hamilton integrals of spin functions revert to overlap integrals and are not listed again here.",
            "header_hamilton_general": "hamilton integrals",
            "ref_hspin": " (s. section 4.2) ",
            "header_overlap_general": "overlap integrals",


            # solely UI:
            "settings_change": "change setting (language/design).",
            "choose_language": "choose a language:",
            "choose_color": "change the color scheme:",
            "help": "What is happening here?",
            "download_start_info1": "You have started the download for permutation group ",
            "download_start_info2": ".\n\nPlease be patient.",
            "language_change": "change language to German",
            "input_line_command": "Please enter a permutation group number.",
            "warning": "warning",
            "yes": "Yes",
            "no": "No",
            "check_big_data": "This is a high number for a permutation group, that gets even bigger by all the needed combinations. Are you sure you want to continue?",
            "input_command": "permutation group:",
            "warning_no_group": "Please fill in a permutation group.",
            "warning_wrong_number": "Please give the permutation group as positive number.",
            "warning_wrong_type": "Please fill in an integer for setting the permutations group.",
            "successful_download": "The download was successful.",
            "failed_download": "Sadly, we encountered an unknown error while downloading the pdf.",

        }
    else: # default
        general_texts ={
            "overlap_header": "Überlappungsintegrale von ",
            "spatial_header": "Raum-Funktionen",
            "spin_header": "Spin-Funktionen",
            "tableau_header": "Young-Tableaus",
            "spin_2rows": "(Da es nur zwei Spinfunktionen α, β gibt, sind mehr als zwei antisymmetrische Funktionen nicht möglich.)",
            "spin_2rows_tex": r"\textit{(Da es nur zwei Spinfunktionen $\alpha, \beta$ gibt, sind mehr als zwei antisymmetrische Funktionen nicht möglich.)}",
            "spatial_2columns": "(Da die Raum-Tableaus adjoint zu den Spin-Tableaus sein müssen"+
                         " (und dort nur maximal 2 Funktionen antisymmetrisch sein können), "+
                         "sind nicht mehr als zwei Spalten möglich.)",
            "too_small_for_overlap": "Die Permutationsgruppe ist zu klein, um nicht-triviale Kombinationen von Basisfunktionen zu bilden. ",
            "h_info_spin": "Achtung: Der Hamiltonoperator ist unabhängig vom Spin, daher werden die Hamiltonintegrale der Spin-Tableaus zu den Überlappungsintegralen und werden hier nicht erneut aufgeführt.",
            "header_hamilton_general": "Hamiltonmatrixelemente",
            "ref_hspin": " (s. Kapitel 4.2) ",
            "header_overlap_general": "Überlappungsintegrale",

            # solely UI:
            "settings_change": "Einstellungen (Sprache/Design) ändern.",
            "choose_language": "Sprachauswahl:",
            "choose_color": "Anpassen der Farbgestaltung:",
            "help": "Was passiert hier eigentlich?",
            "download_start_info1": "Sie haben den Download für die Permutationsgruppe ",
            "download_start_info2": " gestartet.\n\nBitte haben Sie einen Moment Geduld.",
            "language_change": "Sprache zu Englisch ändern",
            "input_line_command": "Bitte geben Sie eine Permutationsgruppennummer ein.",
            "warning": "Warnung",
            "yes": "Ja",
            "no": "Nein",
            "check_big_data": "Diese Eingabe ist eine relativ große Permutationsgruppe, die durch Kombination der enthaltenen Terme ncoh deutlich größer wird. Wollen Sie wirklich fortfahren?",
            "input_command": "Permutationsgruppe:",
            "warning_no_group": "Bitte geben Sie eine Permutationsgruppe ein.",
            "warning_wrong_number": "Bitte geben Sie eine Permutationsgruppe als positive Zahl.",
            "warning_wrong_type": "Bitte geben Sie die Nummer für eine Permutationsgruppe ein.",
            "successful_download": "Der Download war erfolgreich.",
            "failed_download": "Leider gab es ein unbekanntes Problem beim Downloaden.",
            "header_hamilton_spatial": "Hamiltonmatrixelemente für die Raumorbitale",

        }

    return general_texts[key]