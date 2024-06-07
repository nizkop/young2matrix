from enum import Enum

from source.settings.LanguageChoices import LanguageChoices
from source.settings.settings_config import get_language


class UiPages(Enum):
    """ correlation between pages names/content and their indices """
    START = 0
    TABLEAUS = 1
    MULTIPLIED_OUT_TABLEAUS = 2
    SPIN = 3
    SPATIAL_FUNCTIONS = 4
    DOWNLOAD = 5
    OVERLAP_SPIN = 6
    OVERLAP_SPATIAL = 7
    HAMILTON_SPIN = 8
    HAMILTON_SPATIAL = 9



def get_page_name(page:UiPages) -> str:
    """
    get the explanation of a button leading to a given page;
    regarding the current language
    :param page: screen the button leads to
    :return: name/label of the page
    """
    if page == UiPages.START:
        return "Startseite" if get_language() == LanguageChoices.de.name else "start"
    if page == UiPages.TABLEAUS:
        return "Tableaus" if get_language() == LanguageChoices.de.name else "tableaus"
    if page == UiPages.MULTIPLIED_OUT_TABLEAUS:
        return "Ausmultiplizierte Tableaus" if get_language() == LanguageChoices.de.name else "multiplied out tableaus"
    if page == UiPages.SPIN:
        return "Spinfunktionen" if get_language() == LanguageChoices.de.name else "spin functions"
    if page == UiPages.SPATIAL_FUNCTIONS:
        return "Raumfunktionen" if get_language() == LanguageChoices.de.name else "spatial functions"
    if page == UiPages.DOWNLOAD:
        return "Download" if get_language() == LanguageChoices.de.name else "download"
    if page == UiPages.OVERLAP_SPIN:
        return "Überlapp Spin" if get_language() == LanguageChoices.de.name else "overlap of spin functions"
    if page == UiPages.OVERLAP_SPATIAL:
        return "Überlapp Raum" if get_language() == LanguageChoices.de.name else "overlap of spatial functions"
    if page == UiPages.HAMILTON_SPIN:
        return "Hamilton Spin" if get_language() == LanguageChoices.de.name else "hamilton integrals for spin"
    if page == UiPages.HAMILTON_SPATIAL:
        return "Hamilton Raum" if get_language() == LanguageChoices.de.name else "hamilton integrals for spatial functions"
    return "unbekannt" if get_language() == LanguageChoices.de.name else "unknown"


