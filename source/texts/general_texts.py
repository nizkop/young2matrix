from source.ui_parts.settings.idea_config import get_language



def get_general_text(key:str):

    if get_language() == "en":
        general_texts = {

            "spin_2rows": "(Because there are only two spin functions α, β, more than two anti symmetric spin functions are impossible.)",
            "spin_2rows_tex": r"\textit{(Because there are only two spin functions $\alpha, \beta$, more than two anti symmetric spin functions are impossible.)}",
            "spatial_2columns": "(Bacause spatial tableaus have to be adjoint to the spin tableaus" +
                                " (and for them only two functions can be anti symmetric at most), " +
                                "more than two columns are impossible.)",

            # solely UI:
            "input_command": "permutation group:",
            "warning_no_group": "Please fill in a permutation group.",
            "warning_wrong_number": "Please give the permutation group as positive number.",
            "warning_wrong_type": "Please fill in an integer for setting the permutations group.",
            "successful_download": "The download was successful.",
            "failed_download": "Sadly, we encountered an unknown error while downloading the pdf.",
            "h_info_spin": "",#TODO
        }
    else: # default
        general_texts ={
            "spin_2rows": "(Da es nur zwei Spinfunktionen α, β gibt, sind mehr als zwei antisymmetrische Funktionen nicht möglich.)",
            "spin_2rows_tex": r"\textit{(Da es nur zwei Spinfunktionen $\alpha, \beta$ gibt, sind mehr als zwei antisymmetrische Funktionen nicht möglich.)}",
            "spatial_2columns": "(Da die Raum-Tableaus adjoint zu den Spin-Tableaus sein müssen"+
                         " (und dort nur maximal 2 Funktionen antisymmetrisch sein können), "+
                         "sind nicht mehr als zwei Spalten möglich.)",

            # solely UI:
            "input_command": "Permutationsgruppe:",
            "warning_no_group": "Bitte geben Sie eine Permutationsgruppe ein.",
            "warning_wrong_number": "Bitte geben Sie eine Permutationsgruppe als positive Zahl.",
            "warning_wrong_type": "Bitte geben Sie die Nummer für eine Permutationsgruppe ein.",
            "successful_download": "Der Download war erfolgreich.",
            "failed_download": "Leider gab es ein unbekanntes Problem beim Downloaden.",
            "h_info_spin": "Achtung: Der Hamiltonoperator ist unabhängig vom Spin, daher werden die Hamiltonintegrale der Spin-Tableaus zu den Überlappungsintegralen (s. Kapitel 4.2) und werden hier nicht erneut aufgeführt."
        }

    return general_texts[key]