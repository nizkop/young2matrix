from enum import Enum

from source.ui_parts.settings.idea_config import get_language


class ui_pages(Enum):
    """ correlation between pages names/content and their indizes """
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



def get_page_name(page:ui_pages) -> str:
    """
    get the explanation of a button leading to a given page;
    regarding the current language
    :param page: screen the button leads to
    :return: name/label of the page
    """
    if page == ui_pages.START:
        return "Startseite" if get_language() == "de" else "start"
    if page == ui_pages.TABLEAUS:
        return "Tableaus" if get_language() == "de" else "tableaus"
    if page == ui_pages.MULTIPLIED_OUT_TABLEAUS:
        return "Ausmultiplizierte Tableaus" if get_language() == "de" else "multiplied out tableaus"
    if page == ui_pages.SPIN:
        return "Spinfunktionen" if get_language() == "de" else "spin functions"
    if page == ui_pages.SPATIAL_FUNCTIONS:
        return "Raumfunktionen" if get_language() == "de" else "spatial functions"
    if page == ui_pages.DOWNLOAD:
        return "Download" if get_language() == "de" else "download"
    if page == ui_pages.OVERLAP_SPIN:
        return "Überlapp Spin" if get_language() == "de" else "overlap of spin functions"
    if page == ui_pages.OVERLAP_SPATIAL:
        return "Überlapp Raum" if get_language() == "de" else "overlap of spatial functions"
    if page == ui_pages.HAMILTON_SPIN:
        return "Hamilton Spin" if get_language() == "de" else "hamilton integrals for spin"
    if page == ui_pages.HAMILTON_SPATIAL:
        return "Hamilton Raum" if get_language() == "de" else "hamilton integrals for spatial functions"
    return "unbekannt" if get_language() == "de" else "unknown"


